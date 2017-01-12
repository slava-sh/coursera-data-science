import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper(record):
    order_id = record[1]
    mr.emit_intermediate(order_id, record)


def reducer(order_id, records):
    orders = [record for record in records if record[0] == 'order']
    line_items = [record for record in records if record[0] == 'line_item']
    for order in orders:
        for line_item in line_items:
            mr.emit(order + line_item)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        mr.execute(f, mapper, reducer)
