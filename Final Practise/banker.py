def is_system_safe(available, max_need, allocated):
    num_processes = len(allocated)
    num_resources = len(available)

    need = []
    for i in range(num_processes):
        process_need = []
        for j in range(num_resources):
            process_need.append(max_need[i][j] - allocated[i][j])
        need.append(process_need)

    # Step 2: Prepare for safety check
    work = available[:]  # Copy of available resources
    finished = [False] * num_processes
    safe_order = []  # The sequence in which processes can finish

    # Step 3: Try to find a safe sequence
    while len(safe_order) < num_processes:
        found_a_process = False

        for pid in range(num_processes):
            # Skip if already finished
            if finished[pid]:
                print(f"P{pid}: Already Executed")
                continue

            # Check if this process can get all it needs
            can_run = True
            for r in range(num_resources):
                if need[pid][r] > work[r]:
                    can_run = False

            if not can_run:
                print(f"P{pid}: The condition is false")

            # If yes, pretend it runs and finishes
            if can_run:
                # It releases its resources when done
                for r in range(num_resources):
                    work[r] += allocated[pid][r]

                finished[pid] = True
                safe_order.append(pid)
                found_a_process = True

        # If no process can run, we're stuck → unsafe!
        if not found_a_process:
            return False, None

    return True, safe_order


# -------------------------------
# Example: Easy to understand
# -------------------------------
if __name__ == "__main__":
    # There are 3 types of resources: A, B, C
    available = [4, 3, 4, 2]

    # Max resources each process might need
    max_need = [
        [5, 2, 4, 4],
        [4, 2, 6, 2],
        [2, 3, 1, 7],
        [2, 5, 3, 4],
    ]

    # Resources already given to each process
    allocated = [
        [2, 1, 1, 1],
        [3, 2, 2, 1],
        [2, 1, 1, 2],
        [1, 4, 3, 1],
    ]

    # Run the safety check
    safe, sequence = is_system_safe(available, max_need, allocated)

    if safe:
        print("The system is in a SAFE state!")
        print("Safe order to run processes:", ["P" + str(i + 1) for i in sequence])
    else:
        print("The system is NOT safe! Risk of deadlock.")
