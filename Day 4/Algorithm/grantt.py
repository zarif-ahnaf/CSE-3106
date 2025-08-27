import matplotlib.pyplot as plt
from copy import copy

process_dict: list[dict[str, int]] = []

with open("process.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        id, arrival_time, burst_time = map(int, line.split(","))
        process_dic = {
            "id": id,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
        }
        process_dict.append(process_dic)

# Sort by arrival time for ready queue
ready_queue = copy(process_dict)
ready_queue.sort(key=lambda x: x["arrival_time"])

# FCFS / SJF Simulation
time_executed = 0
process_list = copy(process_dict)
final_table = {}
gantt_chart = []

while len(process_list) > 0:
    process_that_can_be_executed = [
        p for p in process_list if p["arrival_time"] <= time_executed
    ]

    if not process_that_can_be_executed:
        next_process = min(process_list, key=lambda p: p["arrival_time"])
        time_executed = next_process["arrival_time"]
        process_that_can_be_executed.append(next_process)

    min_process = min(process_that_can_be_executed, key=lambda p: p["burst_time"])
    start_time = time_executed
    time_executed += min_process["burst_time"]

    waiting_time = start_time - min_process["arrival_time"]
    turnaround_time = waiting_time + min_process["burst_time"]

    final_table[min_process["id"]] = {
        "waiting_time": waiting_time,
        "turnaround_time": turnaround_time,
        "completion_time": time_executed,
    }

    gantt_chart.append((min_process["id"], start_time, time_executed))
    process_list = [p for p in process_list if p["id"] != min_process["id"]]

# --- Visualization ---

fig, axes = plt.subplots(2, 1, figsize=(10, 6))

# Ready Queue (arrival times)
axes[0].barh(
    [f"P{p['id']}" for p in ready_queue],
    [1] * len(ready_queue),
    left=[p["arrival_time"] for p in ready_queue],
    color="skyblue",
    edgecolor="black",
)
axes[0].set_ylabel("Processes")
axes[0].set_title("Ready Queue (Arrival Times)")
axes[0].set_yticks(range(len(ready_queue)))
axes[0].set_yticklabels([f"P{p['id']}" for p in ready_queue])
axes[0].set_xlabel("Time (Arrival)")
axes[0].grid(axis="x")

# Use only arrival times for x-axis
arrival_times = [p["arrival_time"] for p in ready_queue]
axes[0].set_xticks(range(0, max(arrival_times) + 2))

# Gantt Chart (execution timeline)
for pid, start, end in gantt_chart:
    axes[1].barh(
        1, end - start, left=start, height=0.5, color="orange", edgecolor="black"
    )
    axes[1].text(
        start + (end - start) / 2, 1, f"P{pid}", ha="center", va="center", color="white"
    )

axes[1].set_xlabel("Time (Execution)")
axes[1].set_yticks([])
axes[1].set_title("Gantt Chart")
axes[1].grid(axis="x")

plt.tight_layout()
plt.show()
