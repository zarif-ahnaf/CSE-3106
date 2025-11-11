from typing import List


def look_algorithm(
    requests: List[int], head_position: int, direction: str = "right"
) -> tuple[List[int], int]:
    if not requests:
        return [], 0

    left = sorted([r for r in requests if r < head_position], reverse=True)
    right = sorted([r for r in requests if r > head_position])

    seek_sequence = []
    total_seek = 0
    current = head_position

    if direction == "right":
        for track in right:
            seek_sequence.append(track)
            total_seek += abs(track - current)
            current = track
        for track in left:
            seek_sequence.append(track)
            total_seek += abs(track - current)
            current = track
    else:
        for track in left:
            seek_sequence.append(track)
            total_seek += abs(track - current)
            current = track
        for track in right:
            seek_sequence.append(track)
            total_seek += abs(track - current)
            current = track

    return seek_sequence, total_seek


if __name__ == "__main__":
    requests = [176, 79, 34, 60, 92, 11, 41, 114]
    head = 50
    direction = "right"

    sequence, distance = look_algorithm(requests, head, direction)
    print("LOOK Seek Sequence:", sequence)
    print("Total Seek Distance:", distance)
