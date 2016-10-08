# -*- coding: utf-8 -*-

# read resOut.txt
def readTxt():
	fr = open("resOut.txt")
	arrayoflines = fr.readlines()
	
	resOut = []
	dic = {}        #dic[sid]=index  sid---string  index---int
	for lineindex in range(len(arrayoflines)):
		line = arrayoflines[lineindex].strip()
		listfromline = line.split(',')
		resOut.append(listfromline)
		s=listfromline[0]
		sid = s[0:6]
		dic[sid]=lineindex
		#print s[7:]
	return resOut,dic

# input sid(SercurityID) and col,output its data(symbolID,price,TradeVolume)
def search(sid,col,resOut,dic):
	index = dic[sid]
	symbolID=resOut[index][0][7:]
	if(col!=0):
		outss=resOut[index][col]
		if(outss=="0"):
			return symbolID,0,0
		pos1=outss.find('|')
		pos2=outss.find('|',pos1+1)
		price=outss[pos1+1:pos2]
		vol=outss[pos2+1:]
		return symbolID,price,vol
	else:	
		return symbolID,0,0
	
# build a timedic, timedic[timeStr]=colume
def time2dic():
	timedic={}
	for hour in range(9,16):
		for minutes in range(0,60):
			num=hour*100+minutes
			if(931<=num and num<=1130):
				col=(hour-9)*60+minutes-30
			elif(1301<=num and num<=1500):
				col=120+(hour-13)*60+minutes
			else:
				col=0
			if(col!=0):
				if(hour<10):
						hourstr='0'+str(hour)
				else:
					hourstr=str(hour)
				if(minutes<10):
					minutesstr='0'+str(minutes)
				else:
					minutesstr=str(minutes)
				time=hourstr+':'+minutesstr
				timedic[time]=col
	return timedic

# input colume , output timeStr
def col2time(col):
	if(col>=1 and col<=120):
		addH=(col+30)/60
		addM=(col+30)%60
		hourstr=str(9+addH)
		minutesstr=str(addM)
		if(int(hourstr)<10):
			hourstr='0'+hourstr
		if(addM<10):
			minutesstr='0'+minutesstr
		time=hourstr+':'+minutesstr
	elif(col>120 and col<=240):
		addH=(col-120)/60
		addM=(col-120)%60
		hourstr=str(13+addH)
		minutesstr=str(addM)
		if(addM<10):
			minutesstr='0'+minutesstr
		time=hourstr+':'+minutesstr
	else:
		time="error"
	return time		


if __name__ == "__main__":
	resOut,dic = readTxt()
	#symbolID,price,vol = search("600123","13:35",resOut,dic)
	#print symbolID,price,vol
	if(dic.has_key("600123")):
		print "exist"
		symbolID,price,vol = search("600123",10,resOut,dic)
		print symbolID,price,vol
		
	else:
		print "none"	
	timedic=time2dic()
	print timedic["09:31"]
	print col2time(10)
		
