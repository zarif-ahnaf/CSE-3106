# Input Block: 100,500,200,300,600
# Process sizes: 212,417,112,426
from copy import copy


def first_fit(frame_block, process_sizes):
    final_frames = copy(frame_block)
    unallocated = []

    for process in process_sizes:
        allocated = False
        for i in range(len(final_frames)):
            if process <= final_frames[i]:
                final_frames[i] -= process
                allocated = True
                break
        if not allocated:
            unallocated.append(process)

    return final_frames, unallocated


if __name__ == "__main__":
    f, m = first_fit([100, 500, 200, 300, 600], [212, 417, 112, 426])
    print(f)
    print(m)
