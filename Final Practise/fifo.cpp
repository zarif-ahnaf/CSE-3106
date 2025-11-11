#include <iostream>
#include <vector>
#include <deque>
#include <algorithm>

std::tuple<std::deque<int>, std::vector<int>, std::vector<int>>
fifo_page_replacement(int frame_size, const std::vector<int>& references) {
    std::deque<int> queue;
    std::vector<int> hit_list;
    std::vector<int> miss_list;

    for (int page : references) {
        // Check if page is already in the frame (hit)
        if (std::find(queue.begin(), queue.end(), page) != queue.end()) {
            hit_list.push_back(page);
            continue;
        }

        // Page fault (miss)
        if (static_cast<int>(queue.size()) < frame_size) {
            queue.push_back(page);
        } else {
            queue.pop_front();
            queue.push_back(page);
        }

        miss_list.push_back(page);
    }

    return std::make_tuple(queue, hit_list, miss_list);
}

int main() {
    std::vector<int> refs = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 1, 2, 0};
    auto [frames, hits, misses] = fifo_page_replacement(3, refs);

    // Print final frames
    std::cout << "[";
    for (size_t i = 0; i < frames.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << frames[i];
    }
    std::cout << "]\n";

    std::cout << "Hits: " << hits.size() << "\n";
    std::cout << "Miss: " << misses.size() << "\n";

    return 0;
}