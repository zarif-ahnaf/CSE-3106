#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <tuple>

std::tuple<std::vector<int>, std::vector<int>, std::vector<int>>
lru_page_replacement(int frame_size, const std::vector<int>& references) {
    std::vector<int> frames;
    std::vector<int> hit_list;
    std::vector<int> miss_list;
    std::unordered_map<int, int> last_ref; // page -> last access index

    for (size_t index = 0; index < references.size(); ++index) {
        int item = references[index];
        last_ref[item] = static_cast<int>(index);

        // Check if page is already in frames (hit)
        auto it = std::find(frames.begin(), frames.end(), item);
        if (it != frames.end()) {
            hit_list.push_back(item);
            continue;
        }

        // Page fault (miss)
        if (static_cast<int>(frames.size()) < frame_size) {
            frames.push_back(item);
        } else {
            // Find LRU page: the one with smallest last_ref value
            int lru_page = frames[0];
            int lru_time = last_ref[frames[0]];

            for (int page : frames) {
                int ref_time = last_ref[page];
                if (ref_time < lru_time) {
                    lru_time = ref_time;
                    lru_page = page;
                }
            }

            // Replace LRU page
            auto replace_it = std::find(frames.begin(), frames.end(), lru_page);
            *replace_it = item;
        }

        miss_list.push_back(item);
    }

    return std::make_tuple(frames, hit_list, miss_list);
}

int main() {
    std::vector<int> refs = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 0, 1, 7, 0, 1};
    auto [frames, hits, misses] = lru_page_replacement(4, refs);

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