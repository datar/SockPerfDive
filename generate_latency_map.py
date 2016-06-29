import sys
import csv

LATENCY_DATA_HEADER = 'tx,inner,net'
INNER_LATENCY_MAP_HEADER = 'latency,count'
NETWORK_LATENCY_MAP_HEADER = 'latency,count'
USAGE = 'python generate_latency_map.py data_in_file inner_latency_out_file network_latency_out_file'


def transfer_latency_to_map(source, inner_latency_file, network_latency_file):
    in_lat_map = dict()
    net_lat_map = dict()
    with open(source, 'rb') as infile:
        data_reader = csv.reader(infile)

        for row in data_reader:
            in_lat_map[row[1]] = in_lat_map.get(row[1], 0) + 1
            net_lat_map[row[2]] = net_lat_map.get(row[2], 0) + 1

    with open(inner_latency_file, 'wb') as outfile_in_lat, open(network_latency_file,'wb') as outfile_net_lat:
        data_in_writer = csv.writer(outfile_in_lat, quoting=csv.QUOTE_NONE)
        data_net_writer = csv.writer(outfile_net_lat, quoting=csv.QUOTE_NONE)
        for k in sorted(in_lat_map.keys()):
            data_in_writer.writerow([k, in_lat_map[k]])
        for k in sorted(net_lat_map.keys()):
            data_net_writer.writerow([k, net_lat_map[k]])
    return 0


def main():
    if len(sys.argv) < 4:
        exit(USAGE)
    source_file = sys.argv[1]
    inner_latency_file = sys.argv[2]
    network_latency_file = sys.argv[3]
    transfer_latency_to_map(source_file, inner_latency_file, network_latency_file)


if __name__ == '__main__':
    main()
