# -*-coding: utf-8 -*-
import sqlite3
import json
import sys
import os
import codecs
import types

path=os.path.abspath(os.path.dirname(sys.argv[0]))
jsonpath=os.path.join(path,"contents.txt")

#python3 中打开文件最好用codec.open，如果用直接open(),默认gbk编码可能会出现编码错误，
f = codecs.open("contents.txt", 'r', 'UTF-8')
s = json.loads(f.read())
#print(s["seleList"][0])
d = s["seleList"][0]
#对dict进行排序，使用lambda语句，排序后的d是个tuple，再将此tuple生成list，list再到tuple
d=sorted(d.items(), key=lambda d:d[0])
outageInfo=[]
for item in d:
	outageInfo.append(item[1])
#outageInfo =tuple(s["seleList"][0].values())
outageInfo=tuple(outageInfo)
print(outageInfo)



dbpath=os.path.join(path,"outage.db")
cx =sqlite3.connect(dbpath)
cu=cx.cursor()

#cu.execute(" create table if not exists pageModel (beginCount integer,pageCount integer,totalCount integer,totalPage integer,pageNow integer,tableRows integer)")
#cu.execute("insert into pageModel values(?,?,?,?,?,?)",(0,0,0,0,0,0))

#cu.execute(" create table if not exists outagelist (\
#typeName varchar(20),typeCode integer,startTime datetime,scope varchar(200),orgNo integer,orgName varchar(20),\
#cityName varchar(20),lineName varchar(20),countyName varchar(20),tgName varchar(20),tranName varchar(20),sdLineName varchar(20),\
#sgpoweroffId integer,streetName varchar(20),villageName varchar(20),roadName varchar(50),communityName varchar(20),\
#nowTime datetime,poweroffId integer,subsName varchar(20),pubTranName varchar(20),\
#stopDate datetime,poweroffArea varchar(30),poweroffReason varchar(20),powerTime datetime,powerComm varchar(20),\
#subsNo integer,lineNo integer,tgNo integer,infoStatus integer,infoStatusName varchar(20),\
#dateDay varchar(20),orgNos integer,cityCode integer,provinceCode integer)")

cu.execute(" create table if not exists outagelist (\
cityCode integer,cityName varchar(20),communityName varchar(20),countyName varchar(20),dateDay varchar(20),\
infoStatus integer,infoStatusName varchar(20),lineName varchar(20),lineNo integer,nowTime datetime,\
orgName varchar(20),orgNo integer,orgNos integer,powerComm varchar(20),powerTime datetime,\
poweroffArea varchar(30),\
poweroffId integer,\
poweroffReason varchar(20),\
provinceCode integer,pubTranName varchar(20),roadName varchar(50),scope varchar(200),sdLineName varchar(20),\
sgpoweroffId integer,startTime datetime,stopDate datetime,streetName varchar(20),subsName varchar(20),subsNo integer,tgName varchar(20),\
tgNo integer,tranName varchar(20),typeCode integer,typeName varchar(20),villageName varchar(20))")
cu.execute("insert into outagelist values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",outageInfo)
cx.commit()
