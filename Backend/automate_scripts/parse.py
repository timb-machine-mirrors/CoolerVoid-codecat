import re
import os
import sqlite3
import sys
import datetime

def insert_eggs(database_local,mylists):
 conn = sqlite3.connect(database_local)
 conn.set_trace_callback(print)
 conn.cursor()
 for item in mylists:
  conn.execute('insert into rules ("lang","title","description","level","match1","match2","created_at") values (?,?,?,?,?,?,?)', item)
 conn.commit()

def parse_egg(input,database_local,lang):
 file1 = open(input, 'r')
 Lines = file1.readlines()
 mylist=[]
 title = 0
 description = 0 
 relevance = 0
 reference = 0
 matchs = 0

 for line in Lines:
     test=re.search('::Title::\((.+?)\)::', line)
     if test:
      title = test.group(1)
 
     test=re.search('::Description::\((.+?)\)::', line)
     if test:
      description = test.group(1)
 
     test=re.search('::Relevance::\((.+?)\)::', line)
     if test:
      relevance = test.group(1)
 
     test=re.search('::Reference::\((.+?)\)::', line)
     if test:
      reference = test.group(1)
 
     test=re.search('::Match::\#(.+?)\#::', line)
     if test:
      matchs = test.group(1)

     if description and reference and relevance and matchs and title:
         content=description+"\n"+reference+"\n"
         current_time = datetime.datetime.now()
         mylist.append((lang,title,content,relevance,matchs,0,current_time))
         title=0 
         description=0
         reference=0

# print(mylist)
 insert_eggs(database_local,mylist)
 
#print("{}".format( line.strip()))

def main():
 try:
  if len(sys.argv) == 4:
   parse_egg(sys.argv[1],sys.argv[2],sys.argv[3])
  else:
   print("Please follow the example\n $ python3 script.py file.egg database.sqlite3 lang_name\n")
 except Exception as e:
  print(" log error : "+str(e))
  exit(0)

if __name__=="__main__":
 main()
