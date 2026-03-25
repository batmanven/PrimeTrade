import click
import logging
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from bot.logging_config import setup_logging
from bot.orders import OrderManager

# Set up logging early
logger = setup_logging()
console = Console()

@click.group()
def cli():
    """Binance Futures Testnet Trading Bot CLI."""
    pass

@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading symbol (e.g., BTCUSDT)')
@click.option('--side', '-d', type=click.Choice(['BUY', 'SELL', 'buy', 'sell'], case_sensitive=False), required=True, help='Order side (BUY/SELL)')
@click.option('--type', '-t', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'STOP_LIMIT', 'market', 'limit', 'stop_limit'], case_sensitive=False), required=True, help='Order type (MARKET/LIMIT/STOP_LIMIT)')
@click.option('--quantity', '-q', type=float, required=True, help='Quantity of the asset')
@click.option('--price', '-p', type=float, help='Price for LIMIT/STOP_LIMIT order')
@click.option('--stop-price', '-sp', type=float, help='Stop price for STOP_LIMIT order')
def order(symbol, side, order_type, quantity, price, stop_price):
    """Place a Market, Limit, or Stop-Limit order on Binance Futures Testnet."""
    
    # 1. Logic for required price in LIMIT/STOP_LIMIT orders
    if order_type.upper() in ['LIMIT', 'STOP_LIMIT'] and price is None:
        console.print("[bold red]Error:[/bold red] Price is required for LIMIT/STOP_LIMIT orders.")
        sys.exit(1)
    
    if order_type.upper() == 'STOP_LIMIT' and stop_price is None:
        console.print("[bold red]Error:[/bold red] Stop Price is required for STOP_LIMIT orders.")
        sys.exit(1)
        
    try:
        # Create OrderManager
        manager = OrderManager()
        
        # 2. Display Request Summary
        console.print(f"\n[cyan]>>> Sending {order_type.upper()} {side.upper()} order for {quantity} {symbol.upper()}...[/cyan]")
        
        # 3. Process Order
        success, result = manager.process_order(
            symbol=symbol, 
            side=side, 
            order_type=order_type, 
            quantity=quantity, 
            price=price,
            stop_price=stop_price
        )
        
        if success:
            console.print("\n[bold green]✅ Order Placed Successfully![/bold green]")
            
            # Use Rich Table for pretty result output
            table = Table(title="Order Confirmation", show_header=True, header_style="bold magenta")
            table.add_column("Field", style="dim", width=15)
            table.add_column("Value")
            
            for key, val in result.items():
                table.add_row(str(key), str(val))
            
            console.print(table)
        else:
            console.print(f"\n[bold red]❌ Order Failed:[/bold red] {result}")

    except ValueError as ve:
        console.print(f"\n[bold red]Configuration Error:[/bold red] {ve}")
        console.print("[dim]Ensure BINANCE_API_KEY and BINANCE_API_SECRET are set in your .env file.[/dim]")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {str(e)}")

@cli.command()
def balance():
    """Check your account balance on the testnet."""
    try:
        manager = OrderManager()
        balances = manager.client.get_account_balance()
        
        table = Table(title="Account Balances (Non-Zero Only)", show_header=True)
        table.add_column("Asset")
        table.add_column("Balance")
        table.add_column("Available Balance")
        
        # Filter for non-zero balances
        non_zero = [b for b in balances if float(b['balance']) > 0]
        
        for b in non_zero:
            table.add_row(b['asset'], f"{float(b['balance']):.4f}", f"{float(b['withdrawAvailable']):.4f}")
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error fetching balances:[/bold red] {e}")

if __name__ == "__main__":
    cli()
