import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


# ======================
# PAGE REPLACEMENT ALGORITHMS
# ======================

def fifo_page_replacement(pages, frame_size):
    frames = []
    fault_sequence = []
    frames_history = []

    for ref in pages:
        if ref not in frames:
            fault_sequence.append(True)
            if len(frames) >= frame_size:
                frames.pop(0)
            frames.append(ref)
        else:
            fault_sequence.append(False)
        frames_history.append(frames.copy())
    return fault_sequence, frames_history


def optimal_page_replacement(pages, frame_size):
    frames = []
    fault_sequence = []
    frames_history = []

    for idx, ref in enumerate(pages):
        if ref not in frames:
            fault_sequence.append(True)
            if len(frames) >= frame_size:
                future_use = {}
                for page in frames:
                    next_use = float("inf")
                    for j in range(idx + 1, len(pages)):
                        if pages[j] == page:
                            next_use = j
                            break
                    future_use[page] = next_use
                victim = max(future_use, key=future_use.get)
                frames.remove(victim)
            frames.append(ref)
        else:
            fault_sequence.append(False)
        frames_history.append(frames.copy())
    return fault_sequence, frames_history


def lru_page_replacement(pages, frame_size):
    frames = []
    last_used = {}
    fault_sequence = []
    frames_history = []

    for idx, ref in enumerate(pages):
        if ref in frames:
            last_used[ref] = idx
            fault_sequence.append(False)
        else:
            fault_sequence.append(True)
            if len(frames) < frame_size:
                frames.append(ref)
            else:
                lru_page = min(frames, key=lambda p: last_used.get(p, -1))
                lru_index = frames.index(lru_page)
                frames[lru_index] = ref
            last_used[ref] = idx
        frames_history.append(frames.copy())
    return fault_sequence, frames_history


# ======================
# VISUALIZATION FUNCTIONS
# ======================

def visualize_terminal(pages, frame_size, algorithm_name, fault_sequence, frames_history):
    console.print(f"\n[bold green]{algorithm_name} Page Replacement[/bold green]")
    console.print("=" * 80)

    n = len(pages)
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    for _ in pages:
        table.add_column(justify="center", width=6)

    table.add_row(*[str(p) for p in pages], style="bold green")

    for row_idx in range(frame_size):
        cells = []
        for frames in frames_history:
            if row_idx < len(frames):
                cells.append(f"[{frames[row_idx]}]")
            else:
                cells.append("[ ]")
        table.add_row(*cells)

    status_cells = []
    for is_fault in fault_sequence:
        text = "Miss" if is_fault else "Hit"
        color = "red" if is_fault else "green"
        status_cells.append(Text(text, style=color))
    table.add_row(*status_cells)

    console.print(table)

    total_refs = len(pages)
    miss_count = sum(fault_sequence)
    hit_count = total_refs - miss_count
    hit_rate = (hit_count / total_refs) * 100 if total_refs > 0 else 0
    miss_rate = (miss_count / total_refs) * 100 if total_refs > 0 else 0

    console.print(f"\n[bold]Total Page Fault = {miss_count}[/bold]")
    console.print(f"Total References = {total_refs}")
    console.print(f"Hit Count = {hit_count}")
    console.print(f"Miss Count = {miss_count}")
    console.print(f"Hit Rate = {hit_rate:.2f}%")
    console.print(f"Miss Rate = {miss_rate:.2f}%")
    console.print("=" * 80)


def visualize_gui(pages, frame_size, algorithm_name, fault_sequence, frames_history):
    n = len(pages)
    if n == 0:
        return

    fig, axes = plt.subplots(1, n, figsize=(1.8 * n, 4.5), sharey=True)
    fig.suptitle(
        f"{algorithm_name} Page Replacement", fontsize=14, color="green", weight="bold"
    )

    ax_list = axes if n > 1 else [axes]
    for ax in ax_list:
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.5, frame_size - 0.5)
        ax.set_xticks([])
        ax.set_yticks([])

    for i in range(n):
        ax = ax_list[i]
        ref = pages[i]
        is_fault = fault_sequence[i]
        frames = frames_history[i]

        ax.text(
            0,
            frame_size - 0.2,
            str(ref),
            ha="center",
            va="center",
            fontsize=11,
            color="green",
            weight="bold",
        )

        for j in range(frame_size):
            y_pos = frame_size - j - 1
            if j < len(frames):
                rect = patches.Rectangle(
                    (-0.4, y_pos - 0.4),
                    0.8,
                    0.8,
                    linewidth=1.2,
                    edgecolor="green",
                    facecolor="white",
                )
                ax.add_patch(rect)
                ax.text(0, y_pos, str(frames[j]), ha="center", va="center", fontsize=9)
            else:
                rect = patches.Rectangle(
                    (-0.4, y_pos - 0.4),
                    0.8,
                    0.8,
                    linewidth=1,
                    edgecolor="lightgray",
                    facecolor="white",
                    linestyle="--",
                )
                ax.add_patch(rect)

        status = "Miss" if is_fault else "Hit"
        color = "red" if is_fault else "green"
        ax.text(
            0,
            -0.3,
            status,
            ha="center",
            va="center",
            fontsize=9,
            color=color,
            weight="bold",
        )

    total_faults = sum(fault_sequence)
    fig.text(
        0.5,
        0.02,
        f"Total Page Fault = {total_faults}",
        ha="center",
        fontsize=12,
        color="green",
        weight="bold",
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.show()


# ======================
# INPUT & MAIN LOGIC
# ======================

def get_reference_string():
    while True:
        try:
            user_input = input("Enter reference string (comma-separated integers): ").strip()
            if not user_input:
                console.print("[red]Input cannot be empty.[/red]")
                continue
            pages = [int(x.strip()) for x in user_input.split(',')]
            if not pages:
                console.print("[red]At least one page reference is required.[/red]")
                continue
            return pages
        except ValueError:
            console.print("[red]Invalid input. Please enter integers separated by commas (e.g., 7,0,1,2).[/red]")


def get_frame_size():
    while True:
        try:
            fs = int(input("Enter number of frames: "))
            if fs <= 0:
                console.print("[red]Frame size must be a positive integer.[/red]")
                continue
            return fs
        except ValueError:
            console.print("[red]Invalid input. Please enter a positive integer.[/red]")


def choose_algorithms():
    console.print("\n[bold cyan]Available Algorithms:[/bold cyan]")
    console.print("1. FIFO")
    console.print("2. LRU")
    console.print("3. Optimal")
    console.print("4. Run All")
    
    algo_map = {
        "1": ["FIFO"],
        "2": ["LRU"],
        "3": ["Optimal"],
        "4": ["FIFO", "LRU", "Optimal"]
    }

    while True:
        choice = input("\nSelect algorithm(s) [1-4]: ").strip()
        if choice in algo_map:
            return algo_map[choice]
        else:
            console.print("[red]Invalid choice. Please enter 1, 2, 3, or 4.[/red]")


def main():
    console.print("[bold blue]Page Replacement Algorithm Simulator[/bold blue]\n")

    pages = get_reference_string()
    frame_size = get_frame_size()
    selected_algos = choose_algorithms()

    algorithms = {
        "FIFO": fifo_page_replacement,
        "LRU": lru_page_replacement,
        "Optimal": optimal_page_replacement,
    }

    results = {}

    for name in selected_algos:
        func = algorithms[name]
        faults, history = func(pages, frame_size)
        results[name] = {
            "faults": faults,
            "history": history,
            "fault_count": sum(faults),
        }
        # Terminal visualization
        visualize_terminal(pages, frame_size, name, faults, history)
        # Matplotlib GUI visualization
        visualize_gui(pages, frame_size, name, faults, history)

    # Final comparison (only if more than one algorithm was run)
    if len(results) > 1:
        console.print("\n[bold yellow]=== FINAL COMPARISON ===[/bold yellow]")
        comp_table = Table(title="Algorithm Comparison", box=box.ROUNDED)
        comp_table.add_column("Algorithm", style="cyan")
        comp_table.add_column("Page Faults", style="magenta")
        comp_table.add_column("Hit Rate (%)", style="green")

        total_refs = len(pages)
        best_algo = min(results.items(), key=lambda x: x[1]["fault_count"])

        for name, data in results.items():
            fault_count = data["fault_count"]
            hit_rate = ((total_refs - fault_count) / total_refs) * 100
            comp_table.add_row(name, str(fault_count), f"{hit_rate:.2f}")

        console.print(comp_table)
        console.print(f"\n[bold green]🏆 Best Algorithm: {best_algo[0]} (Page Faults = {best_algo[1]['fault_count']})[/bold green]")
    else:
        name = selected_algos[0]
        fault_count = results[name]["fault_count"]
        console.print(f"\n[bold]Result for {name}:[/bold] Page Faults = {fault_count}")


if __name__ == "__main__":
    main()