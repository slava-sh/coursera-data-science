import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper((sequence_id, nucleotides)):
    nucleotides = nucleotides[:-10]
    mr.emit_intermediate(nucleotides, None)


def reducer(nucleotides, _):
    mr.emit(nucleotides)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
