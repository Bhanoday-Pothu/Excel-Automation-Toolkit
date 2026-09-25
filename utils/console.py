from rich.console import Console
console=Console()

def success(message):
    console.print(f"[bold green]✓ {message}[/bold green]")
    
def error(message):
    console.print(f"[bold red]✗ {message}[/bold red]")
    
def info(message):
    console.print(f"[bold cyan]{message}[/bold cyan]")

def warning(message):
    console.print(f"[bold yellow]{message}[/bold yellow]")
    
from rich.table import Table

def show_report(stats):
    table= Table(title="Cleaning report")
    
    table.add_column("Metric",style="cyan")
    table.add_column("Value", style="green", justify="center")
    
    for key, value in stats.items():
        table.add_row(key,str(value))
        
    console.print(table)