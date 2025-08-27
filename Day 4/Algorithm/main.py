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


time_executed = 0
process_dict.sort(key=lambda x: x["arrival_time"])
ready_queue = copy(process_dict)
final_table = {}

while len(process_dict) > 0:
    process_that_can_be_executed = []
    for process in process_dict:
        if process["arrival_time"] <= time_executed:
            process_that_can_be_executed.append(process)
    process_that_can_be_executed.sort(key=lambda x: x["id"])

    min_process = min(process_that_can_be_executed, key=lambda p: p["burst_time"])
    time_executed += min_process["burst_time"]

    process_dict = [
        process for process in process_dict if process["id"] != min_process["id"]
    ]
    process_id = min_process["id"]
    waiting_time = min_process["waiting_time"] = (
        time_executed - min_process["arrival_time"] - min_process["burst_time"]
    )
    turn_around_time = min_process["turnaround_time"] = (
        time_executed - min_process["arrival_time"]
    )
    final_table[process_id] = {
        "waiting_time": waiting_time,
        "turnaround_time": turn_around_time,
    }
    final_table[process_id]["completion_time"] = time_executed

# --- Prepare ready queue bars ---
ready_queue_bars = []  # each entry: (pid, start_time, end_time)
time_executed = 0
process_dict_copy = ready_queue.copy()

while len(process_dict_copy) > 0:
    # processes that have arrived
    current_ready = [p for p in process_dict_copy if p["arrival_time"] <= time_executed]

    if current_ready:
        # choose process with minimal burst time
        min_process = min(current_ready, key=lambda p: p["burst_time"])
        start_time = time_executed
        end_time = start_time + min_process["burst_time"]

        # ready queue bar: from arrival to execution start
        for p in current_ready:
            ready_queue_bars.append((p["id"], p["arrival_time"], start_time))

        time_executed = end_time
        process_dict_copy = [
            p for p in process_dict_copy if p["id"] != min_process["id"]
        ]
    else:
        time_executed += 1  # CPU idle

# --- Plot Ready Queue and Gantt Chart ---
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# 1️⃣ Ready Queue as bar chart
ax = axes[0]
for pid, start, end in ready_queue_bars:
    ax.barh(pid, end - start, left=start, height=0.4, color=f"C{pid % 10}")
ax.set_ylabel("Process ID")
ax.set_yticks([p["id"] for p in ready_queue])
ax.set_title("Ready Queue (Waiting Time Before Execution)")

# 2️⃣ Gantt Chart
ax = axes[1]
timeline = sorted(final_table.items(), key=lambda x: x[1]["completion_time"])
for pid, data in timeline:
    burst_time = data["turnaround_time"] - data["waiting_time"]
    start_time = data["completion_time"] - burst_time
    ax.barh(pid, burst_time, left=start_time, height=0.4, color=f"C{pid % 10}")
    ax.text(
        start_time + burst_time / 2,
        pid,
        f"P{pid}",
        ha="center",
        va="center",
        color="white",
    )
ax.set_ylabel("Process ID")
ax.set_xlabel("Time")
ax.set_title("Gantt Chart (Execution Timeline)")

plt.tight_layout()
plt.show()
