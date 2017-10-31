from subprocess import Popen
import numpy as np
import itertools



def getWinner(log):
    #filename = "matchout.txt"
    who_won =  "-1"
    winner="-1"
    with open(log) as f:
        for line in f:
            if "winningteam = 1\n" in line:
                who_won = "1"
            elif "winningteam = 2\n" in line:
                who_won = "2"
            get = "p"+str(who_won)+".name ="
            if line.find(get)==0:
                win_split = line.split('=')
                winner = win_split[-1]
                
    
    return winner.strip()

def get_winlos(logs):
    who_won =  "-1"
    who_lost ="-1"
    
    winner="-1"
    looser ="-1"

    win_l=[]
    los_l=[]
    
    for i in np.arange(len(logs)):
        file_quotes = logs[i]
        #strip oytter pair of quotes 
        file = file_quotes[1:-1]
        with open(file) as f:
            for line in f:
                if "winningteam = 1\n" in line:
                    who_won = "1"
                    who_lost="2"
                elif "winningteam = 2\n" in line:
                    who_won = "2"
                    who_lost = "1"
                    
                get_win = "p"+str(who_won)+".name ="
                get_los = "p"+str(who_lost)+".name ="
                if line.find(get_win)==0:
                    win_split = line.split('=')
                    winner = win_split[-1]
                    win_l.append(winner.strip())
                if line.find(get_los)==0:
                    los_split = line.split('=')
                    looser = los_split[-1]
                    los_l.append(looser.strip())
    return win_l, los_l

#commands = ['"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe" -log -p1 dArwIn_G0_0 -p2 kfm -p1.ai 1 -p2.ai 1 -rounds 1',
#            '"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe" -log -p1 dArwIn_G0_0 -p2 dArwIn_G0_1 -p1.ai 1 -p2.ai 1 -rounds 1']
#winners=[]
#names =[['dArwIn_G0_0','kfm'], ['dArwIn_G0_0','dArwIn_G0_1']]
#logs=['m1.txt','m2.txt']

def build_pll_cmds(round_list, gen):
    mugen_exe = '"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe"'
    num_rounds = 1
    logs=[]
    cmds = []
    for i in np.arange(len(round_list)):
        log_i =  '"C:/Users/Jadon/Work Space 4Y/RP/Code/Logs/G{0}_{1}.txt"'.format(gen,i)
        x = "{0} -log {1} -p1 {2} -p2 {3} -p1.ai 1 -p2.ai 1 -rounds {4} -nojoy -nosound".format(mugen_exe,log_i, round_list[i][0], round_list[i][1], num_rounds)
        cmds.append(x)
        logs.append(log_i)
    return cmds, logs


def fight(rounds, gen):
    #x = "{0} -log {1}-p1 {2} -p2 {3} -p1.ai 1 -p2.ai 1 -rounds {4}".format(mugen_exe,log, char_one, char_two, num_rounds)
    commands, logs = build_pll_cmds(rounds, gen)
    mugen_dir = 'C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/'
    # run in parallel
    processes = [Popen(cmd, shell=True, cwd = mugen_dir) for cmd in commands]
    # do other things here..
    print("doing stuff")
    # wait for completion
    for p in processes: 
        p.wait()
        
    #get winners and loser from logs for that generation
    #winlist, loslist = get_winlos(logs)
    winlist,loslist = get_winlos(logs)
    
    for i in np.arange(len(winlist)):
        print("winner : {0} Looser : {1}".format(winlist[i], loslist[i]))
    
    
if __name__ =="__main__":
    names =['dArwIn_G0_0', 'dArwIn_G0_1','dArwIn_G0_2', 'dArwIn_G0_3']
    line_up = list(itertools.combinations(names, 2))
    fight(line_up, 0)

