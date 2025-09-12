# Shortest Job First

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

process_dict = dict(sorted(process_dict.items(), key=lambda x: x[1]["arrival_time"]))
finalized_process_list = []


execution_time = 0

while process_dict:
    # Get processes that have arrived so far
    available_processes = {
        k: v for k, v in process_dict.items() if v["arrival_time"] <= execution_time
    }

    if not available_processes:
        # No process has arrived yet; jump to the arrival time of the earliest one
        next_process_key = min(
            process_dict, key=lambda x: process_dict[x]["arrival_time"]
        )
        execution_time = process_dict[next_process_key]["arrival_time"]
        available_processes = {
            k: v for k, v in process_dict.items() if v["arrival_time"] <= execution_time
        }

    # Select the process with the shortest burst time among available
    selected_process_key = min(
        available_processes, key=lambda x: available_processes[x]["burst_time"]
    )
    selected_process = process_dict[selected_process_key]

    # Compute times
    execution_time += selected_process["burst_time"]
    selected_process["completion_time"] = execution_time
    selected_process["turnaround_time"] = (
        execution_time - selected_process["arrival_time"]
    )
    selected_process["waiting_time"] = (
        selected_process["turnaround_time"] - selected_process["burst_time"]
    )

    # Add to final list and remove from process_dict
    finalized_process_list.append((selected_process_key, selected_process))
    del process_dict[selected_process_key]
