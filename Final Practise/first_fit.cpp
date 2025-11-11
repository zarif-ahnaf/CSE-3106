#include <iostream>
#include <vector>
#include <algorithm>

std::pair<std::vector<int>, std::vector<int>>
first_fit(const std::vector<int>& frame_block, const std::vector<int>& process_sizes) {
    std::vector<int> final_frames = frame_block; // copy
    std::vector<int> unallocated;

    for (int process : process_sizes) {
        bool allocated = false;
        for (size_t i = 0; i < final_frames.size(); ++i) {
            if (process <= final_frames[i]) {
                final_frames[i] -= process;
                allocated = true;
                break;
            }
        }
        if (!allocated) {
            unallocated.push_back(process);
        }
    }

    return std::make_pair(final_frames, unallocated);
}

int main() {
    std::vector<int> blocks = {100, 500, 200, 300, 600};
    std::vector<int> processes = {212, 417, 112, 426};

    auto [frames, unallocated] = first_fit(blocks, processes);

    // Print final_frames
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