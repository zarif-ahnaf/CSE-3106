from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import matplotlib.pyplot as plt
import numpy as np

console = Console()

def create_disk_diagram(path, algorithm, y_offsets=None):
    """Create a disk scheduling diagram matching the reference image style"""
    cylinders = [0, 16, 24, 43, 50, 82, 100, 140, 150, 170, 190, 199]
    
    fig, ax = plt.subplots(figsize=(12, 3))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    # Draw disk track
    ax.plot([-5, 205], [0, 0], color='gray', linewidth=1.5)
    
    # Draw cylinder ticks and labels
    for pos in cylinders:
        ax.plot([pos, pos], [0, 0.2], 'k-', linewidth=1.5)
        ax.text(pos, 0.3, str(pos), ha='center', va='bottom', 
                fontsize=10, fontfamily='monospace')
    
    # Default offsets for standard zigzag pattern
    if y_offsets is None:
        y_offsets = [0.4, 0.8, -0.4, -0.8, 0.4, 0.8, -0.4]
    
    # Draw the path with green arrows
    for i in range(len(path) - 1):
        x1, x2 = path[i], path[i+1]
        y = y_offsets[i] if i < len(y_offsets) else y_offsets[-1]
        
        ax.annotate('', 
                   xy=(x2, y), 
                   xytext=(x1, y),
                   arrowprops=dict(
                       arrowstyle='-|>', 
                       color='#4CAF50', 
                       lw=2,
                       shrinkA=0,
                       shrinkB=0
                   ))
    
    # Add final arrow to indicate continuation
    if len(path) > 1:
        last_x = path[-1]
        last_y = y_offsets[-1] if len(y_offsets) > len(path)-2 else y_offsets[-1]
        ax.annotate('', 
                   xy=(205, last_y), 
                   xytext=(last_x, last_y),
                   arrowprops=dict(
                       arrowstyle='-|>', 
                       color='#4CAF50', 
                       lw=2,
                       shrinkA=0,
                       shrinkB=0
                   ))
    
    ax.set_xlim(-5, 205)
    ax.set_ylim(-1.5, 1.5)
    plt.tight_layout()
    return fig

def explain_fcfs():
    """Generate FCFS explanation with RICH formatting"""
    console.print(Panel(Text("FCFS (First Come First Serve)", style="bold blue"), title="Algorithm", width=40))
    
    text = Text()
    text.append("FCFS is the simplest disk scheduling algorithm where requests are addressed in the order they arrive in the disk queue.\n\n", style="white")
    
    text.append("Current head position: ", style="green")
    text.append("50\n", style="bold yellow")
    
    text.append("Request order: ", style="green")
    text.append("[82, 170, 43, 140, 24, 16, 190]\n\n", style="bold yellow")
    
    text.append("Total head movement calculation:\n", style="green")
    text.append("(82-50) + (170-82) + (170-43) + (140-43) + (140-24) + (24-16) + (190-16)\n", style="white")
    text.append("= 32 + 88 + 127 + 97 + 116 + 8 + 174 = ", style="white")
    text.append("642 cylinders", style="bold magenta")
    
    console.print(Panel(text, title="Calculation", border_style="green"))
    
    advantages = [
        "Every request gets a fair chance",
        "No indefinite postponement"
    ]
    
    disadvantages = [
        "Does not try to optimize seek time",
        "May not provide the best possible service"
    ]
    
    # Create advantages/disadvantages table
    table = Table(title="Algorithm Characteristics", show_header=False, border_style="blue")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="white")
    
    for adv in advantages:
        table.add_row("✓ Advantages", adv)
    
    for disc in disadvantages:
        table.add_row("✗ Disadvantages", disc)
    
    console.print(table)

def explain_scan():
    """Generate SCAN explanation with RICH formatting"""
    console.print(Panel(Text("SCAN (Elevator Algorithm)", style="bold blue"), title="Algorithm", width=40))
    
    text = Text()
    text.append("SCAN moves the disk arm to the end of the disk in one direction, servicing requests along the way, then reverses direction.\n\n", style="white")
    
    text.append("Current head position: ", style="green")
    text.append("50\n", style="bold yellow")
    
    text.append("Request order: ", style="green")
    text.append("[82, 170, 43, 140, 24, 16, 190]\n\n", style="bold yellow")
    
    text.append("Service order: ", style="green")
    text.append("50 → 82 → 140 → 170 → 190 → 199 → 43 → 24 → 16\n\n", style="white")
    
    text.append("Total head movement calculation:\n", style="green")
    text.append("(82-50) + (140-82) + (170-140) + (190-170) + (199-190) + (199-43) + (43-24) + (24-16)\n", style="white")
    text.append("= 32 + 58 + 30 + 20 + 9 + 156 + 19 + 8 = ", style="white")
    text.append("332 cylinders", style="bold magenta")
    
    console.print(Panel(text, title="Calculation", border_style="green"))
    
    advantages = [
        "Better performance than FCFS",
        "Reduces average seek time significantly",
        "Avoids starvation of requests"
    ]
    
    disadvantages = [
        "Requests near the current head position may wait longer",
        "More complex than FCFS"
    ]
    
    table = Table(title="Algorithm Characteristics", show_header=False, border_style="blue")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="white")
    
    for adv in advantages:
        table.add_row("✓ Advantages", adv)
    
    for disc in disadvantages:
        table.add_row("✗ Disadvantages", disc)
    
    console.print(table)

def main():
    # FCFS Example (matching the reference image)
    fcfs_path = [50, 82, 170, 43, 140, 24, 16, 190]
    fcfs_y_offsets = [0.4, 0.8, -0.4, -0.8, 0.4, 0.8, -0.4]
    
    # SCAN Example (using the same request set)
    scan_path = [50, 82, 140, 170, 190, 199, 43, 24, 16]
    scan_y_offsets = [0.4, 0.8, 0.9, 1.0, -0.4, -0.8, -0.9]
    
    # Display FCFS
    console.print("\n[bold green]===== FCFS DISK SCHEDULING =====[/bold green]")
    explain_fcfs()
    
    fig1 = create_disk_diagram(fcfs_path, "FCFS", fcfs_y_offsets)
    console.print("\n[bold cyan]Visual representation:[/bold cyan]")
    plt.show()
    
    # Display SCAN
    console.print("\n[bold green]===== SCAN DISK SCHEDULING =====[/bold green]")
    explain_scan()
    
    fig2 = create_disk_diagram(scan_path, "SCAN", scan_y_offsets)
    console.print("\n[bold cyan]Visual representation:[/bold cyan]")
    plt.show()

if __name__ == "__main__":
    main()