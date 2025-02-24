import numpy as np
import random
import time
import typer
from rich.console import Console
from rich.live import Live
from rich.text import Text

app = typer.Typer()
console = Console()

height = 16
width = 16
grid = np.zeros((height, width), dtype=int)
nodes = []
current_height = height - 1  # Start at the bottom
tri = Text(" ", style = "on #00dd55")
sky = Text(" ", style = "on #0055dd")

def generate_tree():
    """Initialize the tree with a trunk."""
    global current_height
    x_center = width // 2
    grid[current_height, x_center] = 1
    nodes.append([current_height, x_center])

def update_tree():
    """Grow the tree upwards with branching."""
    global current_height
    new_nodes = []
    
    if current_height <= 0:
        return  # Stop when reaching the top

    for node in nodes:
        y, x = node  # Get current position

        if y == current_height:  # Only grow from the highest row
            for dx in [-1, 0, 1]:  # Try growing left, center, or right
                if random.random() < 0.5 - ((height-current_height+1)/((2-(abs(dx)))*height)):  # 50% chance of growing
                    new_x, new_y = x + dx, y - 1
                    if 0 <= new_x < width and new_y >= 0:
                        grid[new_y, new_x] = 1
                        new_nodes.append([new_y, new_x])
    
    nodes.extend(new_nodes)  # Add new branches
    current_height -= 1  # Move growth upward

def display():
    """Convert grid into a string with colors for Rich display."""
    output = Text("")
    for row in grid:
        for cell in row:
            output += tri if cell == 1 else sky
        output += "\n"
    return output

@app.command()
def main():
    generate_tree()
    
    with Live(display(), refresh_per_second=10) as live:
        for _ in range(height - 1):
            update_tree()
            live.update(display())  # Update the visual output
            time.sleep(0.5)  # Slow down animation for visibility

    console.print("[bold cyan]Tree generation complete![/bold cyan]")

if __name__ == "__main__":
    app()

