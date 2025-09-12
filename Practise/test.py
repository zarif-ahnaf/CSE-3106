# First Come First Serve

process_dict = {}
with open("process.txt", "r") as f:
    for line in f:
        line = line.strip()
        process_id, arrival_time, burst_time = line.split(",")
        arrival_time = int(arrival_time)
        burst_time = int(burst_time)
        process_dict[process_id] = {
            "arrival_time": arrival_time,
            "burst_time": burst_time,
        }

process_dict = sorted(process_dict.items(), key=lambda x: x[1]["arrival_time"])


execution_time = 0
for key, value in process_dict:
    if execution_time < value["arrival_time"]:
        execution_time = value["arrival_time"]
    execution_time += value["burst_time"]
    value["completion_time"] = execution_time

    turnaround_time = value["completion_time"] - value["arrival_time"]
    waiting_time = turnaround_time - value["burst_time"]
    value["turnaround_time"] = turnaround_time
    value["waiting_time"] = waiting_time


for pid in process_dict:
    print(f"Process ID: {pid[0]}, Details: {pid[1]}")
