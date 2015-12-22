# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sqlite3, os, sys
from shutil import copy

reload(sys)
sys.setdefaultencoding('utf-8')

filename = 'data/text.txt'
database = 'data/letters.db'
features = ['卷', '◎', '◇', '△', '○']
# database structure CREATE TABLE letters (id INTEGER PRIMARY KEY, juan TEXT, author TEXT, title, TEXT letter TEXT, dynasty TEXT)
def createDB(database, refresh):
    current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    if os.path.exists(database):
        if refresh:
            copy(current_path + '/' + 'letters_template.db', database)
    else:
        copy(current_path + '/' + 'letters_template.db', database)


def clean(file):
    f = open(filename, 'r')
    juan, author, title, content = '', '', '', ''
    texts = []
    for line in f.readlines():
        line = line.replace('　　', '').replace('\r\n', '').replace('\n', '')
        if features[0] in line and len(line) < 30 and '冬蕉卷心赋' not in line and '泥洹记' not in line and '善卷' not in line:
            juan = line.replace('\n', '')
        elif features[1] in line:
            author = line.replace(features[1], '')
        elif features[2] in line:
            title = line.replace(features[2], '')
        else:
            if line != '':
                content += line
        if features[1] in line or features[2] in line or features[3] in line or (features[0] in line and len(line) < 30 and '冬蕉卷心赋' not in line and '泥洹记' not in line and '善卷' not in line):
            if content != '':
                print content
                pass
            texts.append([juan, author, title, content])
            content = ''

    f.close()
    return texts


createDB(database, True)
conn = sqlite3.connect(database)
cursor = conn.cursor()
letters = clean(filename)

for letter in letters:

    sql = "INSERT INTO letters (juan, author, title, letter) VALUES ('%s', '%s', '%s', '%s')" % (letter[0], letter[1], letter[2], letter[3])
    # print sql
    if '书' in letter[2]:
        print sql
        cursor.execute(sql)
        conn.commit()

conn.close()

if __name__ == '__main__':
    pass
