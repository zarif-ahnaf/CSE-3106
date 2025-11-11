#include <iostream>
#include <vector>
#include <string>

std::pair<bool, std::vector<int>> is_system_safe(
    const std::vector<int>& available,
    const std::vector<std::vector<int>>& max_need,
    const std::vector<std::vector<int>>& allocated
) {
    const int num_processes = static_cast<int>(allocated.size());
    const int num_resources = static_cast<int>(available.size());

    // Step 1: Calculate Need matrix
    std::vector<std::vector<int>> need(num_processes, std::vector<int>(num_resources));
    for (int i = 0; i < num_processes; ++i) {
        for (int j = 0; j < num_resources; ++j) {
            need[i][j] = max_need[i][j] - allocated[i][j];
        }
    }

    // Step 2: Prepare for safety check
    std::vector<int> work = available; // Copy of available resources
    std::vector<bool> finished(num_processes, false);
    std::vector<int> safe_order;

    // Step 3: Try to find a safe sequence
    while (static_cast<int>(safe_order.size()) < num_processes) {
        bool found_a_process = false;

        for (int pid = 0; pid < num_processes; ++pid) {
            // Skip if already finished
            if (finished[pid]) {
                std::cout << "P" << pid << ": Already Executed\n";
                continue;
            }

            // Check if this process can get all it needs
            bool can_run = true;
            for (int r = 0; r < num_resources; ++r) {
                if (need[pid][r] > work[r]) {
                    can_run = false;
                    break;
                }
            }

            if (!can_run) {
                std::cout << "P" << pid << ": The condition is false\n";
            }

            // If yes, pretend it runs and finishes
            if (can_run) {
                // It releases its resources when done
                for (int r = 0; r < num_resources; ++r) {
                    work[r] += allocated[pid][r];
                }

                finished[pid] = true;
                safe_order.push_back(pid);
                found_a_process = true;
            }
        }

        // If no process can run, we're stuck → unsafe!
        if (!found_a_process) {
            return {false, {}};
        }
    }

    return {true, safe_order};
}

// -------------------------------
// Example: Easy to understand
// -------------------------------
int main() {
    // There are 4 types of resources
    std::vector<int> available = {4, 3, 4, 2};

    // Max resources each process might need
    std::vector<std::vector<int>> max_need = {
        {5, 2, 4, 4},
        {4, 2, 6, 2},
        {2, 3, 1, 7},
        {2, 5, 3, 4}
    };

    // Resources already given to each process
    std::vector<std::vector<int>> allocated = {
        {2, 1, 1, 1},
        {3, 2, 2, 1},
        {2, 1, 1, 2},
        {1, 4, 3, 1}
    };

    // Run the safety check
    auto [safe, sequence] = is_system_safe(available, max_need, allocated);

    if (safe) {
        std::cout << "The system is in a SAFE state!\n";
        std::cout << "Safe order to run processes: ";
        for (size_t i = 0; i < sequence.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << "P" << (sequence[i] + 1);
        }
        std::cout << "\n";
    } else {
        std::cout << "The system is NOT safe! Risk of deadlock.\n";
    }

    return 0;
}