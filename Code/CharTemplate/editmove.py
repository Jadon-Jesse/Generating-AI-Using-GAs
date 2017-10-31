# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 19:59:15 2017

@author: Jadon
"""

import numpy as np

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

string_to_append ='triggerall = var(59) = 1 \n'
string_to_append +='triggerall = Ctrl \n'

for move in move_list:
    file = "MoveList/"+move
    with open(file, "a") as myfile:
        myfile.write(string_to_append)












