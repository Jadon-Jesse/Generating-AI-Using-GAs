# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 22:05:26 2017

@author: Jadon
"""

import os
import shutil
import jinja2 as jin

dAI_dir = "C:/Users/Jadon/Work Space 4Y/RP/Code/dArwIn/"
dAI_req_dir = "C:/Users/Jadon/Work Space 4Y/RP/Code/dArwIn/required/"

names = ["dArwIn_G01",
         "dArwIn_G02",
         "dArwIn_G03"]

char_dest = "C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/chars/"



def copy_req_to_char(name):
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

    file = open(to_filepath,'w')
    file.write(template.render(ai='West'))
#print(template.render(name='West',bur='TOO'))
    file.close()
    
    kfm_def_tmp = "kfm.def"
    
    env_def = jin.Environment(loader=jin.FileSystemLoader(dAI_dir))
    template = env_def.get_template(kfm_def_tmp)
    
    #declare pointer to the ai name
    to_filepathd = char_dest+name+"/"+name+".def"

    file2 = open(to_filepathd,'w')
    file2.write(template.render(char_name=name, display_name = name, cmd = name+".cmd"))
#print(template.render(name='West',bur='TOO'))
    file2.close()
    
    add_char_to_list(name)
    
    
    
    
#for i in names:
#    copy_req_to_char(i)

def replace(filename):
    shutil.move("select_temp.def", "C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/data/select.def")

def temp(txt):
    filename = "select_temp.def"
    with open(filename, 'w') as f:
         f.writelines(txt)
         
    replace(filename)


def add_char_to_list(char_name):
    filename = "C:/Users/Jadon/Work Space 4Y/RP/MUGEN/mugen-1.0/mugen/data/select.def"
    with open(filename, 'r') as f:
        text = f.readlines()
        text.insert(72, char_name+' \n')
        temp(text)
        
        

           



for i in names:
    copy_req_to_char(i)













