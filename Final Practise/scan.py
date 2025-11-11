from typing import List, Tuple


def scan_seek_sequence(
    requests: List[int], head: int, disk_size: int, direction: str = "right"
) -> Tuple[List[int], int]:
    if not requests:
        return [], 0

    seen = set()
    unique_requests = []
    for r in requests:
        if r not in seen:
            unique_requests.append(r)
            seen.add(r)

    max_track = disk_size - 1
    if head < 0 or head > max_track:
        raise ValueError(f"Head position {head} is outside disk range [0, {max_track}]")
    if any(r < 0 or r > max_track for r in unique_requests):
        raise ValueError(f"All requests must be in range [0, {max_track}]")

    left = sorted([r for r in unique_requests if r < head], reverse=True)
    right = sorted([r for r in unique_requests if r > head])

    seek_sequence = []
    total_movement = 0
    current = head

    if direction == "right":
        for track in right:
            seek_sequence.append(track)
            total_movement += abs(track - current)
            current = track

        if right:
            total_movement += abs(max_track - current)
            current = max_track
        elif not left:
            pass
        else:
            total_movement += abs(max_track - current)
            current = max_track

        for track in left:
            seek_sequence.append(track)
            total_movement += abs(track - current)
            current = track

    elif direction == "left":
        for track in left:
            seek_sequence.append(track)
            total_movement += abs(track - current)
            current = track

        if left or right:
            total_movement += abs(0 - current)
            current = 0

        for track in right:
            seek_sequence.append(track)
            total_movement += abs(track - current)
            current = track

    else:
        raise ValueError("Direction must be 'left' or 'right'")

    return seek_sequence, total_movement


if __name__ == "__main__":
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    disk_size = 200

    seq_right, dist_right = scan_seek_sequence(requests, head, disk_size, "right")
    print("SCAN (-> right):")
    print("Seek sequence:", seq_right)
    print("Total head movement:", dist_right, "\n")
