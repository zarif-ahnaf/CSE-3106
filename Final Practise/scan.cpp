#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <stdexcept>
#include <cmath>
#include <tuple>

std::tuple<std::vector<int>, int>
scan_seek_sequence(
    const std::vector<int>& requests,
    int head,
    int disk_size,
    const std::string& direction = "right"
) {
    if (requests.empty()) {
        return std::make_tuple(std::vector<int>(), 0);
    }

    // Deduplicate while preserving order
    std::unordered_set<int> seen;
    std::vector<int> unique_requests;
    for (int r : requests) {
        if (seen.find(r) == seen.end()) {
            unique_requests.push_back(r);
            seen.insert(r);
        }
    }

    int max_track = disk_size - 1;

    // Validate head
    if (head < 0 || head > max_track) {
        throw std::invalid_argument(
            "Head position " + std::to_string(head) +
            " is outside disk range [0, " + std::to_string(max_track) + "]"
        );
    }

    // Validate all requests
    for (int r : unique_requests) {
        if (r < 0 || r > max_track) {
            throw std::invalid_argument(
                "All requests must be in range [0, " + std::to_string(max_track) + "]"
            );
        }
    }

    // Partition and sort
    std::vector<int> left, right;
    for (int r : unique_requests) {
        if (r < head) {
            left.push_back(r);
        } else if (r > head) {
            right.push_back(r);
        }
        // skip r == head (no movement needed)
    }

    std::sort(left.rbegin(), left.rend());   // descending
    std::sort(right.begin(), right.end());   // ascending

    std::vector<int> seek_sequence;
    int total_movement = 0;
    int current = head;

    if (direction == "right") {
        // Move toward max_track
        for (int track : right) {
            seek_sequence.push_back(track);
            total_movement += std::abs(track - current);
            current = track;
        }

        // Go to end of disk if there was any movement right OR if left exists
        if (!right.empty() || !left.empty()) {
            total_movement += std::abs(max_track - current);
            current = max_track;
        }

        // Now service left requests on the way back
        for (int track : left) {
            seek_sequence.push_back(track);
            total_movement += std::abs(track - current);
            current = track;
        }

    } else if (direction == "left") {
        // Move toward 0
        for (int track : left) {
            seek_sequence.push_back(track);
            total_movement += std::abs(track - current);
            current = track;
        }

        // Go to start of disk if there are any requests
        if (!left.empty() || !right.empty()) {
            total_movement += std::abs(0 - current);
            current = 0;
        }

        // Now service right requests
        for (int track : right) {
            seek_sequence.push_back(track);
            total_movement += std::abs(track - current);
            current = track;
        }

    } else {
        throw std::invalid_argument("Direction must be 'left' or 'right'");
    }

    return std::make_tuple(seek_sequence, total_movement);
}

int main() {
    std::vector<int> requests = {98, 183, 37, 122, 14, 124, 65, 67};
    int head = 53;
    int disk_size = 200;

    try {
        auto [seq_right, dist_right] = scan_seek_sequence(requests, head, disk_size, "right");

        std::cout << "SCAN (-> right):\n";
        std::cout << "Seek sequence: [";
        for (size_t i = 0; i < seq_right.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << seq_right[i];
        }
        std::cout << "]\n";
        std::cout << "Total head movement: " << dist_right << "\n\n";

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}