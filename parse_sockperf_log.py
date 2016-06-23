import os
import os.path
import re
import sys
import result_parsor


BEGIN_TEXT_OF_DATA = 'txTime, rxTime'
SOCKPERF_LOG_SECTION_SEP = '------------------------------'
SOCKPERF_LOG_SECTION_SEP_BEGIN = '-'
SOCKPERF_LOG_SUMMARY_LINE_NUMBER = 22


def save_result_to_file(result, target):
    print "save result file"
    f = open(target, 'w')
    for time in result[1]:
        f.write(','.join(map(str, time)))
        f.write("\n")
    f.close()


def transfer_result_from_file(source, target):
    with open(source) as infile, open(target) as outfile:
        summary = []
        for line_index in range(SOCKPERF_LOG_SUMMARY_LINE_NUMBER):
            summary.append(infile.readline().rstrip())

        last_rx_time = 0
        for line in infile:
            if line.startswith(SOCKPERF_LOG_SECTION_SEP_BEGIN):
                break
            (rx_text, tx_text) = line.replace('.', '').strip('\n').split(',')
            rx = int(rx_text)
            tx = int(tx_text)

            outfile.write("%d,%d\n" % (tx-rx, tx - last_rx_time))
    infile.close()
    outfile.close()
    return 0


def main():
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    transfer_result_from_file(source_file, target_file)


if __name__ == '__main__':
    main()