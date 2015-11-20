#-*- coding: utf-8 -*-

import urllib
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
#배열 선언
gameIdList = []
homeBatterInputDataList = []
homePitcherInputDataList = []
awayBatterInputDataList = []
awayPitcherInputDataList = []
gameInfoInputDataList = []
etcInputDataList = []
matchResultDataList1 =[]
matchResultDataList2 =[]

homeBattetsOutputTxtData = str()
homePitchersOutputTxtData = str()
awayBattetsOutputTxtData = str()
awayPitchersOutputTxtData = str()
gameInfoOutputTxtData = str()
etcOutputTxtData = str()
matchResultOutputTxtData1 = str()
matchResultOutputTxtData2 = str()

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
	#game = "20150701SSWO0"
	getGameResultUrl = 'http://sports.news.naver.com/gameCenter/gameRecord.nhn?gameId='+game+'&category=kbo'
	soup = BeautifulSoup(urllib.urlopen(getGameResultUrl).read())
	rawData = str(soup)
	targetDataStartIndex = rawData.find("DataClass")
	targetData = rawData[targetDataStartIndex:]
	targetDataEndIndex = targetData.find("_homeTeamCode")
	targetData = targetData[:targetDataEndIndex]

	selectedDataStartIndex = targetData.find("pitchersBoxscore")
	selectedData = targetData[selectedDataStartIndex:]
	selectedDataEndIndex = selectedData.find("homeTeamNextGames")
	selectedData = selectedData[:selectedDataEndIndex]

	#데이터 알아보기 쉽게 띄어쓰기
	selectedData = selectedData.replace('"','')
	selectedData = selectedData.replace(':{','\n')
	selectedData = selectedData.replace(':[{','\n')
	selectedData = selectedData.replace('},{',',\n')
	selectedData = selectedData.replace('}],','\n')
	selectedData = selectedData.replace('}]},','\n')
	selectedData = selectedData.replace('},','\n')
	selectedData = selectedData.replace('}','')
	selectedData = selectedData.replace('],',']\n')

	#쓸데없는 데이터 잘라내기
	garbageDataStartIndex = selectedData.find("awayTeamNextGames")
	matchResultDataFront = selectedData[:garbageDataStartIndex]
	garbageDataEndIndex = selectedData.find("battersBoxscore")
	matchResultDataRear = selectedData[garbageDataEndIndex:]
	garbageDataStartIndex = matchResultDataRear.find("recentVsGames")
	matchResultDataRearFront = matchResultDataRear[:garbageDataStartIndex]
	garbageDataEndIndex = matchResultDataRear.find("currentInning")
	matchResultDataRearRear = matchResultDataRear[garbageDataEndIndex:]
	matchResultData = matchResultDataFront + '\n' + matchResultDataRearFront + '\n' + matchResultDataRearRear
	#print matchResultData


	#========================== 시스템 입력값들 만들어주기 ========================================
	#타자 스코어 정리
	garbageDataStartIndex = matchResultData.find("battersBoxscore")
	batterResultData = matchResultData[garbageDataStartIndex:]
	garbageDataEndIndex = batterResultData.find("awayTotal")
	battersData = batterResultData[:garbageDataEndIndex]
	dataIndex = battersData.find("away") + 4
	battersAwayData = battersData[dataIndex:]
	dataIndex = battersAwayData.find("home")
	battersAwayData = battersAwayData[:dataIndex]

	dataIndex = batterResultData.find("home") +4
	battersHomeData = battersData[dataIndex:]

	#투수 스코어 정리
	garbageDataStartIndex = matchResultData.find("pitchersBoxscore")
	pitcherResultData = matchResultData[garbageDataStartIndex:]
	garbageDataEndIndex = pitcherResultData.find("battersBoxscore")
	pitchersData = pitcherResultData[:garbageDataEndIndex]
	dataIndex = pitchersData.find("away") + 4
	pitchersAwayData = pitchersData[dataIndex:]
	dataIndex = pitchersAwayData.find("home")
	pitchersAwayData = pitchersAwayData[:dataIndex]

	dataIndex = pitchersData.find("home") +4
	pitchersHomeData = pitchersData[dataIndex:]

	#기타 기록
	garbageDataStartIndex = matchResultData.find("etcRecords") + 10
	etcResultData = matchResultData[garbageDataStartIndex:]

	#========================== 시스템 출력값들 만들어주기 ========================================
	garbageDataStartIndex = matchResultData.find("scoreBoard") + 14
	thisMatchResultData = matchResultData[garbageDataStartIndex:]
	garbageDataEndIndex = thisMatchResultData.find("currentInning") - 1
	thisMatchData = thisMatchResultData[:garbageDataEndIndex]
	garbageDataStartIndex = thisMatchData.find("gameInfo")
	thisMatchData2 = thisMatchData[:garbageDataStartIndex]
	thisMatchData2 = thisMatchData2.replace("rheb","")
	thisMatchData2 = thisMatchData2.replace("home:","home")
	thisMatchData2 = thisMatchData2.replace("away:","away")
	thisMatchData2 = thisMatchData2.replace("home","home:")
	thisMatchData2 = thisMatchData2.replace("away","away:")
	thisMatchData2 = thisMatchData2.replace("home:\n","home: ")
	thisMatchData2 = thisMatchData2.replace("away:\n","away: ")
	thisMatchData2 = thisMatchData2.replace(']\n\nhome:',']\nhome:')
	thisMatchData2index = thisMatchData2.find(']\nhome:')
	inningResult = thisMatchData2[thisMatchData2index+1:]
	recordResult = thisMatchData2[:thisMatchData2index+1]

	garbageDataStartIndex = thisMatchData.find("gameInfo") + 8
	gameInfoData = thisMatchData[garbageDataStartIndex:]

	homeBatterInputDataList.append(battersHomeData)
	homePitcherInputDataList.append(pitchersHomeData)
	awayBatterInputDataList.append(battersAwayData)
	awayPitcherInputDataList.append(pitchersAwayData)
	gameInfoInputDataList.append(gameInfoData)
	etcInputDataList.append(etcResultData)
	matchResultDataList1.append(inningResult)
	matchResultDataList2.append(recordResult)


	#print '========================================================================================================================================================================================================================================'
	#print "게임 ID:" + game
	#print "경기 정보:" + gameInfoData
	#print "원정 타자 기록:" + battersAwayData
	#print "홈 타자 기록:" + battersHomeData
	#print "원정 투수 기록:"+pitchersAwayData
	#print "홈 투수 기록:"+pitchersHomeData
	#print "기타 기록:"+etcResultData
	#print "경기 결과 종합:"+thisMatchData2

for element in range(0, len(gameIdList)):
	homeBattetsOutputTxtData = homeBattetsOutputTxtData+ '\n' + homeBatterInputDataList[element]
	homePitchersOutputTxtData = homePitchersOutputTxtData+ '\n' + homePitcherInputDataList[element]
	awayBattetsOutputTxtData = awayBattetsOutputTxtData+ '\n' + awayBatterInputDataList[element]
	awayPitchersOutputTxtData = awayPitchersOutputTxtData+ '\n' + awayPitcherInputDataList[element]
	gameInfoOutputTxtData = gameInfoOutputTxtData+ '\n' + gameInfoInputDataList[element]
	etcOutputTxtData = etcOutputTxtData+ '\n' + etcInputDataList[element]
	matchResultOutputTxtData1 = matchResultOutputTxtData1+ '\n' + matchResultDataList1[element]
	matchResultOutputTxtData2 = matchResultOutputTxtData2+ '\n' + matchResultDataList2[element]


#file save
outFile1 = open('/Users/habom/Desktop/homeBatters.txt', 'w')
outFile1.write(homeBattetsOutputTxtData)
outFile1.close

outFile2 = open('/Users/habom/Desktop/homePitchers.txt', 'w')
outFile2.write(homePitchersOutputTxtData)
outFile2.close

outFile3 = open('/Users/habom/Desktop/awayBatters.txt', 'w')
outFile3.write(awayBattetsOutputTxtData)
outFile3.close

outFile4 = open('/Users/habom/Desktop/awayPitchers.txt', 'w')
outFile4.write(awayPitchersOutputTxtData)
outFile4.close

outFile5 = open('/Users/habom/Desktop/gameInfo.txt', 'w')
outFile5.write(gameInfoOutputTxtData)
outFile5.close

outFile6 = open('/Users/habom/Desktop/etcRecords.txt', 'w')
outFile6.write(etcOutputTxtData)
outFile6.close

outFile7 = open('/Users/habom/Desktop/matchResult1.txt', 'w')
outFile7.write(matchResultOutputTxtData1)
outFile7.close

outFile8 = open('/Users/habom/Desktop/matchResult2.txt', 'w')
outFile8.write(matchResultOutputTxtData2)
outFile8.close



