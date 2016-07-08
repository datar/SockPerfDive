import time

cmdline_pattern = '%s chrt -f 97 sockperf pp -i 192.168.1.2 -p 5001 -m %d --sender-affinity 2 --receiver-affinity 3 -t %d --burst 1 --mps=max --full-log %s\n'
logfile_pattern = '/home/test/sockperf_log_%s_m%d_t%d_%s.csv'
time_str = time.strftime('%Y%m%d%H%M%S')
msgsizes = range(16,257,1)
time_duration = [60,10]
kernel_bypass = ['', 'onload --profile=latency']
cmdlines = []

for time_d in time_duration:
    for msgsize in msgsizes:
        for kb_lib in kernel_bypass:
            if len(kb_lib) < 5:
                l = 'none'
            else:
                l = 'onload'
            logfile = logfile_pattern % (time_str, msgsize, time_d, l)
            cmdline = cmdline_pattern % (kb_lib, msgsize, time_d, logfile)
            cmdlines.append(cmdline)

with open('test_batch.sh', 'w') as outfile:
    outfile.writelines(cmdlines)
outfile.close()
