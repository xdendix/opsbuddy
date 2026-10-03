# app/ui.py
from rich.console import Console
from rich.panel import Panel

console = Console()
ACCENT_COLOR = "dark_orange"


def print_header():
    title = "[bold dark_orange]🐧 OpsBuddy: The Local AI Sandbox[/bold dark_orange]"
    console.print(Panel.fit(title, border_style=ACCENT_COLOR))
    console.print("Type 'exit' or 'quit' to close the session.\n")
