# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 18:43:26 2017

@author: Jadon
"""
import numpy as np
import random
import shutil
import jinja2 as jin


move_list = ['1_Smash Kung Fu Upper.txt',
             '2_Triple Kung Fu Palm.txt',
             '3_Fast Kung Fu Knee.txt',
             '4_Light Kung Fu Knee.txt',
             '5_Strong Kung Fu Knee.txt',
             '6_Fast Kung Fu Palm.txt',
             '7_Light Kung Fu Palm.txt',
             '8_Strong Kung Fu Palm.txt',
             '9_Fast Kung Fu Upper.txt',
             '10_Light Kung Fu Upper.txt',
             '11_Strong Kung Fu Upper.txt',
             '12_Fast Kung Fu Blow.txt',
             '13_Light Kung Fu Blow.txt',
             '14_Strong Kung Fu Blow.txt',
             '15_High Kung Fu Blocking.txt',
             '16_High Kung Fu Blocking Low.txt',
             '17_High Kung Fu Blocking Air.txt',
             '18_Jump Strong Kick.txt', #Theres only 36 Moves made a mistake
             '19_Far Kung Fu Zankou.txt',
             '20_Light Kung Fu Zankou.txt',
             '21_Strong Kung Fu Zankou.txt',
             '22_Run Fwd.txt',
             '23_Run Back.txt',
             '24_Kung Fu Throw.txt',
             '25_Stand Light Punch.txt',
             '26_Stand Strong Punch.txt',
             '27_Stand Light Kick.txt',
             '28_Standing Strong Kick.txt',
             '29_Taunt.txt',
             '30_Crouching Light Punch.txt',
             '31_Crouching Strong Punch.txt',
             '32_Crouching Light Kick.txt',
             '33_Crouching Strong Kick.txt',
             '34_Jump Light Punch.txt',
             '35_Jump Strong Punch.txt',
             '36_Jump Light Kick.txt',
             ]

trigger_list = ['P2BodyDist x ',
                'P2BodyDist y ',
                'InGuardDist ',
                'P2MoveType ',
                'P2StateType ',
                'MoveContact ',
                'MoveGuarded ']

trigger_args = {0:['>= 0', '< 30', '< 120'],
                1:['< -30', '> 10', '> 60'],
                2:['= 0', '= 1'],
                3:['= A', '= I', '= H'],# '!= A', '!= I', '!= H'],
                4:['= S', '= C', '= A'],# '!= S', '!= C', '!= A'],
                5:['= 0 ','!= 0'],
                6:['= 0', '!= 0']}



#create new dir in Mugen/chars to store new character
def copy_kfmb_chars(char_name):
    src = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/Code/CharTemplate/kfmBlank/"
    dst = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/MUGEN/mugen-1.0/mugen/chars/"+char_name
    
    #copy all contents from kfm blank into new folder
    shutil.copytree(src,dst)
    

def ran_inbounds(siz):
    r = random.randint(0,siz)
    return r

def triggerSelect(move):
    #we need to start generatinig 'random numbers'
    
    #first we need a number between 1 and 4 to set the num of trigger inputs
    num_triggers= random.randrange(1,5)

    #print(num_triggers)
    
    string_to_append=''
    
    
    #now generate 3 random numbers between 0 and num_triggers
    #to select the logic for the trigger inputs
    lucky_choice = random.sample(range(0,len(trigger_list)), num_triggers )
    #print(lucky_choice)
    
    #loop through num trigger inputs to assign their logic
    for i in np.arange(num_triggers):
        r = random.randrange(0,len(trigger_args[lucky_choice[i]]))
        #print(r)
        trig_str = 'trigger1 = ' + str(trigger_list[lucky_choice[i]]) + str(trigger_args[lucky_choice[i]][r]) + '\n' 
        string_to_append += str(trig_str)
    
    
    fin = move + string_to_append + "\n"
    
    return fin
    

#This function will generate random trigger logic each time its called.
#Also randomizes the order of the triggers and their arguments
#Returns long string of moves and triggers for a character

#Its also now defines and returns the chars move sequence in terms of the
#base sequence ie. move_list
def generate_move_list():
    move_seq=[]
    final_string = ''
    direc = 'CharTemplate/MoveList/'
    #now loop through all moves and build them up randomly
    #char_name = 'alpha_v3.cmd'
    #char_gen = open(char_name, 'w')
    
    #generate a random permutation of the movelist
    #Which will define this chars strategy
    perm_moves = np.random.permutation(move_list)
    
    
    for i in np.arange(len(move_list)):
        
        #Lets get the move sequence as an integer
        move_ind = int(perm_moves[i].split('_')[0])
        #and append to move_seq list
        move_seq.append(move_ind)
    
       
        #print(perm_moves[i])
        loc = direc + perm_moves[i]
        move_i = open(loc, 'r')
        #print(move_i.read())
        
        #Now lets build up the triggers
        move_with_triggers = triggerSelect(move_i.read())
        
        
        #char_gen.write(move_with_triggers)
        final_string+=move_with_triggers
        #Close that specific moves file
        #ove_i.close()
        
    return final_string, move_seq
    #Close the generated cmd file
    #char_gen.close()
    #dont really need a seperate file

#####################################################
#This part will contain the code needed to create the caracter

dAI_dir = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/Code/dArwIn/"
dAI_req_dir = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/Code/dArwIn/required/"



char_dest = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/MUGEN/mugen-1.0/mugen/chars/"

    
    
def replace(filename):
    shutil.move("select_temp.def", "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/MUGEN/mugen-1.0/mugen/data/select.def")

def temp(txt):
    filename = "select_temp.def"
    with open(filename, 'w') as f:
         f.writelines(txt)
         
    replace(filename)


def add_char_to_list(char_name):
    filename = "C:/Users/Jadon/Work Space 4Y/Final Research Project/Generating-AI-Using-GAs/MUGEN/mugen-1.0/mugen/data/select.def"
    with open(filename, 'r') as f:
        text = f.readlines()
        text.insert(72, char_name+' \n')
        temp(text)
        




#This function will take in a char name and movestring
# It uses name to read and copy the files required (kfmBlank) to the char destination
#Then it 'injects' the move string to kfm.cmd template to generate a random ai
#Then it calls add char to list which essentially enters that character into the game
#we return the characters sequence list
def spawn_randomly(name):
    #copies required files to mugen/char/dArwIn_G...
    dst = char_dest+name+"/"
    src =dAI_req_dir
    shutil.copytree(src, dst)
    
    #now generate the template and store in that directory
    kfm_cmd_tmp = "kfm.cmd"
    
    env_cmd = jin.Environment(loader=jin.FileSystemLoader(dAI_dir))
    template = env_cmd.get_template(kfm_cmd_tmp)
    
    #declare pointer to the ai name
    to_filepath = char_dest+name+"/"+name+".cmd"
    move_list, seq_list = generate_move_list()
    file = open(to_filepath,'w')
    file.write(template.render(ai=move_list))
#print(template.render(name='West',bur='TOO'))
    file.close()
    
    kfm_def_tmp = "kfm.def"
    
    env_def = jin.Environment(loader=jin.FileSystemLoader(dAI_dir))
    template = env_def.get_template(kfm_def_tmp)
    
    #declare pointer to the ai name
    to_filepathd = char_dest+name+"/"+name+".def"

    file2 = open(to_filepathd,'w')
    file2.write(template.render(char_name=name, display_name = name, cmd = name))

    file2.close()
    
    add_char_to_list(name)
    return seq_list
    
#Spawn children with already defined move list
#instead of name take in generation
#and just generate the name here
def spawn_child(gen, moves, iden):
    name = "dArwIn_G{0}_{1}".format(gen,iden)
    #copies required files to mugen/char/dArwIn_G...
    dst = char_dest+name+"/"
    src =dAI_req_dir
    shutil.copytree(src, dst)
    
    #now generate the template and store in that directory
    kfm_cmd_tmp = "kfm.cmd"
    
    env_cmd = jin.Environment(loader=jin.FileSystemLoader(dAI_dir))
    template = env_cmd.get_template(kfm_cmd_tmp)
    
    #declare pointer to the ai name
    to_filepath = char_dest+name+"/"+name+".cmd"
    move_list = moves############################################
    file = open(to_filepath,'w')
    file.write(template.render(ai=move_list))
#print(template.render(name='West',bur='TOO'))
    file.close()
    
    kfm_def_tmp = "kfm.def"
    
    env_def = jin.Environment(loader=jin.FileSystemLoader(dAI_dir))
    template = env_def.get_template(kfm_def_tmp)
    
    #declare pointer to the ai name
    to_filepathd = char_dest+name+"/"+name+".def"

    file2 = open(to_filepathd,'w')
    file2.write(template.render(char_name=name, display_name = name, cmd = name))

    file2.close()
    
    add_char_to_list(name)
    return name


  
def gen_names(num, gen):
    l = []
    for i in np.arange(num):
        s = "dArwIn_G{0}_{1}".format(gen,i)
        l.append(s)
    return l
             

def initial_population(num_to_gen, gen):
    #Create unique names for each char and init their elo to 100
    names = gen_names(num_to_gen,gen)
    elo=[]
    move_seqs=[]
    print("creating population...")
    for i in names:
        sq_li = spawn_randomly(i)
        move_seqs.append(sq_li)
        elo.append(1000)
    print("done!")
    return names,move_seqs, elo



if __name__ =='__main__':
    
    print("main called directly")
    name = "TestSubjectB"
    fin, seq = generate_move_list()
    










