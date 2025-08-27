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
