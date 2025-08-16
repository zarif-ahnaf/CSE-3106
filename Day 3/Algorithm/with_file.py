from tabulate import tabulate
import matplotlib.pyplot as plt

processes = {}

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

sorted_processes = sorted(processes.items(), key=lambda x: x[1]["arrival_time"])

current_time = 0

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

    current_time = ct

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

# Print table
print(
    tabulate(table, headers=["PID", "AT", "BT", "CT", "TAT", "WT"], tablefmt="orgtbl")
)

print(
    "Average Turnaround Time:",
    sum(info["turnaround_time"] for info in processes.values()) / len(processes.keys()),
)
print(
    "Average Waiting Time:",
    sum(info["waiting_time"] for info in processes.values()) / len(processes.keys()),
)


# Prepare Gantt chart data
gantt_data = []
current_time = 0

for pid, info in sorted(processes.items(), key=lambda x: x[1]["arrival_time"]):
    arrival = info["arrival_time"]
    burst = info["burst_time"]

    start_time = max(current_time, arrival)
    end_time = start_time + burst
    gantt_data.append((pid, start_time, end_time))
    current_time = end_time

# Plot Gantt chart
fig, ax = plt.subplots(figsize=(10, 2))
for pid, start, end in gantt_data:
    ax.barh(0, end - start, left=start, height=0.5, edgecolor="black", label=f"P{pid}")
    ax.text((start + end) / 2, 0, f"P{pid}", ha="center", va="center", color="white")

ax.set_yticks([])
ax.set_xlabel("Time")
ax.set_title("Gantt Chart")
plt.show()
