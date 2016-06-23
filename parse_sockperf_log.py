import os
import os.path
import re
import sys
import result_parsor


def save_result_to_file(result, target):
    print "save result file"
    f = open(target, 'w')
    for time in result[1]:
        f.write(','.join(map(str, time)))
        f.write("\n")
    f.close()


def transfer_result_from_file(source, target):
    try:
        content = open(source).read()
        result = result_parsor.result_file_parse(content)
        print "get result from "+ source
    except IOError as e:
        print "I/O error({0}): {1}: {2}".format(e.errno, e.strerror, source)
        return
    save_result_to_file(result, target)
    return 0


def main():
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    transfer_result_from_file(source_file, target_file)


if __name__ == '__main__':
    main()
