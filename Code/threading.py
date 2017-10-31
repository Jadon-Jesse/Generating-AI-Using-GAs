import time
import queue
import threading
import itertools
import numpy as np
names =  ['dArwIn_G0_0', 'dArwIn_G0_1','dArwIn_G0_2']


def fight(line_up, match):
    s = "Setting up match {0} between {1} and {2}".format(match,line_up[match][0], line_up[match][1])
    print(s)


def get_feed(q,res, i):
    m = q.get_nowait()
    fight(m,i)
    q.task_done()
    
if __name__ == "__main__":
    now = time.ctime()
    print("current "+now)
    results=[]
    feed_q = queue.Queue()
    round_list = list(itertools.combinations(names, 2))
    
    for match in np.arange(len(round_list)):
        feed_q.put(round_list[match])
        t = threading.Thread(target=get_feed, args=(feed_q, results, match))
        t.start()