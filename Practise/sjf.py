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
while len(process_dict) > 0:
    first_process_key = next(iter(process_dict))
    first_process_key_value = process_dict[first_process_key]
    if first_process_key_value["arrival_time"] > execution_time:
        execution_time = first_process_key_value["arrival_time"]

    execution_time += first_process_key_value["burst_time"]
    first_process_key_value["completion_time"] = execution_time
    first_process_key_value["turnaround_time"] = (
        execution_time - first_process_key_value["arrival_time"]
    )
    first_process_key_value["waiting_time"] = (
        first_process_key_value["turnaround_time"]
        - first_process_key_value["burst_time"]
    )

    finalized_process_list.append((first_process_key, first_process_key_value))
    process_dict = {k: v for k, v in process_dict.items() if k != first_process_key}
    process_dict = dict(sorted(process_dict.items(), key=lambda x: x[1]["burst_time"]))


print(finalized_process_list)
