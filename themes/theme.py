from rich.console import Console
from rich.theme import Theme


def set_rich_console():
    theme = Theme({
        "error": "red",
        "success": "bold green",
        "menu_selection": "bright_blue bold",
        "menu_text": "bright_blue",
        "panel": "bold blue",
        "input": "bold cyan"
    })
    return Console(theme=theme)
