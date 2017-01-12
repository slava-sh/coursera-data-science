import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper((person, friend)):
    mr.emit_intermediate(person, friend)


def reducer(person, friends):
    mr.emit((person, len(friends)))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
