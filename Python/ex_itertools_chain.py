import itertools


def gabbar():
    for i in range(3):
        yield f"gabbar-{i}"
    return "gabbar"


def kalia():
    for i in range(2):
        yield f"kalia-{i}"
    return "kalia"


chain1 = itertools.chain(gabbar(), kalia())
chain2 = itertools.chain(chain1, ["abc", "def"])

for i in chain1:
    print(1, i)

for i in chain2:
    print(2, i)
