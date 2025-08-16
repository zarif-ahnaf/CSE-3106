from tabulate import tabulate

num_processes = int(input("Enter the number of processes: "))

processes = {}

for i in range(1, num_processes + 1):
    arrival_time = int(input(f"Enter arrival time for process {i}: "))
    burst_time = int(input(f"Enter burst time for process {i}: "))
    processes[i] = {"arrival_time": arrival_time, "burst_time": burst_time}

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
print(tabulate(table, headers=["PID", "AT", "BT", "CT", "TAT", "WT"], tablefmt="grid"))
print(
    "Average Turnaround Time:",
    sum(info["turnaround_time"] for info in processes.values()) / num_processes,
)
print(
    "Average Waiting Time:",
    sum(info["waiting_time"] for info in processes.values()) / num_processes,
)
