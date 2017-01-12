import MapReduce
import sys

# A proper solution requires two MR steps. See
# https://www.coursera.org/learn/data-manipulation/discussions/all/threads/YXazUeLnEeWAzxJelNFrFw
MAX_N = 100

mr = MapReduce.MapReduce()


def mapper(record):
    (matrix, row, col, value) = record
    if matrix == 'a':
        for i in range(MAX_N):
            mr.emit_intermediate((row, i), (matrix, col, value))
    elif matrix == 'b':
        for i in range(MAX_N):
            mr.emit_intermediate((i, col), (matrix, row, value))


def reducer(key, records):
    a = {col: value for (matrix, col, value) in records if matrix == 'a'}
    b = {row: value for (matrix, row, value) in records if matrix == 'b'}
    value = sum(a[i] * b[i] for i in a.viewkeys() & b.viewkeys())
    if value:
        mr.emit(key + (value,))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
