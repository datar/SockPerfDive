import os.path
import sys
import csv
from multiprocessing import Pool as Workers

LATENCY_DATA_HEADER = 'tx,inner,net'
IN_LATENCY_DATA_HEADER = 'inner'
NET_LATENCY_DATA_HEADER = 'net'
IN_LATENCY_ZERO = '0'

INNER_HEADER = 'latency_in'
NET_HEADER = 'latency_net'
COUNT_HEADER = 'count'

INNER_LATENCY_MAP_HEADER = 'latency,count'
NETWORK_LATENCY_MAP_HEADER = 'latency,count'
USAGE = 'python generate_latency_map.py data_in_file inner_latency_out_file network_latency_out_file'


def transfer_latency_to_map(task):
    source = task[0]
    inner_latency_file = task[1]
    network_latency_file = task[2]
    in_lat_map = dict()
    net_lat_map = dict()
    with open(source, 'rb') as infile:
        data_reader = csv.reader(infile)

        for row in data_reader:
            in_lat_map[row[1]] = in_lat_map.get(row[1], 0) + 1
            net_lat_map[row[2]] = net_lat_map.get(row[2], 0) + 1

    with open(inner_latency_file, 'wb') as outfile_in_lat, open(network_latency_file, 'wb') as outfile_net_lat:
        data_in_writer = csv.writer(outfile_in_lat, quoting=csv.QUOTE_NONE)
        data_in_writer.writerow([INNER_HEADER, COUNT_HEADER])
        in_lat_map.pop(IN_LATENCY_DATA_HEADER, None)
        in_lat_map.pop(IN_LATENCY_ZERO, None)
        for k in in_lat_map.keys():
            data_in_writer.writerow([k, in_lat_map[k]])

        data_net_writer = csv.writer(outfile_net_lat, quoting=csv.QUOTE_NONE)
        data_net_writer.writerow([NET_HEADER, COUNT_HEADER])
        net_lat_map.pop(NET_LATENCY_DATA_HEADER, None)
        for k in net_lat_map.keys():
            data_net_writer.writerow([k, net_lat_map[k]])
    return 0


def main():
    if len(sys.argv) < 4:
        exit(USAGE)
    source_file = sys.argv[1]
    inner_latency_file = sys.argv[2]
    network_latency_file = sys.argv[3]

    source_file = os.path.normpath(source_file)
    inner_latency_file = os.path.normpath(inner_latency_file)
    tasks = []
    if os.path.isfile(source_file):
        tasks = [[source_file, inner_latency_file, network_latency_file]]
    else:
        if not os.path.exists(inner_latency_file):
            os.makedirs(inner_latency_file)
        if not os.path.exists(network_latency_file):
            os.makedirs(network_latency_file)
        filenames = os.listdir(source_file)
        for filename in filenames:
            source = os.path.join(source_file, filename)
            target_in = os.path.join(inner_latency_file, filename)
            target_net = os.path.join(network_latency_file, filename)
            tasks.append([source, target_in, target_net])
    works = Workers(10)
    works.map(transfer_latency_to_map, tasks)
    works.close()
    works.join()


if __name__ == '__main__':
    main()
