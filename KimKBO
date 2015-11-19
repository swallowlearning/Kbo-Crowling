import urllib
from bs4 import BeautifulSoup
from datetime import datetime
import itertools
import re

TeamName=['OB','SK','HT','HH','WO','NC','LG','KT','SS','LT']

year=2015

test_file=open('test.txt','w')

startString="DataClass = jindo.$Class({"
endString="_homeTeamCode :"
n=0

for imonth in range(10,11):
	for iday in range(1,3):
		date=str(year)+str(imonth)+'0'+str(iday)
		for iTeam in itertools.permutations(range(0,10),2):
			TeamMatch=TeamName[iTeam[0]]+TeamName[iTeam[1]]
			print(imonth,iday,TeamMatch)
			n=n+1
			urlName='http://sports.news.naver.com/gameCenter/gameRecord.nhn?gameId='+date+TeamMatch+'0&category=kbo'
			#print(urlName)
			mySoup=BeautifulSoup(urllib.urlopen(urlName).read(),'html.parser')
			soupTitle=mySoup.title.string
			#print([str(imonth),str(iday),TeamMatch])
			alert=mySoup.find(text=re.compile("alert"))
			if alert==None:
				print('\n'+'1')
				# crowling start
				mySoup_script=mySoup.find_all('script')
				mySoupData=str(mySoup_script[41])
				#print(mySoupData.find(startString))
				#print(mySoupData.find(endString))
				rawData=mySoupData[mySoupData.find(startString)+30:mySoupData.find(endString)-2]
				test_file.write(rawData)
				print(rawData)
#test_file.flush()
test_file.close()
# html OBSK, HHWO
# html NCLG

#http://sports.news.naver.com/gameCenter/gameRecord.nhn?gameId=20151001OBSK0&category=kbo
