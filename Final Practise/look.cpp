#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <tuple>

std::tuple<std::vector<int>, int>
look_algorithm(const std::vector<int>& requests, int head_position, const std::string& direction = "right") {
    if (requests.empty()) {
        return std::make_tuple(std::vector<int>(), 0);
    }

    std::vector<int> left, right;

    // Partition requests into left (< head) and right (> head)
    for (int r : requests) {
        if (r < head_position) {
            left.push_back(r);
        } else if (r > head_position) {
            right.push_back(r);
        }
        // Note: requests equal to head are ignored (no seek needed)
    }

    // Sort sublists
    std::sort(left.rbegin(), left.rend());   // descending
    std::sort(right.begin(), right.end());   // ascending

    std::vector<int> seek_sequence;
    int total_seek = 0;
    int current = head_position;

    if (direction == "right") {
        for (int track : right) {
            seek_sequence.push_back(track);
            total_seek += std::abs(track - current);
            current = track;
        }
        for (int track : left) {
            seek_sequence.push_back(track);
            total_seek += std::abs(track - current);
            current = track;
        }
    } else { // direction == "left"
        for (int track : left) {
            seek_sequence.push_back(track);
            total_seek += std::abs(track - current);
            current = track;
        }
        for (int track : right) {
            seek_sequence.push_back(track);
            total_seek += std::abs(track - current);
            current = track;
        }
    }

    return std::make_tuple(seek_sequence, total_seek);
}

int main() {
    std::vector<int> requests = {176, 79, 34, 60, 92, 11, 41, 114};
    int head = 50;
    std::string direction = "right";

    auto [sequence, distance] = look_algorithm(requests, head, direction);

    std::cout << "LOOK Seek Sequence: [";
    for (size_t i = 0; i < sequence.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << sequence[i];
    }
    std::cout << "]\n";

    std::cout << "Total Seek Distance: " << distance << "\n";

    return 0;
}