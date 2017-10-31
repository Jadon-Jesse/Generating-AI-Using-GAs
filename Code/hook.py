# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:17:58 2017

@author: Jadon
"""

import subprocess
import itertools
import numpy as np
import pandas as pd
#p = subprocess.Popen([command, argument1,...], cwd=working_directory)
#p.wait() 

def getWinner(c1,c2):
    filename = "matchout.txt"
    who_won =  "-1"
    winner="-1"
    with open(filename) as f:
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
    
    winner = getWinner(char_one,char_two)
    return winner
    

def fight_par(char_one, char_two, char3, char4):
    filename = "matchout.txt"
    num_rounds = "1"
    filename2 = "matchout2.txt"


    #-log matchstats.txt -p1 <p1_name> -p2 <p2_name> -p1.ai 1 -p2.ai 1 -rounds 1
    #Have to keep the quotes for the cmd 
    mugen_exe = '"C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/mugen.exe"'

    mugen_dir = "C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/"
    log1 = '"C:/Users/Jadon/Work Space 4Y/RP/Code/{0}"'.format(filename)
    log2 = '"C:/Users/Jadon/Work Space 4Y/RP/Code/{0}"'.format(filename2)
    x = "{0} -log {1}-p1 {2} -p2 {3} -p1.ai 1 -p2.ai 1 -rounds {4}".format(mugen_exe,log1, char_one, char_two, num_rounds)
    y = "{0} -log {1}-p1 {2} -p2 {3} -p1.ai 1 -p2.ai 1 -rounds {4}".format(mugen_exe,log2, char3, char4, num_rounds)
    commands=[]
    commands.append(x)
    commands.append(y)
    #print(x)
    #aparantly s.call automatically waits to finish
    p = [subprocess.call(cmd, cwd = mugen_dir ) for cmd in commands]
    
    winner = getWinner(char_one,char_two)
    # run in parallel
    
    # do other things here..
    # wait for completion
    return winner

def round_robin(names):
    #generate round robbin list of player combinations
    line_up = list(itertools.combinations(names, 2))
    match_list=[]
    p1_list=[]
    p2_list=[]
    winner_list=[]
    elo_list=[]
    #df_matches = pd.DataFrame({"MatchNo","P1","P2","Winner","ELO"}, columns = ["P1","P2","Winner","ELO"], index = "MatchNo" )
    for match in np.arange(len(line_up)):
        print("Setting up match {0} between {1} and {2}".format(match,line_up[match][0], line_up[match][1]))
        #line up the match between the fighters
        winner = fight(line_up[match][0], line_up[match][1])
        match_list.append(match)
        p1_list.append(line_up[match][0])
        p2_list.append(line_up[match][1])
        winner_list.append(winner)
        elo_list.append('10000')
        #print("Winner : "+winner)
    df_matches = pd.DataFrame({"MatchNo":match_list,"P1":p1_list,"P2":p2_list,"Winner":winner_list,"ELO":elo_list}, columns = ["MatchNo","P1","P2","Winner","ELO"])
    return df_matches


if __name__ == '__main__':
    #ckm ='Kung Fu Man'
    #m = 'kfm2'
    names = ["dArwIn_G4_0",
        "dArwIn_G9_0"]
    df = round_robin(names)
    print("Called directly from main")


