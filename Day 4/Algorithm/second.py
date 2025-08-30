import matplotlib.pyplot as plt
from copy import copy
from tabulate import tabulate
process_dict: list[dict[str, int]] = []

# --- Read processes from file ---
with open("process.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        id, arrival_time, burst_time = map(int, line.strip().split(","))
        process_dic = {
            "id": id,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
        }
        process_dict.append(process_dic)

# --- Sort by arrival time for ready queue ---
ready_queue = copy(process_dict)
ready_queue.sort(key=lambda x: x["arrival_time"])

# --- FCFS / SJF Simulation ---
time_executed = 0
process_list = copy(process_dict)
final_table = {}
gantt_chart = []

while len(process_list) > 0:
    # Find processes that have arrived
    process_that_can_be_executed = [
        p for p in process_list if p["arrival_time"] <= time_executed
    ]

    if not process_that_can_be_executed:
        # If no process has arrived, jump to next arrival
        next_process = min(process_list, key=lambda p: p["arrival_time"])
        time_executed = next_process["arrival_time"]
        process_that_can_be_executed.append(next_process)

    # Select process with minimal burst time (SJF)
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

result_rows = []
total_tat = 0
total_wt = 0

for p in process_dict:
    pid = p["id"]
    at = p["arrival_time"]
    bt = p["burst_time"]
    ct = final_table[pid]["completion_time"]
    tat = final_table[pid]["turnaround_time"]
    wt = final_table[pid]["waiting_time"]
    rt = wt  # Non-preemptive → RT = WT

    total_tat += tat
    total_wt += wt

    result_rows.append([pid, at, bt, ct, tat, wt, rt])

# --- Print Table ---
headers = ["PID", "AT", "BT", "CT", "TAT", "WT", "RT"]
print(tabulate(result_rows, headers=headers, tablefmt="grid"))

# --- Print Averages ---
n = len(process_dict)
print(f"\nAverage TAT = {total_tat / n:.2f}")
print(f"Average WT  = {total_wt / n:.2f}")

# --- Visualization ---
fig, axes = plt.subplots(2, 1, figsize=(10, 6))

# --- Ready Queue (arrival times) with y-offset for same arrival time ---
y_positions = []
y_counter = {}
for p in ready_queue:
    arrival = p["arrival_time"]
    if arrival not in y_counter:
        y_counter[arrival] = 0
    y_positions.append(y_counter[arrival])
    y_counter[arrival] += 1

axes[0].barh(
    y_positions,
    [1] * len(ready_queue),
    left=[p["arrival_time"] for p in ready_queue],
    color="skyblue",
    edgecolor="black",
)

# Label each bar with process ID
for y_pos, p in zip(y_positions, ready_queue):
    axes[0].text(p["arrival_time"] + 0.1, y_pos, f"P{p['id']}", va="center")

axes[0].set_ylabel("Processes")
axes[0].set_title("Ready Queue (Arrival Times)")
axes[0].set_xlabel("Time (Arrival)")
axes[0].set_yticks([])  # Hide default y-axis ticks
axes[0].grid(axis="x")

# --- Gantt Chart (execution timeline) ---
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
