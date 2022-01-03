import os
import sys
import time
from time import sleep
from csv import DictWriter
# import signal

# OUTPUT_FILE = 'default.json'

# def save_and_exit(sig, frame):
#     print(f"Saving to {OUTPUT_FILE}")

def process_and_save(output_path, stats):
    def process_line(l):
        t, data = l
        stat_line = [s for s in data.strip().split(' ') if ":" in s]
        # stat_line.append('time:%.6f' % t)
        # stat_line.append('ssthresh:0')
        # # stat_line.append('rtt_var:0')
        stat_line = [s.split(":") for s in stat_line]
        stat_line = {k[0]: k[1] for k in stat_line}
        
        # fix add other stats
        stat_line['time'] = "%.6f" % t
        if 'rtt' in stat_line:
            rtt_actual, rtt_var = stat_line['rtt'].split("/")
            stat_line['rtt'] = rtt_actual
            stat_line['rtt_var'] = rtt_var
        if 'ssthresh' not in stat_line:
            stat_line['ssthresh'] = 0
        return stat_line

    fieldnames = [
        'time',
        'rto',
        'rtt',
        'rtt_var',
        'mss',
        'pmtu',
        'rcvmss',
        'advmss',
        'cwnd',
        'ssthresh',
        'bytes_acked',
        'segs_out',
        'segs_in',
        'data_segs_out',
        'lastsnd',
        'lastrcv',
        'lastack',
        'rcv_ssthresh',
        'minrtt'
    ]

    stats = [process_line(x) for x in stats]
    # print(stats)
    with open(output_path, 'w') as f:
        writer = DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(stats)


def record_stats(sleep_time):
    stats = []
    while True:
        output = os.popen('ss -in dport == 8080 sport == 45000').readlines()
        if len(output) < 3:
            if len(stats) != 0:
                return stats
        else:
            stats.append((time.perf_counter(), output[2]))
        time.sleep(sleep_time/1000)
        # stat_line = [s for s in output[2].strip().split(' ') if ":" in s]


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 output_file interval_in_ms")
        sys.exit(0)
    
    output_path = sys.argv[1]
    sleep_time = float(sys.argv[2])
    print(f"Recording with interval of {sleep_time} and saving to {output_path}")

    res = record_stats(sleep_time)
    process_and_save(output_path, res)




if __name__ == "__main__":
    main()
    # s = 
