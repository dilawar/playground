import zlib
import random
import string

def rand_string(N):
    alph = string.digits + ',.'
    st = random.choices(alph, k=N)
    return ''.join(st).encode('utf8')

def main():
    s = rand_string(1000000)
    p = zlib.compress(s, 4)
    print(len(s), len(p))

if __name__ == '__main__':
    main()
