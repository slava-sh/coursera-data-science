import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper((document_id, text)):
    for token in text.split():
        mr.emit_intermediate(token, document_id)


def reducer(token, document_ids):
    document_ids = list(set(document_ids))
    mr.emit((token, document_ids))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
