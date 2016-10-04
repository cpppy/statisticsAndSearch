# -*- coding: utf-8 -*-

# read resOut.txt
def readTxt():
	fr = open("resOut.txt")
	arrayoflines = fr.readlines()
	
	resOut = []
	dic = {}
	for lineindex in range(len(arrayoflines)):
		line = arrayoflines[lineindex].strip()
		listfromline = line.split(',')
		resOut.append(listfromline)
		s=listfromline[0]
		sid = s[0:6]
		dic[sid]=lineindex+1
		#print s[7:]
		return resOut,dic

def search(sid,time,resOut,dic):
	index = dic[sid]
	symbolID=resOut[index][0][7:]
	if(time[1]==':'):
		time = '0'+time
	hour=int(time[0:2])
	minutes=int(time[3:5])
	num=hour*100+minutes
	col=0
	if(931<=num & num<=1130):
		col=(hour-9)*60+minutes-30
	elif(1301<=num & num<=1500):
		col=120+(hour-13)*60+minutes
	else:
		col=0
	if(col!=0):
		outss=resOut[index][col]
		
		pos1=outss.find('|')
		pos2=outss.find('|',pos1+1)
		price=outss[pos1+1,pos2]
		vol=outss[pos2+1:]
		return symbolID,price,vol
	else:	
		return symbolID,0,0
	


if __name__ == "__main__":
	resOut,dic = readTxt()
	print search("600123","14:35",resOut,dic)
	
