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
     test1=re.search('::Title::\((.+?)\)::', line)
     if test1:
      title = test1.group(1)
 
     test2=re.search('::Description::\((.+?)\)::', line)
     if test2:
      description = test2.group(1)
 
     test3=re.search('::Relevance::\((.+?)\)::', line)
     if test3:
      relevance = test3.group(1)
 
     test4=re.search('::Reference::\((.+?)\)::', line)
     if test4:
      reference = test4.group(1)
 
     test5=re.search('::Match::#(.+?)#::', line)
     if test5:
      matchs = test5.group(1)

     if description and reference and relevance and matchs and title:
         content=description+"\n"+reference+"\n"
         current_time = datetime.datetime.now()
         mylist.append((lang,title,content,relevance,matchs,0,current_time))
         title=0 
         description=0
         reference=0
         matchs=0
         relevance=0

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
