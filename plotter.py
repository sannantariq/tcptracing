import pandas as pd
import numpy as np 
from gnuplotter.plotter.plot2d import Plot
import sys

def main():
    input_file = 'remote_10_pause_500.csv'
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
    
    d = pd.read_csv(input_file, delimiter=',')
    d = d.fillna(0)
    d['time'] -= d['time'].iloc[0]

    max_pause = d[d['lastsnd'] <= 2000]['lastsnd'].max()
    min_rto = d['rto'].min()
    # print(max_pause)
    
    p = Plot("tcp_stats", "/Users/stariq/Documents/Research/CCMeasure/scripts/scripts_for_tcp_check/figs/")
    p.create_and_push_dataset(d['time'], d['cwnd'], with_='linespoints ps 3 axis x1y1', title='cwnd')
    p.create_and_push_dataset(d['time'], d['ssthresh'], with_='linespoints ps 3 axis x1y1', title='ssthresh')
    p.create_and_push_dataset(d['time'], d['data_segs_out'], with_='linespoints ps 3 axis x1y2', title='data packets sent')
    cmds = ['set y2label "data packets"', 'set y2range [0:8000]', 'set y2tics 1000', 'set ytics nomirror', 'set key outside above']
    p.plot(input_file.split('.')[0], title=f"Max Pause: {int(max_pause)}ms, Min RTO: {min_rto}", x_label='time', y_label='mss', custom_cmds=cmds)
    

if __name__ == "__main__":
    main()