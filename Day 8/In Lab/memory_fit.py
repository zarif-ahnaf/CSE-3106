import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

console = Console()

# --- Allocation Algorithms (return allocation + final blocks) ---
def first_fit(block_sizes, process_sizes):
    allocation = [None] * len(process_sizes)
    blocks = block_sizes[:]
    for i, proc in enumerate(process_sizes):
        for j, block in enumerate(blocks):
            if block >= proc:
                allocation[i] = j
                blocks[j] -= proc
                break
    return allocation, blocks

def best_fit(block_sizes, process_sizes):
    allocation = [None] * len(process_sizes)
    blocks = block_sizes[:]
    for i, proc in enumerate(process_sizes):
        best_idx = -1
        min_diff = float('inf')
        for j, block in enumerate(blocks):
            if block >= proc:
                diff = block - proc
                if diff < min_diff:
                    min_diff = diff
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blocks[best_idx] -= proc
    return allocation, blocks

def worst_fit(block_sizes, process_sizes):
    allocation = [None] * len(process_sizes)
    blocks = block_sizes[:]
    for i, proc in enumerate(process_sizes):
        worst_idx = -1
        max_diff = -1
        for j, block in enumerate(blocks):
            if block >= proc:
                diff = block - proc
                if diff > max_diff:
                    max_diff = diff
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blocks[worst_idx] -= proc
    return allocation, blocks

def next_fit(block_sizes, process_sizes):
    allocation = [None] * len(process_sizes)
    blocks = block_sizes[:]
    last_idx = 0
    n = len(blocks)
    for i, proc in enumerate(process_sizes):
        allocated = False
        start = last_idx
        while True:
            if blocks[last_idx] >= proc:
                allocation[i] = last_idx
                blocks[last_idx] -= proc
                last_idx = (last_idx + 1) % n
                allocated = True
                break
            last_idx = (last_idx + 1) % n
            if last_idx == start:
                break
        if not allocated:
            allocation[i] = None
    return allocation, blocks

# --- Fragmentation Calculator ---
def calculate_fragmentation(original_blocks, final_blocks, allocation, process_sizes):
    internal_frag = 0
    allocated_blocks = set()
    block_process_map = {}

    for i, blk in enumerate(allocation):
        if blk is not None:
            allocated_blocks.add(blk)
            if blk not in block_process_map:
                block_process_map[blk] = []
            block_process_map[blk].append(process_sizes[i])

    for blk in allocated_blocks:
        total_proc_in_block = sum(block_process_map[blk])
        internal_frag += original_blocks[blk] - total_proc_in_block

    external_frag = sum(final_blocks)
    return internal_frag, external_frag

# --- Visualization ---
def visualize_memory(original_blocks, final_blocks, allocation, process_sizes, algorithm_name):
    n_blocks = len(original_blocks)
    y_positions = np.arange(n_blocks)
    block_height = 0.6
    current_x = [0] * n_blocks

    fig, ax = plt.subplots(figsize=(10, 6))

    # Background: full original blocks
    for i in range(n_blocks):
        ax.barh(y_positions[i], original_blocks[i], height=block_height,
                color='whitesmoke', edgecolor='black', linewidth=0.8)

    colors = plt.cm.tab10(np.linspace(0, 1, len(process_sizes)))

    # Allocated segments
    for i, blk in enumerate(allocation):
        if blk is not None:
            size = process_sizes[i]
            ax.barh(y_positions[blk], size, left=current_x[blk],
                    height=block_height, color=colors[i],
                    edgecolor='black', linewidth=0.8, label=f'P{i} ({size})')
            current_x[blk] += size

    # Free space
    for i in range(n_blocks):
        free = final_blocks[i]
        if free > 0:
            ax.barh(y_positions[i], free, left=current_x[i],
                    height=block_height, color='lightgray',
                    edgecolor='black', linewidth=0.8)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([f'Block {i}\n({original_blocks[i]})' for i in range(n_blocks)])
    ax.set_xlabel('Memory Size')
    internal_frag, external_frag = calculate_fragmentation(original_blocks, final_blocks, allocation, process_sizes)
    ax.set_title(f'{algorithm_name} – Memory Layout\n'
                 f'(Internal Frag: {internal_frag} | External Frag: {external_frag})')
    ax.invert_yaxis()

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if by_label:
        ax.legend(by_label.values(), by_label.keys(), fontsize='small', loc='upper right')

    plt.tight_layout()
    plt.show()

# --- Input Parser ---
def parse_list_input(prompt_text):
    while True:
        try:
            user_input = Prompt.ask(prompt_text).strip()
            if not user_input:
                console.print("[red]Input cannot be empty.[/red]")
                continue
            values = [int(x.strip()) for x in user_input.split(',')]
            if any(v <= 0 for v in values):
                console.print("[red]All values must be positive integers.[/red]")
                continue
            return values
        except ValueError:
            console.print("[red]Invalid input. Use comma-separated positive integers (e.g., 100,200,300).[/red]")

# --- Main ---
def main():
    console.rule("[bold blue]Memory Allocation Simulator with Fragmentation Analysis")

    block_sizes = parse_list_input("[bold cyan]Enter memory block sizes (e.g., 100,500,200,300,600)")
    process_sizes = parse_list_input("[bold cyan]Enter process sizes (e.g., 212,417,112,426)")

    console.print("[bold green]Select an allocation algorithm:")
    console.print("1. First Fit")
    console.print("2. Best Fit")
    console.print("3. Worst Fit")
    console.print("4. Next Fit")

    while True:
        choice = Prompt.ask("[bold]Enter your choice (1-4)", choices=["1", "2", "3", "4"], default="2")
        if choice in ["1", "2", "3", "4"]:
            break
        console.print("[red]Please enter 1, 2, 3, or 4.[/red]")

    algo_map = {
        "1": ("First Fit", first_fit),
        "2": ("Best Fit", best_fit),
        "3": ("Worst Fit", worst_fit),
        "4": ("Next Fit", next_fit)
    }

    algo_name, algo_func = algo_map[choice]
    allocation, final_blocks = algo_func(block_sizes[:], process_sizes[:])

    # === Calculate Fragmentation ===
    internal_frag, external_frag = calculate_fragmentation(block_sizes, final_blocks, allocation, process_sizes)
    total_memory = sum(block_sizes)
    allocated_memory = sum(p for i, p in enumerate(process_sizes) if allocation[i] is not None)
    unused_memory = total_memory - allocated_memory  # = internal + external

    # === Rich Terminal Output ===
    console.rule(f"[bold magenta]{algo_name} – Results")

    table = Table(title="Allocation Details")
    table.add_column("Process", style="cyan", justify="center")
    table.add_column("Size", style="yellow")
    table.add_column("Block", style="green")
    table.add_column("Status", style="bold")

    for i, blk in enumerate(allocation):
        status = "[green]Allocated[/green]" if blk is not None else "[red]Not Allocated[/red]"
        block_str = f"Block {blk}" if blk is not None else "—"
        table.add_row(f"P{i}", str(process_sizes[i]), block_str, status)

    console.print(table)

    # Fragmentation Summary
    frag_table = Table(title="Fragmentation Analysis", show_header=False)
    frag_table.add_row("[bold]Total Memory:[/bold]", f"{total_memory}")
    frag_table.add_row("[bold]Allocated Memory:[/bold]", f"{allocated_memory}")
    frag_table.add_row("[bold]Unused Memory:[/bold]", f"{unused_memory}")
    frag_table.add_row("[bold]Internal Fragmentation:[/bold]", f"[blue]{internal_frag}[/blue]")
    frag_table.add_row("[bold]External Fragmentation:[/bold]", f"[red]{external_frag}[/red]")
    frag_table.add_row("[italic]Note:[/italic]", "Internal = wasted in allocated blocks; External = total free space")

    console.print(frag_table)

    # === Visualization ===
    console.print("\n[bold]Generating memory layout visualization...[/bold]")
    visualize_memory(block_sizes, final_blocks, allocation, process_sizes, algo_name)

if __name__ == "__main__":
    main()