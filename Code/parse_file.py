# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 19:35:05 2017

@author: Jadon
"""

#This script should act as the file parser
import numpy as np
import random



def moves_to_list(moves):
    move_list=[]
    new_move_flag = ";---------------------------------------------------------------------------\n"
    arg_list=[]
    for i in np.arange(len(moves)):
        #if we see a nre_move flag
        if moves[i] == new_move_flag:
            arg_list=[]
            move_list.append(arg_list)
        
        arg_list.append(moves[i])
    return move_list


#open and read cmd file into a list
def read_cmd(char_name):
    char_cmd = char_name+".cmd"

    dst = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/MUGEN/mugen-1.0/mugen/chars/"+char_name+"/"+char_cmd
    
    with open(dst) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #content = [x.strip() for x in content] 
    #slice from ai gen moves to the last 2 lines because we want to avoid the +++++++ line as that will mess things up when were permuting moves
    content = content[293:-2]
    #get into list
    moves = moves_to_list(content)
    return moves

#Takes in a male and female and returend 2 children:
#child1 using male as base then swaping triggers with female 50percdnt of the time
#child2 using female as baase""...
def cross_over(male, female, epsilon):
    child1 = []
    child2=[]
    male_moves = read_cmd(male)
    female_moves = read_cmd(female)
    
    #build up child1s moves using male as base
    for i in np.arange(len(male_moves)):
        ran = random.uniform(0,1)
        #set childs move at i to the males for now
        #child1.append(male_moves[i])
        cur_movem = male_moves[i]
        #If our random num is <50 then swap that move with the females move
        if ran< epsilon:
            #print(ran)
            #print(epsilon)
            #get the index of her move and set it to our cur move
            indef = -1
            for j in np.arange(len(female_moves)):
                if cur_movem[1] in female_moves[j][1]:
                    #print('found')
                    indef = j
                    cur_movem = female_moves[j]
                    break
        child1.append(cur_movem)
        
    #build up child2s moves using female as base
    for i in np.arange(len(female_moves)):
        ran = random.uniform(0,1)
        #set childs move at i to the female for now
        #child2.append(male_moves[i])
        cur_movef = female_moves[i]
        #If our random num is <50 then swap that move with the females move
        if ran< epsilon:
            #print(ran)
            #print(epsilon)
            #get the index of her move and set it to our cur move
            indef = -1
            for j in np.arange(len(male_moves)):
                if cur_movef[1] in male_moves[j][1]:
                    #print('found')
                    indef = j
                    cur_movef = male_moves[j]
                    break
        child2.append(cur_movef)
        
    #Randomize their respective moves\
    #child1 = np.random.permutation(child1).tolist()
    #child2 = np.random.permutation(child2).tolist()
    
    return child1, child2
    


def mutate(child):
    mu_rate = 0.03
    ran = random.uniform(0,1)
    if ran<mu_rate:
        random.shuffle(child)
        print("mutated")
    return child

def create_children(male, female, ep):
    
    bro,sis = cross_over(male,female,ep)
    bro_moves = mutate(bro)
    sis_moves = mutate(sis)
    
    return to_str(bro_moves), to_str(sis_moves)

def to_str(moveList):
    s = ""
    for i in np.arange(len(moveList)):
        s+=(''.join(moveList[i]))
    return s

def to_str_nospace(moveList):
    s = ''#"'
    for i in np.arange(len(moveList)):
        s+=(''.join(moveList[i]))
        s = s.replace(' ', ';space')
        s = s.replace('\n',';newline')
        s = s.replace('>',';gtrthan')
        s = s.replace('<',';lssthan')
    #s +='"'
    return s
    

if __name__ == '__main__':
    print("called directly")
    char1 = 'dArwIn_G0_1'
    #char2 = 'dArwIn_G0_2'
    
    bro =read_cmd(char1)
    li = to_str_nospace(bro)
    file = open("check2.txt","w")
    file.write(li)
    file.close
    #print(bro)
    #bro,sis = cross_over('dArwIn_G0_1','dArwIn_G0_2',0.5)
    #f = open('mm.txt','w')
    #f.write(to_str(bro))
    #f.close()
