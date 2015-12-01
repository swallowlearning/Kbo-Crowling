#-*- coding: utf-8 -*-

import urllib
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
#배열 선언
gameIdList = []
outputData =str()
pitchers = str()
batters =str()

#입력 정보
startYear = 2015
endYear = 2016
startMonth = 3
endMonth = 11

#게임ID 불러오기
for year in range(startYear, endYear):
	yearStr = str(year)
	for month in range(startMonth,endMonth):
		monthStr = "0"+str(month)
		getIdUrl = "http://sports.news.naver.com/schedule/index.nhn?uCategory=&category=kbo&year="+yearStr+"&month="+monthStr+"&teamCode=&date=20151031"
		soup = BeautifulSoup(urllib.urlopen(getIdUrl).read())
		gameIdData = soup.find_all('span', {'class': "td_btn"})
		gameIdDataStr = str(gameIdData)
		#HTML TAG제거
		gameIdDataStr = gameIdDataStr.replace('[<span class="td_btn">','')
		gameIdDataStr = gameIdDataStr.replace('<!-- 문자중계 경기결과 버튼 -->','')
		gameIdDataStr = gameIdDataStr.replace('<a href="/gameCenter/gameResult.nhn?category=kbo&amp;gameId=','')
		gameIdDataStr = gameIdDataStr.replace('" onclick="clickcr(this,','')
		gameIdDataStr = gameIdDataStr.replace(" 'sch.gamerecord', '', '', event);",'')
		gameIdDataStr = gameIdDataStr.replace('" target="_blank"><img alt="경기결과" height="23" src="http://imgnews.naver.net/image/sports/2011/baseball_schedule/btn_result2.gif" width="61"/></a>','')
		gameIdDataStr = gameIdDataStr.replace('</span>, <span class="td_btn">','')
		gameIdDataStr = gameIdDataStr.replace('<!-- TV 경기영상 버튼 -->','')
		gameIdDataStr = gameIdDataStr.replace('<a href="/gameCenter/gameVideo.nhn?category=kbo&amp;gameId=','')
		gameIdDataStr = gameIdDataStr.replace(" 'sch.gamevod', '', '', event);",'')
		gameIdDataStr = gameIdDataStr.replace('" target="_blank"><img alt="경기영상" height="23" src="http://imgnews.naver.net/image/sports/2010/kbo_schedule/btn_vod2.gif" width="61"/></a>','')
		gameIdDataStr = gameIdDataStr.replace('</span>]','')
		#열분리
		splitGameIdDataStr = gameIdDataStr.splitlines()
		#공백제거 및 리스트 생성
		cnt = 0
		for line in splitGameIdDataStr:
			if line != "": #빈칸이 아니면
				cnt =  cnt+1
				if cnt%2 == 1:
					gameIdList.append(line)
#print gameIdList

#게임내용 불러오기
for game in gameIdList:
	getGameResultUrl = 'http://sports.news.naver.com/gameCenter/gameRecord.nhn?gameId='+game+'&category=kbo'
	soup = BeautifulSoup(urllib.urlopen(getGameResultUrl).read())
	rawData = str(soup)
	targetDataStartIndex = rawData.find("DataClass")
	targetData = rawData[targetDataStartIndex:]
	targetDataEndIndex = targetData.find("_homeTeamCode")
	targetData = targetData[:targetDataEndIndex]

	selectedDataStartIndex = targetData.find("pitchersBoxscore")
	selectedData = targetData[selectedDataStartIndex:]
	selectedDataEndIndex = selectedData.find("etcRecords")
	selectedData = selectedData[:selectedDataEndIndex]
	selectedData = selectedData.replace('"','')
	selectedData = selectedData.replace(' ⅓','.33')
	selectedData = selectedData.replace(' ⅔','.63')

	startIndex3 =  selectedData.find("awayTeamNextGames")
	matchInfo = selectedData[startIndex3:]
	endIndex3 = matchInfo.find("battersBoxscore")
	matchInfo = matchInfo[:endIndex3]
	#print matchInfo
	startIndex4 =  matchInfo.find("aName")
	matchInfoToday = matchInfo[startIndex4:]
	endIndex4 = matchInfoToday.find("}")
	matchInfoToday = matchInfoToday[:endIndex4]
	#print matchInfoToday

	startIndex5 =  matchInfoToday.find("stadium")
	stadium = matchInfoToday[startIndex5:]
	endIndex5 = stadium.find(",")
	stadium = stadium[:endIndex5]

	startIndex6 =  matchInfoToday.find("gweek")
	gweek = matchInfoToday[startIndex6:]
	endIndex6 = gweek.find(",")
	gweek = gweek[:endIndex6]

	startIndex7 =  matchInfoToday.find("gdate")
	gdate = matchInfoToday[startIndex7:]
	endIndex7 = gdate.find(",")
	gdate = gdate[:endIndex7]

	gameInfomation = gdate +','+gweek+','+stadium
	#print gameInfomation

	startIndex8 =  selectedData.find("scoreBoard")
	matchResult = selectedData[startIndex8:]
	endIndex8 = matchResult.find("rheb")
	matchResult = matchResult[:endIndex8]

	startIndex9 =  matchResult.find("home")
	matchResultHome = matchResult[startIndex9:]
	endIndex9 = matchResultHome.find("]")
	matchResultHome = matchResultHome[:endIndex9]
	matchResultHome = matchResultHome.replace('home:[',',')
	#print matchResultHome

	startIndex10 =  matchResult.find("away")
	matchResultAway = matchResult[startIndex10:]
	endIndex10 = matchResultAway.find("]")
	matchResultAway = matchResultAway[:endIndex10]
	matchResultAway = matchResultAway.replace('away:[',',')
	#print matchResultAway

	startIndex2 =  selectedData.find("battersBoxscore")
	battersBoxscore = selectedData[startIndex2:]
	endIndex2 = battersBoxscore.find("awayTotal")
	battersBoxscore = battersBoxscore[:endIndex2]
	battersBoxscore = battersBoxscore.replace('}','\n')
	battersBoxscore = battersBoxscore.replace('battersBoxscore:{','')
	battersBoxscore = battersBoxscore.replace('away:[{','\n')
	battersBoxscore = battersBoxscore.replace('home:[{','\n')
	battersBoxscore = battersBoxscore.replace(',{','')
	battersBoxscore = battersBoxscore.replace(']\n,','')
	battersBoxscore = battersBoxscore.replace(':,',':0,')
	
	splitBattersBoxscore = battersBoxscore.splitlines()	
	cnt = 0
	for spLines in splitBattersBoxscore:
		if spLines.count(']')>0:
			cnt = cnt +1
		if cnt>0:
			teamflag = 'Home,'
			result = matchResultHome
		else:
			teamflag = 'away,'
			result = matchResultAway

		if len(spLines)>5:
			#print spLines
			pitchersCode=',hr:0,inn:0,bbhp:0,pCode:0,era:0,l:0,kk:0,w:0,tb:0,s:0,r:0,hit:0,pa:0,name:0,wls:0,bf:0,ab:0,bb:0,gameCount:0,er:0'
			#pitchersCode = ',dummy,'
			tmp3 = gameInfomation +','+ teamflag + spLines + pitchersCode + result
			#tmp3 = teamflag + spLines + pitchersCode
			batters = batters + '\n' +tmp3
	#print batters

	startIndex =  selectedData.find("pitchersBoxscore")
	pitchersBoxscore = selectedData[startIndex:]
	endIndex = pitchersBoxscore.find("awayTeamNextGames")
	pitchersBoxscore = pitchersBoxscore[:endIndex]
	pitchersBoxscore = pitchersBoxscore.replace('}','\n')
	pitchersBoxscore = pitchersBoxscore.replace('pitchersBoxscore:{','')
	pitchersBoxscore = pitchersBoxscore.replace('away:[{','\n')
	pitchersBoxscore = pitchersBoxscore.replace('home:[{','\n')
	pitchersBoxscore = pitchersBoxscore.replace(',{','')
	pitchersBoxscore = pitchersBoxscore.replace(']\n,','')
	pitchersBoxscore =  pitchersBoxscore.replace('wls:,','wls:무,')

	splitPitchersBoxscore = pitchersBoxscore.splitlines()
	cnt = 0
	for spLines in splitPitchersBoxscore:
		if spLines.count(']')>0:
			cnt = cnt +1
		if cnt>0:
			teamflag = 'Home,'
			result = matchResultHome
		else:
			teamflag = 'away,'
			result = matchResultAway

		if len(spLines)>5:
			pCodeStartIndex = spLines.find('pCode')
			tmp1 = spLines[pCodeStartIndex:]
			endIndex = tmp1.find(',')
			tmp1 = tmp1[:endIndex+1]
		
			nameStartIndex = spLines.find('name')
			tmp2 = spLines[nameStartIndex:]
			endIndex = tmp2.find(',')
			tmp2 = tmp2[:endIndex+1]

			battersCode1='inn18:0,inn19:0,run:0,inn9:0,pos:0,rbi:0,inn7:0,inn11:0,inn8:0,inn10:0,inn5:0,inn13:0,inn6:0,inn12:0,inn3:0,inn15:0,hit:0,inn4:0,inn14:0,inn1:0,inn17:0,inn2:0,'
			battersCode2 ='hra:0,inn24:0,inn23:0,inn22:0,inn21:0,inn25:0,ab:0,inn20:0,'
			#battersCode1 = 'dummy1,'
			#battersCode2 = 'dummy2,'
			tmp3 = gameInfomation +','+ teamflag + battersCode1 + tmp2 + 'inn16:0,'+ tmp1 + battersCode2+ spLines+result
			pitchers = pitchers + '\n' +tmp3
	#print pitchers
	inputData = batters+pitchers
	print inputData

#file save
outFile1 = open('/Users/habom/Desktop/result.txt', 'w')
outFile1.write(inputData)
outFile1.close
