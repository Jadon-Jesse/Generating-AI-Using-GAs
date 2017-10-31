# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 21:07:58 2017

@author: Jadon
"""

import jinja2 as jin

#temp = jin.Template('Hello {{name}}')
#print (temp.render(name='he'))

template_filename = 'temp.txt'

env = jin.Environment(loader=jin.FileSystemLoader('.'))
template = env.get_template(template_filename)

file = open('new.cmd','w')
file.write(template.render(name='West',bur='TOO'))
#print(template.render(name='West',bur='TOO'))
file.close()