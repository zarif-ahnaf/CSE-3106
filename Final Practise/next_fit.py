# Input Block: 100,500,200,300,600
# Process sizes: 212,417,112,426
from copy import copy


def next_fit(frame_block, process_sizes):
    final_frames = copy(frame_block)
    unallocated = []
    n = len(final_frames)
    last_index = 0

    for process in process_sizes:
        allocated = False
        start = last_index
        while True:
            if process <= final_frames[last_index]:
                final_frames[last_index] -= process
                last_index = (last_index + 1) % n
                allocated = True
                break

            last_index = (last_index + 1) % n
            if last_index == start:
                break
        if not allocated:
            unallocated.append(process)
            last_index = start

    return final_frames, unallocated


if __name__ == "__main__":
    f, m = next_fit([100, 500, 200, 300, 600], [212, 417, 112, 426])
    print(f)
    print(m)
