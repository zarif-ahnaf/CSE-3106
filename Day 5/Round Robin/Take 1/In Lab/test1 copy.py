import matplotlib.pyplot as plt
from matplotlib.patches import Patch


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def round_robin(processes, quantum):
    time = 0
    ready_queue = []
    gantt_chart = []
    ready_queue_events = []  # (time, process_name)

    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    completed = 0

    while completed < n:
        # Add newly arrived processes to ready queue
        for p in processes:
            if p.arrival_time <= time and p not in ready_queue and p.remaining_time > 0:
                ready_queue.append(p)
                ready_queue_events.append((time, p.name))

        if ready_queue:
            current = ready_queue.pop(0)
            exec_time = min(current.remaining_time, quantum)
            gantt_chart.append((time, time + exec_time, current.name))
            time += exec_time
            current.remaining_time -= exec_time

            # Add newly arrived processes during execution
            for p in processes:
                if (
                    p.arrival_time <= time
                    and p not in ready_queue
                    and p.remaining_time > 0
                    and p != current
                ):
                    ready_queue.append(p)
                    ready_queue_events.append((time, p.name))

            # Reschedule current if not finished
            if current.remaining_time > 0:
                ready_queue.append(current)
                ready_queue_events.append((time, current.name))
            else:
                current.completion_time = time
                current.turnaround_time = current.completion_time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
                completed += 1
        else:
            gantt_chart.append((time, time + 1, "Idle"))
            time += 1

    return gantt_chart, ready_queue_events


def plot_gantt_chart(ax, gantt_chart, colors):
    for start, end, name in gantt_chart:
        ax.barh(
            0,
            end - start,
            left=start,
            color=colors.get(name, "lightgray"),
            edgecolor="black",
        )
        ax.text((start + end) / 2, 0, name, ha="center", va="center", fontsize=10)
    ax.set_yticks([0])
    ax.set_yticklabels(["Gantt Chart"])
    ax.set_xlim(0, gantt_chart[-1][1] + 1)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")


def plot_ready_queue(ax, ready_queue_events, colors):
    # Stack blocks vertically if they overlap
    stacked_events = []
    y_positions = []

    for time, name in ready_queue_events:
        # Find first available row without overlap
        y = 0
        while any(abs(time - t) < 1 and y == row for t, row, _ in stacked_events):
            y += 1
        stacked_events.append((time, y, name))
        y_positions.append(y)

    for time, y, name in stacked_events:
        ax.barh(y, 1, left=time, height=0.8, color=colors[name], edgecolor="black")
        ax.text(time + 0.5, y, name, va="center", ha="center", fontsize=10)

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title("Ready Queue (Arrival & Rescheduling)")


def main():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 8),
        Process("P4", 3, 6),
    ]
    quantum = 2

    gantt_chart, ready_queue_events = round_robin(processes, quantum)

    # Assign colors
    cmap = plt.cm.tab20
    all_names = list(
        set([p.name for p in processes] + [name for _, name in ready_queue_events])
    )
    colors = {name: cmap(i % 20) for i, name in enumerate(all_names)}

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=False)
    plot_gantt_chart(ax1, gantt_chart, colors)
    plot_ready_queue(ax2, ready_queue_events, colors)

    # Legend
    legend_elements = [
        Patch(facecolor=color, edgecolor="black", label=name)
        for name, color in colors.items()
    ]
    ax2.legend(handles=legend_elements, bbox_to_anchor=(1, 1), loc="upper left")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
