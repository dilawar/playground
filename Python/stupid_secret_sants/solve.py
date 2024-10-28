import numpy as np
import random


def run():
    all_people = [f"p{i}" for i in range(0, 100)]
    leftover = list(all_people)

    pairs = dict()
    for p1 in all_people:
        p2 = random.choice(leftover)
        while p2 == p1:
            p2 = random.choice(leftover)
            if len(leftover) == 1:
                return -1
        # print(f"{p1} -- {p2}")
        # remove p2 from the list
        leftover.remove(p2)
        pairs[p1] = p2

    # count stupid couple
    total_pairs = 0
    for p1 in pairs:
        p2 = pairs[p1]
        if pairs[p2] == p1:
            print(f"Holy shit, {p1} <-> {p2}")
            total_pairs += 1

    return total_pairs


def main():
    runs = []
    for i in range(10000):
        print(i, 10000)
        n_pairs = run()
        if n_pairs >= 0:
            runs.append(n_pairs)
    print(runs)
    print(np.mean(runs))


if __name__ == "__main__":
    main()
