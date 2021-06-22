import pandas as pd
import numpy as np 
from gnuplotter.plotter.plot2d import Plot, create_dataset
import sys

def plot(plot_data, outfilepath, underlays=[], return_dataset_only=False):
    
    datasets = []
    datasets.append(create_dataset(plot_data['time'], plot_data['cwnd'], with_='linespoints', axes='x1y1', title='cwnd'))
    datasets.append(create_dataset(plot_data['time'], plot_data['rtt'], with_='linespoints', axes='x1y2', title='rtt'))

    if not return_dataset_only:
        p = Plot("tcp_stats", outfilepath)
        
        for u in underlays:
            p.push_dataset(u)
        for d in datasets:
            p.push_dataset(d)
        
        cmds = ['set y2label "rtt(ms)"', 'set ytics nomirror', 'set y2tics 100', 'set key outside above']
        p.plot('', x_label='time', y_label='cwnd(mss)', custom_cmds=cmds)
    return datasets

def get_printable_name(addr):
    addr = addr.split(':')
    addr, port = ''.join(addr[:-1]), addr[-1]
    addr = addr.replace('[', '').replace(']', '').replace(':', '').replace('.', '_')
    
    return f"{addr}_{port}"
        

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input_file_path, output_folder_path")
        sys.exit(0)
    input_file = sys.argv[1]
    outfile_prefix = sys.argv[2]
    
    d = pd.read_csv(input_file, delimiter=',', names=['time', 'sender_addr', 'recvr_addr', 'curr_ret', 'total_ret', 'cwnd', 'ssthresh', 'rtt', 'min_rtt', 'data_segs_out', 'cc'])
    d = d.fillna(0)
    d['time'] -= d['time'].iloc[0]
    senders = pd.unique(d['sender_addr'])
    for addr in senders:
        sender_data = d[d.sender_addr.eq(addr)]
        recvr_addr = get_printable_name(sender_data['recvr_addr'].iloc[0])
        outfile_path = f"{outfile_prefix}/{get_printable_name(addr)}_{recvr_addr}"
        print(outfile_path)
        plot(sender_data, outfile_path)
        print(sender_data.shape)
        print(sender_data.head())
        print(f"Max CWND Achieved:{sender_data['cwnd'].max()}")

    # max_pause = d[d['lastsnd'] <= 2000]['lastsnd'].max()
    # min_rto = d['rto'].min()
    # # print(max_pause)
    
    # p = Plot("tcp_stats", "/Users/stariq/Documents/Research/CCMeasure/scripts/scripts_for_tcp_check/figs/")
    # p.create_and_push_dataset(d['time'], d['cwnd'], with_='linespoints ps 3 axis x1y1', title='cwnd')
    # p.create_and_push_dataset(d['time'], d['ssthresh'], with_='linespoints ps 3 axis x1y1', title='ssthresh')
    # p.create_and_push_dataset(d['time'], d['data_segs_out'], with_='linespoints ps 3 axis x1y2', title='data packets sent')
    # cmds = ['set y2label "data packets"', 'set y2range [0:8000]', 'set y2tics 1000', 'set ytics nomirror', 'set key outside above']
    # p.plot(input_file.split('.')[0], title=f"Max Pause: {int(max_pause)}ms, Min RTO: {min_rto}", x_label='time', y_label='mss', custom_cmds=cmds)
    

if __name__ == "__main__":
    main()
    # print(get_printable_name('[::ffff:127.0.0.1]:5201'))