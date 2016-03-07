import os
import re
import argparse


SOCKPERF_SUMMARY_LINE_NUMBER = 20
SOCKPERF_PARAMETER_LINE = 1
SOCKPERF_LATENCY_LINE = 6
SOCKPERF_MAX_LINE = 9
SOCKPERF_9999_LINE = 10
SOCKPERF_99_LINE = 13
SOCKPERF_50_LINE = 17
SOCKPERF_MIN_LINE = 19
SOCKPERF_RESULT_KEYS = ['FILE', 'MPS', 'MSG-SIZE', 'TIME', 'AVG', 'SD', 'MAX', '9999', '99', 'MEDIAN', 'MIN']


def cmp_sample(x, y):
    if x['MPS'] != y['MPS']:
        return cmp(int(x['MPS']), int(y['MPS']))
    if x['MSG-SIZE'] != y['MSG-SIZE']:
        return cmp(int(x['MSG-SIZE']), int(y['MSG-SIZE']))
    if x['TIME'] != y['TIME']:
        return cmp(int(x['TIME']), int(y['TIME']))
    return 0


def get_result_file_list(dirpath):
    result_files = []
    for root, dirs, files in os.walk(dirpath):
        for filename in files:
            if filename.endswith('csv') and not filename.startswith('summary'):
                result_files.append(os.path.join(root, filename))
    return result_files


def save_file_result(filename, result):
    s = open(filename, 'w')
    s.write(','.join(SOCKPERF_RESULT_KEYS))
    s.write(os.linesep)
    for summary in sorted(result, cmp=cmp_sample):
        items = []
        for k in SOCKPERF_RESULT_KEYS:
            items.append(summary[k])
        line = ','.join(items)
        s.write(line)
        s.write(os.linesep)
    s.close()


def get_parameter_values_from_line(line):
    result = {'MPS': None, 'MSG-SIZE': None, 'TIME': None}
    v = re.search('--mps=(.*?)\s+', line)
    if v:
        result['MPS'] = v.group(1)
    v = re.search('--msg-size=(.*?)\s+', line)
    if v:
        result['MSG-SIZE'] = v.group(1)
    v = re.search('--time=(.*?)\s+', line)
    if v:
        result['TIME'] = v.group(1)
    return result


def get_avg_sd_value_from_line(line):
    v = re.search('avg-lat=\s*([\d\.]+)\s+\(std-dev=([\d\.]+)\)', line)
    if v:
        result = dict()
        result['AVG'] = v.group(1)
        result['SD'] = v.group(2)
    else:
        result = dict()
        result['AVG'] = None
        result['SD'] = None
    return result


def get_latency_value_from_line(line):
    v = re.search('=\s*([\d\.]+)', line)
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
        result['MEDIAN'] = get_latency_value_from_line(lines[SOCKPERF_50_LINE])
        result['99'] = get_latency_value_from_line(lines[SOCKPERF_99_LINE])
        result['9999'] = get_latency_value_from_line(lines[SOCKPERF_9999_LINE])
        result['FILE'] = os.path.basename(filename)
        for k in SOCKPERF_RESULT_KEYS:
            if result[k] is None:
                print "CANNOT_GET_%s_FROM_FILE:%s" % (k, filename)
                result = None
                break
    except IOError as e:
        print "I/O error({0}): {1}: {2}".format(e.errno, e.strerror, filename)
        return
    return result


def main():
    parser = argparse.ArgumentParser(description='Generate a Summary of Performance Data')
    parser.add_argument('--dir_name', dest='dirname', default="", help="Test Result Directory Name")
    args = parser.parse_args()
    source_dir_uri = args.dirname
    summary = []
    for filename in get_result_file_list(source_dir_uri):
        s = get_summary_from_file(filename)
        if s is None:
            continue
        summary.append(s)
    filename = os.path.join(source_dir_uri, 'summary.csv')
    save_file_result(filename, summary)


if __name__ == '__main__':
    main()
