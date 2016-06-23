sockperf_log_section_seq = '------------------------------'


def parameter_str_parse(paramter_str):
    parameters = paramter_str.split(" --")[1:]
    res = dict([tuple(p.split("=")) for p in parameters])
    return res


def summery_parse(summary_str):
    pass


def data_str_parse(data_str):
    lines = data_str.replace('.', '').strip('\n').split('\n')
    items = [line.split(',') for line in lines]
    items.pop(0)
    start_time = int(items[0][0])
    times = []
    last_rtime = start_time
    for item in items:
        stime = int(item[0])
        rtime = int(item[1])
        times.append([stime-start_time, rtime-start_time, rtime-stime, stime-last_rtime])
        last_rtime = rtime
    return times


def first_step_analysis(latency):
    result = dict()
    result['MAX'] = max(latency)
    result['MIN'] = min(latency)
    latency.sort()
    l = len(latency)
    result['25'] = latency[l/4]
    result['MED'] = latency[l/2]
    result['75'] = latency[l*3/4]
    result['90'] = latency[l*9/10]
    result['99'] = latency[l*99/100]
    result['999'] = latency[l*999/1000]
    result['9999'] = latency[l*9999/10000]

    stat = [l, min(latency), latency[l/4], latency[l/2], latency[l*3/4], latency[l*9/10], latency[l*99/100],
            latency[l*999/1000], latency[l*9999/10000], max(latency)]
    return stat


def result_file_parse(file_content):
    sections = file_content.split(sockperf_log_section_seq)
    parameter_str = sections[1].rstrip()
    summary = sections[2].rstrip()
    data_str = sections[3].rstrip()
    parameters = parameter_str_parse(parameter_str)
    times = data_str_parse(data_str)
    latency = [x[2]/2 for x in times]
    #stat = first_step_analysis(latency)
    return parameters, times, None




