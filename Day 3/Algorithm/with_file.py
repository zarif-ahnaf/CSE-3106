from tabulate import tabulate
import matplotlib.pyplot as plt

processes = {}

# Load data
with open("test.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        pid, arrival_time, burst_time = line.split(",")
        processes[pid] = {
            "arrival_time": int(arrival_time),
            "burst_time": int(burst_time),
        }

# Sort by arrival time
sorted_processes = sorted(processes.items(), key=lambda x: x[1]["arrival_time"])

# FCFS Scheduling
current_time = 0
execution_order = []

for pid, info in sorted_processes:
    arrival = info["arrival_time"]
    burst = info["burst_time"]

    if current_time < arrival:
        current_time = arrival

    ct = current_time + burst
    tat = ct - arrival
    wt = tat - burst

    processes[pid]["completion_time"] = ct
    processes[pid]["turnaround_time"] = tat
    processes[pid]["waiting_time"] = wt

    execution_order.append(pid)
    current_time = ct

# Print table
table = []
for pid, info in processes.items():
    table.append(
        [
            pid,
            info["arrival_time"],
            info["burst_time"],
            info["completion_time"],
            info["turnaround_time"],
            info["waiting_time"],
        ]
    )

print(
    tabulate(table, headers=["PID", "AT", "BT", "CT", "TAT", "WT"], tablefmt="orgtbl")
)

print(
    "Average Turnaround Time:",
    sum(info["turnaround_time"] for info in processes.values()) / len(processes),
)
print(
    "Average Waiting Time:",
    sum(info["waiting_time"] for info in processes.values()) / len(processes),
)

# Prepare Gantt chart data
gantt_data = []
current_time = 0
for pid in execution_order:
    info = processes[pid]
    start_time = max(current_time, info["arrival_time"])
    end_time = start_time + info["burst_time"]
    gantt_data.append((pid, start_time, end_time))
    current_time = end_time

# Plot both Ready Queue and Gantt Chart in one figure
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(12, 4), gridspec_kw={"height_ratios": [1, 2]}
)

# Ready Queue on top
for idx, pid in enumerate(execution_order):
    ax1.barh(0, 1, left=idx, height=0.5, edgecolor="black", color="lightgreen")
    ax1.text(idx + 0.5, 0, f"P{pid}", ha="center", va="center", color="black")

ax1.set_yticks([])
ax1.set_xticks(range(len(execution_order) + 1))
ax1.set_xticklabels([str(i) for i in range(len(execution_order) + 1)])
ax1.set_xlabel("Queue Position")
ax1.set_title("Ready Queue (Order of Execution)")

# Gantt chart on bottom
for pid, start, end in gantt_data:
    ax2.barh(0, end - start, left=start, height=0.5, edgecolor="black", color="skyblue")
    ax2.text((start + end) / 2, 0, f"P{pid}", ha="center", va="center", color="black")

ax2.set_yticks([])
ax2.set_xlabel("Time")
ax2.set_title("Gantt Chart")

plt.tight_layout()
plt.show()
