import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import heapq
from typing import List, Dict, Tuple

# Type aliases
Process = Dict[str, int]
GanttEntry = Tuple[int, int, int]
QueueState = Tuple[int, List[int]]
SchedulingResult = Dict[str, List]


def priority_scheduling(processes: List[Process]) -> SchedulingResult:
    """
    Simulates Non-Preemptive Priority CPU scheduling.
    Lower 'priority' value means higher priority.

    Args:
        processes: List of processes with 'pid', 'at', 'bt', 'priority'

    Returns:
        Dict with 'processes', 'gantt_chart', 'ready_queue'
    """
    # Create mutable working copies
    proc_list: List[Process] = [
        {
            "pid": p["pid"],
            "at": p["at"],
            "bt": p["bt"],
            "priority": p["priority"],
            "remaining": p["bt"],
        }
        for p in processes
    ]

    n: int = len(proc_list)
    for p in proc_list:
        p.update({"ct": 0, "tat": 0, "wt": 0})

    gantt_chart: List[GanttEntry] = []
    ready_queue_log: List[QueueState] = []
    current_time: int = 0
    completed: int = 0

    # We'll use a list as a priority queue: (priority, arrival_time, process)
    # arrival_time breaks ties for same priority (FCFS among same priority)
    ready_queue: List[Tuple[int, int, Process]] = []

    # Track which processes are already enqueued to avoid duplicates
    enqueued = [False] * n

    while completed < n:
        # Add all newly arrived processes that haven't been enqueued yet
        for idx, p in enumerate(proc_list):
            if p["at"] <= current_time and p["remaining"] > 0 and not enqueued[idx]:
                heapq.heappush(ready_queue, (p["priority"], p["at"], p))
                enqueued[idx] = True

        # Build current ready queue state (list of pids)
        current_ready_pids = [proc["pid"] for (_, _, proc) in ready_queue]
        ready_queue_log.append((current_time, current_ready_pids))

        if not ready_queue:
            # CPU idle: jump to next arrival time
            next_arrival = min(
                (p["at"] for p in proc_list if p["remaining"] > 0), default=current_time
            )
            current_time = next_arrival
            continue

        # Get highest priority process (lowest priority number)
        prio, at, current_proc = heapq.heappop(ready_queue)

        # Execute the process to completion (non-preemptive)
        exec_time = current_proc["bt"]
        gantt_chart.append(
            (current_proc["pid"], current_time, current_time + exec_time)
        )
        current_time += exec_time

        # Update process completion stats
        current_proc["ct"] = current_time
        current_proc["tat"] = current_proc["ct"] - current_proc["at"]
        current_proc["wt"] = current_proc["tat"] - current_proc["bt"]
        current_proc["remaining"] = 0  # mark as completed
        completed += 1

        # After execution, add any processes that arrived during this burst
        # (This is handled in the next loop iteration)

    return {
        "processes": proc_list,
        "gantt_chart": gantt_chart,
        "ready_queue": ready_queue_log,
    }


def visualize_scheduling_results(
    gantt_data: List[GanttEntry], ready_queue: List[QueueState]
) -> None:
    """
    Visualize both ready queue and execution timeline in a single window with subplots.
    """
    if not gantt_data:
        print("No Gantt chart data to visualize.")
        return

    # Create a figure with two subplots (2 rows, 1 column)
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # --- First subplot: Ready Queue visualization ---
    # Extract all unique processes and their first arrival times
    arrival_times = {}
    for time, pids in ready_queue:
        for pid in pids:
            if pid not in arrival_times:
                arrival_times[pid] = time

    # Sort processes by arrival time
    sorted_processes = sorted(
        [(pid, at) for pid, at in arrival_times.items()], key=lambda x: x[1]
    )

    # Handle processes with same arrival time by assigning different y positions
    y_positions = []
    y_counter = {}
    for pid, at in sorted_processes:
        if at not in y_counter:
            y_counter[at] = 0
        y_positions.append(y_counter[at])
        y_counter[at] += 1

    # Draw ready queue bars
    if sorted_processes:
        axes[0].barh(
            y_positions,
            [0.1]
            * len(sorted_processes),  # Very narrow bars to represent arrival points
            left=[at for _, at in sorted_processes],
            height=0.4,
            color="skyblue",
            edgecolor="black",
        )

        # Label each bar with process ID
        for i, (pid, at) in enumerate(sorted_processes):
            axes[0].text(at + 0.05, y_positions[i], f"P{pid}", va="center", ha="left")

    axes[0].set_title("Ready Queue (Process Arrivals)")
    axes[0].set_xlabel("Time")
    axes[0].set_yticks([])  # Hide y-axis ticks
    axes[0].grid(axis="x", linestyle="--", alpha=0.7)

    # Set x-axis limits based on the data
    if sorted_processes:
        max_time = max(at for _, at in sorted_processes) + 2
    else:
        max_time = 10
    axes[0].set_xlim(0, max_time)

    # --- Second subplot: Execution timeline ---
    # Get all unique time points
    time_points = sorted(set([t for entry in gantt_data for t in entry[1:]]))
    if not time_points:
        plt.close()
        return

    # Assign colors to processes
    process_colors = {}
    cmap = plt.cm.tab10
    for i, (pid, _, _) in enumerate(gantt_data):
        if pid not in process_colors:
            process_colors[pid] = cmap(i % 10)

    # Draw colored process boxes
    for pid, start, end in gantt_data:
        color = process_colors[pid]
        axes[1].barh(
            1,
            end - start,
            left=start,
            height=1,
            color=color,
            edgecolor="black",
            linewidth=1.2,
        )
        axes[1].text(
            (start + end) / 2,
            1,
            f"P{pid}",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="white"
            if color[0] + color[1] + color[2] < 1.5
            else "black",  # Contrast text color
        )

    # Add vertical grid lines at time boundaries
    for t in time_points:
        axes[1].axvline(x=t, color="black", linestyle="-", alpha=0.3)

    # Add time labels below the axis
    for t in time_points:
        axes[1].text(
            t, -0.2, f"{int(t)}", ha="center", va="top", fontsize=10, fontweight="bold"
        )

    axes[1].set_title("Execution Timeline")
    axes[1].set_xlabel("Time")
    axes[1].set_yticks([])
    axes[1].grid(axis="x", linestyle="--", alpha=0.7)
    axes[1].set_xlim(0, time_points[-1])

    plt.tight_layout()
    plt.show()


def read_processes_from_file(filename: str) -> List[Process]:
    """
    Read processes from CSV using built-in csv module.
    Expected columns: pid, at, bt, priority
    """
    processes: List[Process] = []
    try:
        with open(filename, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            required = {"pid", "at", "bt", "priority"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError(
                    f"Missing required columns: {required}. Found: {reader.fieldnames}"
                )

            for i, row in enumerate(reader, start=2):
                try:
                    pid = int(row["pid"])
                    at = int(row["at"])
                    bt = int(row["bt"])
                    priority = int(row["priority"])
                    if bt <= 0:
                        raise ValueError("Burst time must be positive")
                    processes.append(
                        {"pid": pid, "at": at, "bt": bt, "priority": priority}
                    )
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid data in row {i}: {e}") from e

        if not processes:
            raise ValueError("No valid processes found.")
        return processes

    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}") from e


def main() -> None:
    filename: str = input("Enter the input filename (e.g., processes.csv): ").strip()

    try:
        processes: List[Process] = read_processes_from_file(filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print(f"\n✅ Loaded {len(processes)} processes\n")

    result: SchedulingResult = priority_scheduling(processes)

    # Build result table
    table_rows: List[List[int]] = []
    for p in sorted(result["processes"], key=lambda x: x["pid"]):
        table_rows.append(
            [p["pid"], p["at"], p["bt"], p["priority"], p["ct"], p["tat"], p["wt"]]
        )

    avg_tat: float = sum(p["tat"] for p in result["processes"]) / len(
        result["processes"]
    )
    avg_wt: float = sum(p["wt"] for p in result["processes"]) / len(result["processes"])

    print(
        tabulate(
            table_rows,
            headers=["PID", "AT", "BT", "Priority", "CT", "TAT", "WT"],
            tablefmt="fancy_grid",
        )
    )
    print(f"\n📊 Average Turnaround Time: {avg_tat:.2f}")
    print(f"📊 Average Waiting Time: {avg_wt:.2f}")

    # Visualize everything in one window with subplots
    visualize_scheduling_results(result["gantt_chart"], result["ready_queue"])


if __name__ == "__main__":
    main()
