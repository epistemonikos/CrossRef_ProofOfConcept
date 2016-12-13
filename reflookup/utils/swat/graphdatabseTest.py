__author__ = 'fmosso'
import pyorient
import json

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "admin", "admin" )

#create a databse
client.db_create( "db", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )


client.db_open( "db", "admin", "admin" )

client.command( "create class Paper extends V" )
client.command( "create class Reference extends E" )


#client.command( "INSERT INTO Paper CONTENT {name: \"paper1\"}")
#client.command( "INSERT INTO Paper CONTENT {name: \"paper2\"}")
#client.command( "INSERT INTO Paper CONTENT {name: \"paper3\"}")

#client.command("create edge Reference from (select from Paper where name = 'paper1') to (select from Paper where name = 'paper2')")

def insertPaper(JSON):
    try:
        client.command( "INSERT INTO Paper CONTENT" + str(JSON))
    except:
        pass

def makeReference(pbid1,pbid2):
    try:
        client.command("create edge Reference from (select from Paper where ids.pubmed = \""+pbid2+"\") to (select from Paper where ids.pubmed =\""+pbid1+"\")")
    except:
        pass

f= open("data.txt")
paper = (json.loads(f.readline()))
insertPaper (paper)
for line in f:
  reference = (json.loads(line))
  insertPaper(reference)
  makeReference(json.loads(paper)["ids"]["pubmed"],json.loads(reference)["ids"]["pubmed"])
f.close()


#makeReference("paper3","paper1")