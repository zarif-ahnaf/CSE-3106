#include <iostream>
#include <vector>
#include <tuple>

std::pair<std::vector<int>, std::vector<int>>
next_fit(const std::vector<int>& frame_block, const std::vector<int>& process_sizes) {
    std::vector<int> final_frames = frame_block; // copy
    std::vector<int> unallocated;
    int n = static_cast<int>(final_frames.size());
    int last_index = 0;

    for (int process : process_sizes) {
        bool allocated = false;
        int start = last_index;

        do {
            if (process <= final_frames[last_index]) {
                final_frames[last_index] -= process;
                last_index = (last_index + 1) % n;
                allocated = true;
                break;
            }
            last_index = (last_index + 1) % n;
        } while (last_index != start);

        if (!allocated) {
            unallocated.push_back(process);
            last_index = start; // reset to start position as in Python
        }
    }

    return std::make_pair(final_frames, unallocated);
}

int main() {
    std::vector<int> blocks = {100, 500, 200, 300, 600};
    std::vector<int> processes = {212, 417, 112, 426};

    auto [frames, unallocated] = next_fit(blocks, processes);

    // Print final frames
    std::cout << "[";
    for (size_t i = 0; i < frames.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << frames[i];
    }
    std::cout << "]\n";

    // Print unallocated
    std::cout << "[";
    for (size_t i = 0; i < unallocated.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << unallocated[i];
    }
    std::cout << "]\n";

    return 0;
}