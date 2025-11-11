# 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 1, 2, 0
from collections import deque


def fifo_page_replacement(frame_size, references):
    queue = deque()

    hit_list = []
    miss_list = []
    for page in references:
        if page in queue:
            hit_list.append(page)
            continue

        if len(queue) < frame_size:
            queue.append(page)
        else:
            queue.popleft()
            queue.append(page)

        miss_list.append(page)

    return list(queue), hit_list, miss_list


if __name__ == "__main__":
    f, h, m = fifo_page_replacement(3, [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 1, 2, 0])
    print(f)
    print(f"Hits: {len(h)}")
    print(f"Miss: {len(m)}")
