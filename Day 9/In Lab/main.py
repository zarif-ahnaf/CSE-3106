from tabulate import tabulate


def print_state(processes, allocation, maximum, available, step_desc=""):
    """Print Allocation, Max, and Available using tabulate."""
    n = len(processes)
    m = len(available)
    resource_headers = [f"R{j}" for j in range(m)]

    # Prepare rows for Allocation and Max
    alloc_rows = [[f"P{i}"] + allocation[i] for i in range(n)]
    max_rows = [[f"P{i}"] + maximum[i] for i in range(n)]

    # Create tables
    alloc_table = tabulate(
        alloc_rows, headers=[" "] + resource_headers, tablefmt="grid"
    )
    max_table = tabulate(max_rows, headers=[" "] + resource_headers, tablefmt="grid")
    avail_table = tabulate([available], headers=resource_headers, tablefmt="grid")

    # Print with labels
    print("\n" + "=" * 60)
    if step_desc:
        print(step_desc)
    print("\nAllocation:")
    print(alloc_table)
    print("\nMax:")
    print(max_table)
    print("\nAvailable:")
    print(avail_table)
    print("=" * 60)


def bankers_algorithm(processes, allocation, maximum, available):
    n = len(processes)
    m = len(available)

    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work = available[:]
    finish = [False] * n
    safe_sequence = []

    print_state(processes, allocation, maximum, available, "Initial State")

    step = 1
    while len(safe_sequence) < n:
        found = False
        # Search in natural order
        for i in range(n):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(m)):
                    safe_sequence.append(processes[i])
                    finish[i] = True
                    for j in range(m):
                        work[j] += allocation[i][j]

                    print_state(
                        processes,
                        allocation,
                        maximum,
                        work,
                        f"Step {step}: Process P{processes[i]} finished. Resources released.",
                    )
                    step += 1
                    found = True
                    break
        if not found:
            print("\n❌ System is in an UNSAFE state! No safe sequence exists.")
            return None

    print(
        f"\n✅ System is in a SAFE state.\nSafe sequence: {' → '.join(f'P{p}' for p in safe_sequence)}"
    )
    return safe_sequence


def get_matrix_input(rows, cols, matrix_name):
    """Get matrix input from user with validation."""
    matrix = []
    print(f"\nEnter {matrix_name} Matrix ({rows} processes × {cols} resources):")
    for i in range(rows):
        while True:
            try:
                row = list(
                    map(int, input(f"P{i} (space-separated values): ").strip().split())
                )
                if len(row) != cols:
                    print(f"Error: Please enter exactly {cols} values for this row.")
                    continue
                if any(x < 0 for x in row):
                    print("Error: Resource values cannot be negative.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Error: Please enter valid integers only.")
    return matrix


def get_vector_input(length, vector_name):
    """Get vector input from user with validation."""
    while True:
        try:
            vector = list(
                map(
                    int,
                    input(
                        f"\nEnter {vector_name} ({length} resources, space-separated): "
                    )
                    .strip()
                    .split(),
                )
            )
            if len(vector) != length:
                print(f"Error: Please enter exactly {length} values.")
                continue
            if any(x < 0 for x in vector):
                print("Error: Resource values cannot be negative.")
                continue
            return vector
        except ValueError:
            print("Error: Please enter valid integers only.")


if __name__ == "__main__":
    print("===== Banker's Algorithm Implementation =====")

    # Get dimensions
    while True:
        try:
            n = int(input("\nEnter number of processes: "))
            if n <= 0:
                print("Error: Number of processes must be positive.")
                continue
            m = int(input("Enter number of resource types: "))
            if m <= 0:
                print("Error: Number of resource types must be positive.")
                continue
            break
        except ValueError:
            print("Error: Please enter valid integers only.")

    # Get matrices and vectors
    allocation = get_matrix_input(n, m, "Allocation")
    maximum = get_matrix_input(n, m, "Maximum")
    available = get_vector_input(m, "Available resources")

    # Create process list
    processes = list(range(n))

    print("\nBanker's Algorithm with Tabulated Output\n")
    bankers_algorithm(processes, allocation, maximum, available)
