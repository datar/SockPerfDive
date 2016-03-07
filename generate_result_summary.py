import os
import re
import argparse
import result_parsor


SOCKPERF_SUMMARY_LINE_NUMBER = 20
SOCKPERF_PARAMETER_LINE = 1
SOCKPERF_LATENCY_LINE = 6
SOCKPERF_MAX_LINE = 9
SOCKPERF_9999_LINE = 10
SOCKPERF_99_LINE = 13
SOCKPERF_50_LINE = 17
SOCKPERF_MIN_LINE = 19


#test was performed using the following parameters: --mps=400 --burst=1 --reply-every=1 --msg-size=64 --time=10
#sockperf: [2;35m====> avg-lat=  1.403 (std-dev=0.677)[0m
#sockperf: ---> <MAX> observation =   42.337


def get_result_file_list(dirpath):
    result_files = []
    for root, dirs, files in os.walk(dirpath):
        for filename in files:
            if filename.endswith('csv'):
                result_files.append(root+filename)
    return result_files


def save_file_result(dirpath, result, result_id):
    filename = os.path.join(dirpath, 'summary.csv')
    s = open(filename, 'w')
    s.write(result)
    s.write(os.linesep)
    s.close()


def get_parameter_values_from_line(line):
    parameters = line.split(" --")[1:]
    res = dict([tuple(p.split("=")) for p in parameters])
    return res


def get_avg_sd_value_from_line(line):
    v = re.search('avg-lat=\s*([\d\.]+)\s+\(std\-dev=([\d\.]+)\)', line)
    if v:
        result = dict()
        result['AVG'] = v.group(1)
        result['SD'] = v.group(2)
    else:
        result = None
    return result


def get_latency_value_from_line(line):
    v = re.search('=\s*([\d\.]]+)', line)
    if v:
        return v.group(1)
    else:
        return None


def get_summary_from_file(filename):
    try:
        in_file = open(filename)
        lines = []
        for i in range(SOCKPERF_SUMMARY_LINE_NUMBER):
            lines.append(in_file.readline())
        result = dict()
        result.update(get_parameter_values_from_line(lines[SOCKPERF_PARAMETER_LINE]))
        result.update(get_avg_sd_value_from_line(lines[SOCKPERF_LATENCY_LINE]))
        result['MAX'] = get_latency_value_from_line(lines[SOCKPERF_MAX_LINE])
        result['MIN'] = get_latency_value_from_line(lines[SOCKPERF_MIN_LINE])
        result['50'] = get_latency_value_from_line(lines[SOCKPERF_50_LINE])
        result['99'] = get_latency_value_from_line(lines[SOCKPERF_99_LINE])
        result['9999'] = get_latency_value_from_line(lines[SOCKPERF_9999_LINE])
    except IOError as e:
        print "I/O error({0}): {1}: {2}".format(e.errno, e.strerror, filename)
        return
    return result


def main():
    parser = argparse.ArgumentParser(description='Create Performance Data')
    parser.add_argument('--dir_name', dest='dirname', default="", help="Result Directory Name")
    args = parser.parse_args()
    source_dir_uri = args.dirname
    filenames = get_result_file_list(source_dir_uri)
    summary = []
    for filename in filenames:
        summary.append(get_summary_from_file(filename))
    print summary


if __name__ == '__main__':
    main()
