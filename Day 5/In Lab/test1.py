import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from tabulate import tabulate


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
    ready_queue_events = []

    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    completed = 0

    while completed < n:
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

            for p in processes:
                if (
                    p.arrival_time <= time
                    and p not in ready_queue
                    and p.remaining_time > 0
                    and p != current
                ):
                    ready_queue.append(p)
                    ready_queue_events.append((time, p.name))

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
    stacked_events = []
    for time, name in ready_queue_events:
        y = 0
        while any(abs(time - t) < 1 and y == row for t, row, _ in stacked_events):
            y += 1
        stacked_events.append((time, y, name))

    for time, y, name in stacked_events:
        ax.barh(y, 1, left=time, height=0.8, color=colors[name], edgecolor="black")
        ax.text(time + 0.5, y, name, va="center", ha="center", fontsize=10)

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title("Ready Queue (Arrival & Rescheduling)")


def main():
    processes = []
    with open("process.txt") as f:
        for line in f:
            name, arrival, burst = line.strip().split(",")
            processes.append(Process(name, int(arrival), int(burst)))
            
    quantum = 2

    gantt_chart, ready_queue_events = round_robin(processes, quantum)

    cmap = plt.cm.tab20
    all_names = list(
        set([p.name for p in processes] + [name for _, name in ready_queue_events])
    )
    colors = {name: cmap(i % 20) for i, name in enumerate(all_names)}

    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=False)
    plot_gantt_chart(ax1, gantt_chart, colors)
    plot_ready_queue(ax2, ready_queue_events, colors)

    legend_elements = [
        Patch(facecolor=color, edgecolor="black", label=name)
        for name, color in colors.items()
    ]
    ax2.legend(handles=legend_elements, bbox_to_anchor=(1, 1), loc="upper left")

    plt.tight_layout()
    plt.show()

    table_ready = [
        [time, " -> ".join([name for t, name in ready_queue_events if t == time])]
        for time, _ in ready_queue_events
    ]
    # Remove duplicates
    table_ready = [list(x) for x in {tuple(row) for row in table_ready}]
    table_ready.sort(key=lambda x: x[0])

    print("Ready Queue at Each Time Step:")
    print(tabulate(table_ready, headers=["Time", "Ready Queue"], tablefmt="fancy_grid"))

    table_process = [
        [
            p.name,
            p.arrival_time,
            p.burst_time,
            p.completion_time,
            p.turnaround_time,
            p.waiting_time,
        ]
        for p in processes
    ]
    print("Process Info:")
    print(
        tabulate(
            table_process,
            headers=[
                "Process",
                "Arrival",
                "Burst",
                "Completion",
                "Turnaround",
                "Waiting",
            ],
            tablefmt="fancy_grid",
        )
    )

    # Average WT & TAT
    n = len(processes)
    avg_wt = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

if __name__ == "__main__":
    main()
