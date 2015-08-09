# -*- coding: utf-8 -*
#for python2.7
import cookielib
import urllib
import urllib2
import sys
import os 
import hashlib
import json
import requests
import sqlite3

#定义post_data类，用于提交数据时构建post数据
class PostData(object):
	def __init__(self):
        	self.orgNo='21401'
		self.outageStartTime='2015-08-01'
		self.outageEndTime='2015-08-05'
		self.scope=''
		self.provinceNo='21102'
		self.typeCode=''
		self.lineName=''
	def post_data(self):
		return {
				'orgNo':self.orgNo,
				'outageStartTime':self.outageStartTime,
				'outageEndTime':self.outageEndTime,
				'scope':self.scope,
				'provinceNo':self.provinceNo,
				'typeCode':self.typeCode,
				'lineName':self.lineName
		}

class pageModel(object):
	def __init__(self):
		self.beginCount = 0
		self.pageCount =0
		self.totalCount = 0
		self.totalPage =0
		self.pageNow =1
		self.tableRows =0

class outageDetail(object):
	def __init__(self):
		self.cityCode=''
		self.cityName=''
		self.communityName=''
		self.countyNmae=''
		self.dateDay=''
		self.infoStatus=''
		self.infoStatusNmae=''
		self.lineName=''
		self.lineNo=''
		self.nowTime=''
		self.orgName=''
		self.orgNo=''
		self.orgNos=''
		self.powerComm=''
		self.powerTime=''
		self.poweroffArea=''
		self.poweroffId=''
		self.provinceCode=''
		self.pubTranName=''
		self.roadName=''
		self.scope=''
		self.sdLineName=''
		self.sgpoweroffId=''
		self.startTime=''
		self.stopTime=''
		self.streetName=''
		self.subsName=''
		self.subsName=''
		self.tgName=''
		self.tgNo=''
		self.tranName=''
		self.typeCode=''
		self.typeName=''
		self.villageName=''


def insert_outageInfo(seleList):
	path=os.path.abspath(os.path.dirname(sys.argv[0]))
	dbpath=os.path.join(path,"outage.db")
	cx =sqlite3.connect(dbpath)
	cu=cx.cursor()
	for d in seleList:
		#对dict进行排序，使用lambda语句，排序后的d是个tuple，再将此tuple生成list，list再到tuple
		d=sorted(d.items(), key=lambda d:d[0])
		outageInfo=[]
		for item in d:
			outageInfo.append(item[1])
			#outageInfo =tuple(s["seleList"][0].values())
		outageInfoTuple=tuple(outageInfo)
		cu.execute("insert into outagelist values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",outageInfoTuple)
		cx.commit()
	cu.close()
	cx.close()


#准备写入sqlite
def insert_pageModelInfo(pageModelTuple):
	path=os.path.abspath(os.path.dirname(sys.argv[0]))
	dbpath=os.path.join(path,"outage.db")
	cx =sqlite3.connect(dbpath)
	cu=cx.cursor()
	cu.execute("insert into pageModel values(?,?,?,?,?,?)",pageModelTuple)
	cx.commit()
	cu.close()
	cx.close()

def create_outageDB():
	path=os.path.abspath(os.path.dirname(sys.argv[0]))
	dbpath=os.path.join(path,"outage.db")
	cx =sqlite3.connect(dbpath)
	cu=cx.cursor()
	#create pageModelDB
	cu.execute(" create table if not exists pageModel (beginCount integer,pageCount integer,totalCount integer,totalPage integer,pageNow integer,tableRows integer)")
	#create outagelistDB fields orderby field names
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
	cx.commit()
	cu.close()
	cx.close()



headers = {
"Host":"www.95598.cn",
"Connection": "keep-alive",
"Accept": "*/*",
"Origin": "http://www.95598.cn",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Referer": "http://www.95598.cn/95598/outageNotice/initOutageNotice?type=1&partNo=PM06003002",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.8"
}

test = PostData()
post_data = test.__dict__



#main
outageURL="http://www.95598.cn/95598/outageNotice/initOutageNotice?type=1&partNo=PM06003002"
posturl="http://www.95598.cn/95598/outageNotice/queryOutageNoticeList"
#post_data=({'orgNo':'21401','outageStartTime':'2015-08-01','outageEndTime':'2015-08-05','scope':'','provinceNo':'21102','typeCode':'','lineName':''})

#访问显示停电的页面，获得cookies
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
resp = urllib2.urlopen(outageURL)
#print resp.read()

#向停电接口post数据，获得停电信息的Json数据
post_data = urllib.urlencode(post_data)
request = urllib2.Request(posturl,post_data,headers)
response =urllib2.urlopen(request)
outageJson = response.read()

#将json数据写入文件，便于debug
path = os.path.abspath(os.path.dirname(sys.argv[0]))
fullpath = os.path.join(path,"contents.txt")
with open(fullpath,"a") as code:
	code.write(outageJson)
	code.close()

s = json.loads(outageJson)
pageModel = s["pageModel"]
#print result
pageModelTuple=tuple(pageModel.values())
#print pageModelTuple

seleList = s["seleList"]
#print(len(seleList))
create_outageDB()
insert_outageInfo(seleList)





