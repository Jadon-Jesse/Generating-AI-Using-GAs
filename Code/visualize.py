# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 00:12:03 2017

@author: Jadon
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from subprocess import Popen
import subprocess

def plot_avr_winlos_pgen(df):
    plt.figure()
    gens=df.Gen.unique()
    
    #get avr winlos per gen
    win_avr=[]
    los_avr=[]
    for gen in np.arange(len(gens)):
        win_avr.append(df.loc[df.Gen==gens[gen]].Wins.mean())
        los_avr.append(df.loc[df.Gen==gens[gen]].Loses.mean())
    plt.scatter(x=gens,y=win_avr, label='Average Wins',c="g")
    plt.scatter(x=gens,y=los_avr, label='Average Loss',c="r")
    plt.legend()
    plt.show()
    return win_avr, los_avr

def plot_winlos_reg(df):
    fig=plt.figure()
    gens=df.Gen.unique()
    
    #get avr winlos per gen
    win_avr=[]
    los_avr=[]
    for gen in np.arange(len(gens)):
        win_avr.append(df.loc[df.Gen==gens[gen]].Wins.mean())
        los_avr.append(df.loc[df.Gen==gens[gen]].Loses.mean())
    df_tmp = pd.DataFrame({'Gen':gens,'AvrWins':win_avr,'AvrLos':los_avr}, columns=['Gen','AvrWins','AvrLos'], index=gens)
    #plt.scatter(x=gens,y=win_avr, label='Average Wins',c="g")
    #plt.scatter(x=gens,y=los_avr, label='Average Loss',c="r")
    sns.regplot(x='Gen', y='AvrWins',data=df_tmp, label='AvrWins')
    sns.regplot(x='Gen', y='AvrLos',data=df_tmp, label='AvrLos')
    plt.title('Scatter Plot Showing Average Wins/Loss Per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Amount')
    plt.legend()
    plt.show()
    fig.savefig('scatter.png')
    return win_avr, los_avr,df_tmp

def assess_names(pop):
    #create df to hold eatch win los for each character
    #Easy, Medium, Hard
    test_list = ["evilken"]#["kfm","Deadpool","evilken"]
    #2d list to hold generated fights
    ass_list = []
    #The for each character in our list make them fight the each test char
    for i in np.arange(len(pop)): 
        #generate the vs list
        a = [[pop[i],test_list[x]] for x in range(len(test_list))]
        ass_list.append(a)
    return ass_list

def build_cmds_to_assess(round_list):
    mugen_exe = '"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe"'
    num_rounds = 1
    #logs=[]
    cmds = []
    match_no=0
    #for each child
    for i in np.arange(len(round_list)):
        #for each benchmark char
        for j in np.arange(len(round_list[i])):
            #log_i =  '"C:/Users/Jadon/Work Space 4Y/RP/Code/Logs/Ass_G{0}_{1}.txt"'.format(str(gen),str(match_no))
            x = "{0} -p1 {1} -p2 {2} -p1.ai 1 -p2.ai 1 -rounds {3} -nojoy -nosound".format(mugen_exe, round_list[i][j][0], round_list[i][j][1], num_rounds)
            cmds.append(x)
            #logs.append(log_i)
            match_no+=1
    return cmds

def assess_round_robin_parallel(commands):
    
    mugen_dir = 'C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/'
    
    # run in parallel
    processes = [Popen(cmd, shell=True, cwd = mugen_dir) for cmd in commands]
    # do other things here..
    print("doing stuff")
    # wait for completion
    for p in processes: 
        p.wait()
        
def fight(char_one, char_two):
    filename = "matchout.txt"
    num_rounds = "1"


    #-log matchstats.txt -p1 <p1_name> -p2 <p2_name> -p1.ai 1 -p2.ai 1 -rounds 1
    #Have to keep the quotes for the cmd 
    mugen_exe = '"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe"'

    mugen_dir = "C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/"
    log = '"C:/Users/Jadon/Work Space 4Y/RP/Code/{0}"'.format(filename)
    x = "{0} -log {1} -p1 {2} -p2 {3} -p1.ai 1 -p2.ai 1 -rounds {4} -nosound".format(mugen_exe,log, char_one, char_two, num_rounds)
    #print(x)
    #aparantly s.call automatically waits to finish
    p = subprocess.call(x, cwd = mugen_dir )
    
    #winner = getWinner(char_one,char_two)
    #return winner

file = 'Results/Out_100Gs.csv'

df_stats = pd.read_csv(file,usecols=['Gen','Name','Wins','Loses','Draws'] )
#w,l,t=plot_winlos_reg(df_stats)
pop=[]
#'dArwIn_G36_1a'
best='dArwIn_G57_3a'#df_stats.iloc[df_stats.loc[df_stats.Gen==62].Wins.argmax()].Name
worst='dArwIn_G1_2b'
pop.append(best)
#pop.append(worst)
ls = assess_names(pop)
cmds=build_cmds_to_assess(ls)
assess_round_robin_parallel(cmds)



