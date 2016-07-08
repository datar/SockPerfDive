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
    with open(source) as infile, open(target, 'w') as outfile:
        summary = []
        for line_index in range(SOCKPERF_LOG_SUMMARY_LINE_NUMBER):
            summary.append(infile.readline().rstrip())


        # output file has header line
        outfile.write('tx,inner,net\n')
        last_rx_time = 0
        first_tx = 0

        for line in infile:
            if line.startswith(SOCKPERF_LOG_SECTION_SEP_BEGIN):
                break
            (tx_text, rx_text) = line.replace('.', '').strip('\n').split(',')
            rx = int(rx_text)
            tx = int(tx_text)
            if first_tx == 0:
                first_tx = tx
                last_rx_time = tx
            outfile.write("%d,%d,%d\n" % (tx-first_tx, tx-last_rx_time, rx-tx))
            last_rx_time = rx
    infile.close()
    outfile.close()
    return 0


def main():
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    if os.path.isdir(source_file):
        filenames = os.listdir(source_file)
    else:
        filenames = [source_file]
    for filename in filenames:
        (basename, extname) = os.path.splitext(filename)
        if extname.upper() != '.CSV':
            continue
        source_name = os.path.join(source_file, filename)
        target_name = os.path.join(target_file, filename)
        transfer_result_from_file(source_name, target_name)


if __name__ == '__main__':
    main()
