import os
import re
import result_parsor


source_dir_uri = 'Z:\\Analysis\\20160302112700\\'


target_dir = 'Z:\\Analysis\\'


def get_result_file_list(dirpath):
    result_files = []
    for root, dirs, files in os.walk(dirpath):
        for filename in files:
            if filename.endswith('csv'):
                result_files.append(root+filename)
    return result_files


def generate_result_list(parse_result, result_id):
    msg_size = parse_result[0]['msg-size']
    times = parse_result[1]
    lines = []
    for time in times:
        lines.append(','.join([result_id, msg_size, ','.join(map(str, time))]))

    summary = msg_size + ',' + (','.join(map(str, parse_result[2])))
    return '\n'.join(lines), summary


def generate_sample_id_from_filename(filename):
    return re.search('\d{14}_\w{3}_m\d+', filename).group(0)


def generate_test_id_from_str(content):
    return re.search('\d{14}', content).group(0)


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


def get_result_from_file(filename):
    try:
        content = open(filename).read()
        result = result_parsor.result_file_parse(content)
    except IOError as e:
        print "I/O error({0}): {1}: {2}".format(e.errno, e.strerror, filename)
        return
    result_id = generate_sample_id_from_filename(filename)
    save_file_result(result, result_id)
    return 0


def main():
    filenames = get_result_file_list(source_dir_uri)
    for filename in filenames:
        get_result_from_file(filename)


if __name__ == '__main__':
    main()
