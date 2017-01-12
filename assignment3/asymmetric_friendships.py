import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper((person, friend)):
    key = tuple(sorted([person, friend]))
    mr.emit_intermediate(key, (person, friend))


def reducer(key, relationships):
    if len(relationships) != 1:
        return
    [(person, friend)] = relationships
    mr.emit((person, friend))
    mr.emit((friend, person))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
