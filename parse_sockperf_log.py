import os
import os.path
import sys
from multiprocessing import Pool as Workers


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


def transfer_result_from_file(task):
    source = task[0]
    target = task[1]
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
        if not os.path.exists(target_file):
            os.makedirs(target_file, 0777)
    else:
        filenames = [source_file]

    tasks = []
    for filename in filenames:
        (basename, extname) = os.path.splitext(filename)
        if extname.upper() != '.CSV':
            continue
        source_name = os.path.join(source_file, filename)
        target_name = os.path.join(target_file, filename)
        tasks.append([source_name, target_name])

    works = Workers(5)
    works.map(transfer_result_from_file, tasks)
    works.close()
    works.join()


if __name__ == '__main__':
    main()
