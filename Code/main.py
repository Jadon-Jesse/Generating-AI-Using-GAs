# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 22:13:30 2017

@author: Jadon
"""
import pandas as pd
import numpy as np
import itertools
import math
import random
import matplotlib.pyplot as plt
import urllib
import pymysql
import time
from subprocess import Popen

import alpha_chargen
import hook
import parse_file
################################
#This script will run the show
#Takes in
#   -InitialPop : NUmber of individuals to randomly create
#   -NumGen: Number of generations to evolve over
#   -Ga Params



def expected_outcome(Rw,Rl):
    e = 1.0/(1+math.pow(10,((Rl - Rw)/400)))
    return e
    


def update_charsheet(winner, looser, i):
    df = list_df_gen[i]
    
    #if draw darN == draw darM match
    winsp = winner.split(" ")
    losp = looser.split(" ")
    
    if winsp[0] == losp[0]:
        print("Draw between {0} and {1}".format(winsp[1], losp[1]))
        
        
    else:
        #Update wins losses
        df.loc[df.loc[df.Name == winner].index,'Wins'] +=1
        df.loc[df.loc[df.Name == looser].index, 'Losses'] +=1
              
        #Update Total_Matches Played
        df.loc[df.loc[df.Name == winner].index,'Total_Matches'] +=1
        df.loc[df.loc[df.Name == looser].index,'Total_Matches'] +=1
            
        #Calculate new ELO Rating
        Ep1w = float(df[df.Name == winner].ELO)
        Ep2l = float(df[df.Name == looser].ELO)
        #P1 = Winner here
        Rp1 = Ep1w + 50.0*(1.0 - expected_outcome(Ep1w,Ep2l ))
        #P2 = Looser here
        Rp2 = Ep2l + 50.0*(0.0 - expected_outcome(Ep2l,Ep1w ))
         #Update ELO
        df.loc[df.loc[df.Name == winner].index,'ELO'] = Rp1
        df.loc[df.loc[df.Name == looser].index, 'ELO'] = Rp2
    
    
      
    list_df_gen[i] = df
    
def update_char_stats(char, win, los, drw, gen):
    df = list_df_stats[gen]
    
    
    df.loc[df.loc[df.Name == char].index,'Wins'] +=int(win)
    df.loc[df.loc[df.Name == char].index, 'Loses'] +=int(los)
    df.loc[df.loc[df.Name == char].index, 'Draws'] +=int(drw)     
    #Update Total_Matches Played
    
      
    list_df_stats[gen] = df

def round_robin(names, generation):
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
        winner = hook.fight(line_up[match][0], line_up[match][1])
        match_list.append(match)
        p1_list.append(line_up[match][0])
        p2_list.append(line_up[match][1])
        winner_list.append(winner)
        elo_list.append('1000')
        
        #Check who lost
        los=''
        if winner == line_up[match][0]:
            los = line_up[match][1]
        elif winner == line_up[match][1]:
            los = line_up[match][0]
            
        print("winner : {}".format(winner))
        print("loser : {}".format(los))
        #Update the char sheet
        update_charsheet(winner,los,generation)
        
        #print("Winner : "+winner)
    df_matches = pd.DataFrame({"MatchNo":match_list,"P1":p1_list,"P2":p2_list,"Winner":winner_list,"ELO":elo_list}, columns = ["MatchNo","P1","P2","Winner","ELO"])
    return df_matches


def build_cmds(round_list, gen):
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
                #Draw Game
                if "winningteam = 0\n" in line:
                    who_won = "0"
                    who_lost = "0"
                #TEam 1 Wins
                if "winningteam = 1\n" in line:
                    who_won = "1"
                    who_lost="2"
                #Team 2 wins
                if "winningteam = 2\n" in line:
                    who_won = "2"
                    who_lost = "1"
                #if draw then consider both as losses so elo stays same for them
                if who_won =="0" and who_lost =="0":
                    #append flags
                    #get both chars name
                    get_drwp1= "p1"+".name ="
                    if line.find(get_drwp1)==0:
                        drw_split = line.split('=')
                        draw = drw_split[-1]
                        name="draw "+str(draw.strip())
                        win_l.append(name)
                    get_drwp2= "p2"+".name ="    
                    if line.find(get_drwp2)==0:
                        drw_split = line.split('=')
                        draw = drw_split[-1]
                        name="draw "+str(draw.strip())
                        los_l.append(name)
                        
                #otherwise get winner and looser
                else:
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

    
def round_robin_parallel(names, generation):
    #generate round robbin list of player combinations
    line_up = list(itertools.combinations(names, 2))
    
    #get list of commands to parallelize
    commands, logs = build_cmds(line_up, generation)
    mugen_dir = 'C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/'
    
    # run in parallel
    processes = [Popen(cmd, shell=True, cwd = mugen_dir) for cmd in commands]
    # do other things here..
    print("doing stuff")
    # wait for completion
    for p in processes: 
        p.wait()
        
    #get ALL winners and losers from logs for that generation
    #winlist, loslist = get_winlos(logs)
    winlist,loslist = get_winlos(logs)
    

    #Update the char sheet in sequence
    for i in np.arange(len(winlist)):
        
        update_charsheet(winlist[i],loslist[i],generation)
        
        #print("Winner : "+winner)
   
#takes in an even length list of players and generate the ts match line up
def single_ts(players):
    #first shuffle the list
    
    gen = list()
    if len(players)==2:
        gen.append(players)
        return gen
    elif len(players) >2:
        shuffle = np.random.permutation(players).tolist()
    
        for i in np.arange(0,len(shuffle)-1,2):
            t =[shuffle[i],shuffle[i+1]]
            gen.append(t)
    return gen
    
#here were assuming our population is a power of 2
def single_elim_ts_parallel(names, generation):
    #for this generation we have to do the ts until we have an ultimate winner
    #We gotta loop over the tree height
    poptemp= names
    levels = int(math.log(len(names), 2))
    for i in np.arange(levels):
        
        line_up = single_ts(poptemp)
        print("line up")
        print(line_up)
        #get list of commands to parallelize
        commands, logs = build_cmds(line_up, generation)
        mugen_dir = 'C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/'
        
        # run in parallel
        processes = [Popen(cmd, shell=True, cwd = mugen_dir) for cmd in commands]
        # do other things here..
        print("doing stuff")
        # wait for completion
        for p in processes: 
            p.wait()
            
        #get ALL winners and losers from logs for that generation
        #winlist, loslist = get_winlos(logs)
        winlist,loslist = get_winlos(logs)
        poptemp=[]
    
        #Update the char sheet in sequence
        for i in np.arange(len(winlist)):
            poptemp.append(winlist[i])
            update_charsheet(winlist[i],loslist[i],generation)
    
    
    
    
    
    

elite_rate = 0.1
new_rate = 0.1
crossover_rate = 0.8

mutation_rate = 0.001

def tourn_sel(df):
    print(df)
    r = random.sample(range(0,len(df)),4)
    p1=""
    p2=""
    print(r)
    print(df.loc[r[0]].ELO)
    if df.loc[r[0]].ELO > df.loc[r[1]].ELO:
        p1 = df.loc[r[0]].Name
    if df.loc[r[0]].ELO < df.loc[r[1]].ELO:
        p1 = df.loc[r[1]].Name
    if df.loc[r[2]].ELO > df.loc[r[3]].ELO:
        p2 = df.loc[r[2]].Name
    if df.loc[r[2]].ELO < df.loc[r[3]].ELO:
        p2 = df.loc[r[3]].Name
    print(p1)               
    return p1, p2

def nu_gen(df,size,nextgen):
    children=[]
    # get elite individuals and addem to our new df 
    num_elite = int(math.ceil(elite_rate*size))
    
    #create new DF to hold the new population
    new_pop = []
    df_newPop = pd.DataFrame(columns=['Name','ELO','Wins','Losses','Total_Matches'])
    
    
    
    #Append the elite individuals with their exsisting ratings n stuff to the new pop
    df_newPop = df_newPop.append(df[0:num_elite])

    #Perform genertoc operation of crossover 
    #num of time to run loop
    num_fover = int(math.floor(crossover_rate * size))
    #make sure the number of children is a multiple of 2
    tloop=0
    if num_fover % 2==0:
        tloop = num_fover
    elif num_fover % 2 !=0:
        tloop = num_fover -1
    loop = int(tloop/2)
    for i in np.arange(loop):
        #choose parents possibly tournment selection later
        print("creating kids")
        #r = random.sample(range(0,len(df)),2)
        par1,par2 = tourn_sel(df)
        print("P1 {0}".format(par1))
        print("P2 {0}".format(par2))
        #par1 = df.loc[r[0]].Name
        #par2 = df.loc[r[1]].Name
        #generate their childrens moves
        child_amoves, child_bmoves = parse_file.create_children(par1,par2, 0.5)
        aid = str(i)+"a"
        bid = str(i)+"b"
        #spawn children
        aname = alpha_chargen.spawn_child(nextgen, child_amoves, aid)
        bname = alpha_chargen.spawn_child(nextgen, child_bmoves, bid)
        print("done")
        new_pop.append(aname)
        new_pop.append(bname)
        children.append(aname)
        children.append(bname)
        #create temp dfs
        winlos = 0
        elo = 1000
        matches = 0
        dfa = pd.DataFrame({'Name':[aname], 'ELO':[elo], 'Wins':[winlos], 'Losses':[winlos], 'Total_Matches':[matches]}, columns=['Name','ELO','Wins','Losses', 'Total_Matches'])
        dfb = pd.DataFrame({'Name':[bname], 'ELO':[elo], 'Wins':[winlos], 'Losses':[winlos], 'Total_Matches':[matches]}, columns=['Name','ELO','Wins','Losses', 'Total_Matches'])
        df_newPop = df_newPop.append(dfa, ignore_index=True)
        df_newPop = df_newPop.append(dfb, ignore_index=True)
     

    #now create new individiuals if necessary
    #....
    num_nu = size  - (num_elite + (tloop))
    if num_nu==0:
        print('No new individuals created')
    elif num_nu>0:
        for ind in np.arange(num_nu):
             name_nu = "dArwIn_G{0}_{1}".format(nextgen,ind)
             elo_nu = 1000
             winl = 0
             matches=0
             #create the new individual randomly
             alpha_chargen.spawn_randomly(name_nu)
             df_nu = pd.DataFrame({'Name':[name_nu], 'ELO':[elo_nu], 'Wins':[winl], 'Losses':[winl],'Total_Matches':[matches]}, columns=['Name','ELO','Wins','Losses','Total_Matches'])
             df_newPop = df_newPop.append(df_nu, ignore_index=True)
    
    print("generation "+str(nextgen)+" complete!")
    print("Num survived : {0} ".format(num_elite))
    print("New children : {0} ".format(num_fover))
    print("New Inds : {0} ".format(num_nu))
    
    return df_newPop, children
        
#Evolve locally using parallel sims
def evolve_std(num_generations, current_pop):
    for i in np.arange(num_generations):
        print("Generation : "+str(i))
        print("current pop")
        print(current_pop)
        #!!!MAke chars fight here using either rr or ts
        
        #fight chars in round robbin
        round_robin_parallel(current_pop, i)
        #m = round_robin(current_pop,i)
        
        #using TSE instead of RR 
        
        #single_elim_ts_parallel(current_pop, i)
        
        #Sort our current pupulation interms of ELO
        df_sorted = list_df_gen[i].sort_values('ELO', ascending = False)
        #print(df_sorted.head())
        #Get last elo
        v = df_sorted.iloc[-1].ELO
        ratio.append(v)
        #list_df_stats.append(assess_on_cloud(current_pop, i))
    
        #Only replace population if were not on the last generation
        if i < num_generations-1:        
            #hah! Get it?
            #Create the new generation
            new_pop, children = nu_gen(df_sorted, len(df_sorted),i+1)
            #replace current pop with new pop
            current_pop = new_pop.Name.tolist()
            #keep track
            list_df_gen.append(new_pop)
        #On last generation... do some stuff with the list of dfs
        elif i == num_generations-1:
            print("DONE!")
            plt.scatter(range(0,len(ratio)), ratio)
            plt.title("Lowest ELO per Generation")
            plt.xlabel("Generation")
            plt.ylabel("ELO")
            plt.show()
            
def update_gen_from_db(gen, expected_writes):
    # Open database connection
    db = pymysql.connect("jadonjes.heliohost.org","jadonjes_darwin","HackThisDB1","jadonjes_OUTCOME" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM MatchOutTBL WHERE generation = '{0}'".format(str(gen))
    try:
       # Execute the SQL command
       cursor.execute(sql)
       #make sure we got all the details before moving on
       while(cursor.rowcount != expected_writes):
           #sleep for 20 seconds
           print("Row Counts: "+str(cursor.rowcount))
           print("Expected: "+str(expected_writes))
           print("Sleeping for 20s")
           time.sleep(20)
           cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
          iden = row[0]
          genn = row[1]
          match = row[2]
          winner = row[3]
          looser = row[4]
          update_charsheet(winner,looser,gen)
          # Now print fetched result
          #print ("{0} {1} {2} {3} {4} \n".format(iden,genn,match, winner,looser))
    except:
       print ("Error: unable to fetch data")

def pull_stats_from_db(gen,expected_ch):
    df_stats = pd.DataFrame(columns=["Gen","Name","Wins","Loses","Draws"])
    # Open database connection
    db = pymysql.connect("jadonjes.heliohost.org","jadonjes_darwin","HackThisDB1","jadonjes_OUTCOME" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM GenStatsTBL WHERE generation = '{0}'".format(str(gen))
    try:
       # Execute the SQL command
       cursor.execute(sql)
       while(cursor.rowcount != expected_ch):
          #sleep for 20 seconds
          print("Row Counts(children): "+str(cursor.rowcount))
          print("Expected(children): "+str(expected_ch))
          print("Sleeping for 20s")
          time.sleep(20)
          cursor.execute(sql)
          print(cursor.rowcount)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
          iden = row[0]
          gener = row[1]
          name = row[2]
          win = row[3]
          lose = row[4]
          draw = row[5]
          df_stat_tmp = pd.DataFrame({"Gen":[gener], "Name":[name],"Wins":[win], "Loses":[lose], "Draws":[draw]},columns=["Gen","Name","Wins","Loses","Draws"])

          df_stats = df_stats.append(df_stat_tmp, ignore_index=True)
          # Now print fetched result
          #print ("{0} {1} {2} {3} {4} \n".format(iden,genn,match, winner,looser))
      
    except:
       print ("Error: unable to fetch data")  
    
    return df_stats 

#Evolve the population on the cloud
#for each generation we gen the list of matches to take place 
#Then we post that to our network load bal
#Once over we go collect the reults and update the char sheet
def evolve_on_cloud(num_generations, current_pop):
    for i in np.arange(num_generations):
        print("Generation : "+str(i))
        line_up = list(itertools.combinations(current_pop, 2))
        #Post each chars deets for each match
        for match in np.arange(len(line_up)):
            genn = i
            matchnu=match
            p1n = line_up[match][0]
            p1moves = parse_file.read_cmd(p1n)
            p1str = parse_file.to_str(p1moves)
            p2n = line_up[match][1]
            p2moves = parse_file.read_cmd(p2n)
            p2str = parse_file.to_str(p2moves)
            tags = "Evolve"

            data = urllib.parse.urlencode({"matchnum":matchnu,"gen":genn,"p1name":p1n , "p1moves":p1str, "p2name": p2n, "p2moves":p2str, "tag":tags})
            data = data.encode('utf-8')
            request = urllib.request.Request("http://104.197.115.172")
            
            # adding charset parameter to the Content-Type header.
            request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
            
            f = urllib.request.urlopen(request, data)
            print(f.read().decode('utf-8'))
        
        #after the matches are over we need to pull the reults for that generation
        #from the db
        #And just to make sure that all the simulations have completed well sleep for some time
        print("Wait for 45 seconds.")
        time.sleep(45)
        print("Updating char sheet...")
        #update the char sheet 
        update_gen_from_db(i)
        
        #Now just update relevent dfs and create new pop
        #Sort our current pupulation interms of ELO
        df_sorted = list_df_gen[i].sort_values('ELO', ascending = False)
        #print(df_sorted.head())
        #Get last elo
        v = df_sorted.iloc[-1].ELO
        ratio.append(v)
    
        #Only replace population if were not on the last generation
        if i < num_generations-1:        
            #hah! Get it?
            new_pop = nu_gen(df_sorted, len(df_sorted),i+1)
            #replace current pop with new pop
            current_pop = new_pop.Name.tolist()
            #keep track
            list_df_gen.append(new_pop)
        #On last generation... do some stuff with the list of dfs
        elif i == num_generations-1:
            print("DONE!")
            plt.scatter(range(0,len(ratio)), ratio)
            plt.title("Lowest ELO per Generation")
            plt.xlabel("Generation")
            plt.ylabel("ELO")
            plt.show()
        
        
def assess_winls(wins,loses, name):
    nwins = []
    nwins.append(wins.count(name))
    nlos = []
    nlos.append(loses.count(name))
    draw_str = "draw "+name
    ndraws = []
    ndraws.append(wins.count(draw_str))
    
    return nwins, nlos, ndraws


def get_child_names(names):
    children=[]
    for i in np.arange(len(names)):
        #check last letter of name
        if names[i][-1] == "a" or names[i][-1] == "b":
            children.append(names[i])
            
    if len(children)==0:
        #if no children then were probably in the first generation
        return names
    else:
        return children
    
def assess_names(pop,generation):
    #create df to hold eatch win los for each character
    #Easy, Medium, Hard
    test_list = ["kfm","Deadpool","evilken"]
    #2d list to hold generated fights
    ass_list = list()
    #The for each character in our list make them fight the each test char
    for i in np.arange(len(pop)): 
        #generate the vs list
        a = [[pop[i],test_list[x]] for x in range(len(test_list))]
        ass_list.append(a)
    return ass_list

def cloud_cast(line, cur_gen, tag):
    match =0
    #Post each chars deets for each match
    #after assess names we get back a 3d list [[["p1","easy"],[p1,med],..]]
    for char in np.arange(len(line)):
        #them for each of their test martches
        for char_sim in np.arange(len(line[char])):
            #then we post the details
            genn = cur_gen
            matchnu=str(match)
            p1n = line[char][char_sim][0]
            print(p1n)
            p1moves = parse_file.read_cmd(p1n)
            p1str = parse_file.to_str(p1moves)
            p2n = line[char][char_sim][1]
            #dont need to get  moves for p2
            p2str = p2n+ "moves" ##parse_file.to_str(p2moves)
            tags = tag
    
            data = urllib.parse.urlencode({"matchnum":matchnu,"gen":genn,"p1name":p1n , "p1moves":p1str, "p2name": p2n, "p2moves":p2str, "tag":tags})
            data = data.encode('utf-8')
            request = urllib.request.Request("http://104.197.115.172")
            
            # adding charset parameter to the Content-Type header.
            request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
            
            try:
                print("requesting simulation(exp)")
                f = urllib.request.urlopen(request, data)
                print(f.read().decode('utf-8'))
            except Exception as e:
                # Return code error (e.g. 404, 501, ...)
                # ...
                print(str(e))
                
            match+=1
            

def experiment_on_cloud(num_generations, current_pop):
    for i in np.arange(num_generations):
        #Go about normal shiaattt 
        #first evolve
        print("Generation : "+str(i))
        line_up = list(itertools.combinations(current_pop, 2))
        for match in np.arange(len(line_up)):
            genn = i
            matchnu=match
            p1n = line_up[match][0]
            p1moves = parse_file.read_cmd(p1n)
            p1str = parse_file.to_str(p1moves)
            p2n = line_up[match][1]
            p2moves = parse_file.read_cmd(p2n)
            p2str = parse_file.to_str(p2moves)
            tags = "Evolve"

            data = urllib.parse.urlencode({"matchnum":matchnu,"gen":genn,"p1name":p1n , "p1moves":p1str, "p2name": p2n, "p2moves":p2str, "tag":tags})
            data = data.encode('utf-8')
            request = urllib.request.Request("http://104.197.115.172")
            
            # adding charset parameter to the Content-Type header.
            request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
            
            #f = urllib.request.urlopen(request, data)
            #print(f.read().decode('utf-8'))

            try:
                print("requesting simulation")
                f = urllib.request.urlopen(request, data)
                print(f.read().decode('utf-8'))
            except Exception as e:
                # Return code error (e.g. 404, 501, ...)
                # ...
                print(str(e))

                
            
            
            
        #after the matches are over we need to pull the reults for that generation
        #from the db
        #And just to make sure that all the simulations have completed well sleep for some time
        print("Wait for 45 seconds.")
        time.sleep(45)
        print("Updating char sheet...")
        #update the char sheet 
        expected_sims_rr = int(sum(range(1,len(current_pop))))
        update_gen_from_db(i,expected_sims_rr)
        
        #Now just update relevent dfs and create new pop
        #Sort our current pupulation interms of ELO
        df_sorted = list_df_gen[i].sort_values('ELO', ascending = False)
        
        

        

        #Get last elo
        v = df_sorted.iloc[-1].ELO
        ratio.append(v)
    
        #Only replace population if were not on the last generation
        if i < num_generations-1:        
            #hah! Get it?
            new_pop,new_kids = nu_gen(df_sorted, len(df_sorted),i+1)
            print(new_kids)
            #replace current pop with new pop
            current_pop = new_pop.Name.tolist()
            
            #NOW assess the generations children/
            a_pop = assess_names(new_kids, i+1)
            #simulate on cloud
            cloud_cast(a_pop, i+1, "Experiment")
            #update the charstats
            print("Wait for 45 seconds.")
            time.sleep(45)
            print("Updating STATS sheet...")
            #each child vs easy med hard
            expected_pause = int(len(new_kids)*3)
            gen_stats = pull_stats_from_db(i+1, expected_pause)
            list_df_stats.append(gen_stats)
            
            #keep track
            list_df_gen.append(new_pop)
        #On last generation... do some stuff with the list of dfs
        elif i == num_generations-1:
            print("DONE!")
            plt.scatter(range(0,len(ratio)), ratio)
            plt.title("Lowest ELO per Generation")
            plt.xlabel("Generation")
            plt.ylabel("ELO")
            plt.show()

    

num_init_pop = 4
#Num generations to evolve initial pop for
num_generations = 4

#Holds character info over eneratuions
list_df_gen = []

#holds character assessment info over generations
list_df_stats = []



#Initial Population
init_pop, elo = alpha_chargen.initial_population(num_init_pop, 0)
#init_pop = ['dArwIn_G0_0']

#elo = [1000]

df_init = pd.DataFrame({'Name':init_pop, 'ELO':elo}, columns=['Name','ELO'])
df_init['Wins'] = 0
df_init['Losses'] = 0
df_init['Total_Matches']=0
   
list_df_gen.append(df_init)
ratio=[]


    

evolve_std(num_generations, init_pop)
#evolve_on_cloud(num_generations, init_pop)
#lst = assess_on_cloud(init_pop, 0)
#experiment_on_cloud(num_generations, init_pop)   
    
    
    
    
    
    