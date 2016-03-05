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
SOCKPERF_MIN_LINE = 20


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


def save_file_result(result, result_id):
    target_content, summary = generate_result_list(result, result_id)
    f = open(result_id+'.csv', 'w')
    f.write(target_content)
    f.close()

    test_id = generate_test_id_from_str(result_id)
    s = open(target_dir+test_id+'.csv', 'a')
    s.write(summary)
    s.write(os.linesep)
    s.close()

def get_max_value_from_line(line):



def get_summary_from_file(filename):
    try:
        in_file = open(filename)
        lines = []
        for i in range(SOCKPERF_SUMMARY_LINE_NUMBER):
            lines.append(in_file.readline())
        result = dict()
        result['MAX'] = max(latency)
        result['MIN'] = min(latency)
        result['50'] = latency[l/2]
        result['99'] = latency[l*99/100]
        result['9999'] = latency[l*9999/10000]
    except IOError as e:
        print "I/O error({0}): {1}: {2}".format(e.errno, e.strerror, filename)
        return

    save_file_result(result, result_id)
    return 0


def main():
    parser = argparse.ArgumentParser(description='Create Performance Data')
    parser.add_argument('--dir_name', dest='dir_name', default="", help="Result Directory Name")
    args = parser.parse_args()
    source_dir_uri = args.dirname
    filenames = get_result_file_list(source_dir_uri)
    summary = []
    for filename in filenames:
        summary.append(get_summary_from_file(filename))


if __name__ == '__main__':
    main()
