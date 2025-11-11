# 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 0, 1, 7, 0, 1


def lru_page_replacement(frame_size, references):
    frames = []

    hit_list = []
    miss_list = []
    last_ref = {}

    for index, item in enumerate(references):
        last_ref[item] = index
        if item in frames:
            hit_list.append(item)
            continue

        if len(frames) < frame_size:
            frames.append(item)
        else:
            lru_page = min(frames, key=lambda p: last_ref.get(p, -1))
            frames[frames.index(lru_page)] = item
        miss_list.append(item)

    return frames, hit_list, miss_list


if __name__ == "__main__":
    f, h, m = lru_page_replacement(
        4, [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 0, 1, 7, 0, 1]
    )
    print(f)
    print(f"Hits: {len(h)}")
    print(f"Miss: {len(m)}")
