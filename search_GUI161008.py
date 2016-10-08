# -*- coding: utf-8 -*-
import gtk
from pylab import *
from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import matplotlib.pyplot as plt
import resOutSearch
import matplotlib

class mywindow(gtk.Window):
	def __init__(self):
		global resOut,dic,sid,index,time,timedic
		resOut,dic = resOutSearch.readTxt()
		timedic = resOutSearch.time2dic()
		
		super(mywindow,self).__init__()	
		self.set_title("Search and PLot")
		self.set_size_request(620,280)
		self.set_position(gtk.WIN_POS_CENTER)
		fixed=gtk.Fixed()

		#Security ID
		#Security ID label setting
		numlabel=gtk.Label('Security ID:')
		numlabel.set_size_request(100,30)
		fixed.put(numlabel,50,50)	
		self.numtext=gtk.Entry()
		self.numtext.set_size_request(100,30)
		fixed.put(self.numtext,150,50)	
		self.numtext.set_text('600123')
		sid=self.numtext.get_text()
		self.numtext.connect('key-release-event',self.on_key_release)


		#Previous ID button defination
		numprebut=gtk.Button('Previous ID')
		numprebut.set_size_request(120,30)
		fixed.put(numprebut,300,50)             
		numprebut.connect('clicked',self.OnNumPreBut,'Previous ID')
		#Next ID button defination
		numnexbut=gtk.Button('Next ID')
		numnexbut.set_size_request(120,30)
		fixed.put(numnexbut,450,50)
		numnexbut.connect('clicked',self.OnNumNexBut,'Next ID')

		#Timeslice
		#Timeslice label setting
		timelabel=gtk.Label('TimeSlice:')
		timelabel.set_size_request(100,30)
		fixed.put(timelabel,50,100)
		self.timetext=gtk.Entry()
		self.timetext.set_size_request(100,30)
		fixed.put(self.timetext,150,100)	
		self.timetext.set_text('10:31')
		time=self.timetext.get_text()
		self.timetext.connect('key-release-event',self.on_time_release)
		
		#Timeslice limits label
		timelabel2=gtk.Label('(9:31~11:30 or 13:01~15:00)')
		timelabel2.set_size_request(220,30)
		fixed.put(timelabel2,50,130)

		#Timeslice button defination
		pretimebut=gtk.Button('Previous min')
		pretimebut.set_size_request(120,30)
		fixed.put(pretimebut,300,100)
		pretimebut.connect('clicked',self.OnPreTimeBut,'Previous')

		nextimebut=gtk.Button('Next min')
		nextimebut.set_size_request(120,30)
		fixed.put(nextimebut,450,100)
		nextimebut.connect('clicked',self.OnNexTimeBut,'Next')

		#Plotbutton defination
		plotbut=gtk.Button('Search & Plot')
		plotbut.set_size_request(200,60)
		fixed.put(plotbut,380,170)
		plotbut.connect('clicked',self.OnPlotBut,'Plot')

		#axes defination
		xlimlabel=gtk.Label('Extent:')
		xlimlabel.set_size_request(50,30)
		fixed.put(xlimlabel,70,170)
		
		#xbegin
		self.xbegin=gtk.Entry()
		self.xbegin.set_size_request(50,30)
		fixed.put(self.xbegin,120,170)
		self.xbegin.set_text('20')
		         
		global xb  
		xb=self.xbegin.get_text()
		#self.xbegin.set_editable(False)
		self.xbegin.connect('key-release-event',self.on_xbegin_release)
		
		#xend
		self.xend=gtk.Entry()
		self.xend.set_size_request(50,30)
		fixed.put(self.xend,190,170)
		self.xend.set_text('20')
		
		global xe  #xend
		xe=self.xend.get_text()
		#self.xend.set_editable(False)
		self.xend.connect('key-release-event',self.on_xend_release)

		#overlay setting
		olaylabel=gtk.Label('Overlay')
		olaylabel.set_size_request(80,30)
		fixed.put(olaylabel,50,220)

		self.radio1=gtk.RadioButton(None,'ON  (Max. 7)')
		fixed.put(self.radio1,130,225)

		self.radio2=gtk.RadioButton(self.radio1,'OFF')
		fixed.put(self.radio2,260,225)


		self.connect('destroy',gtk.main_quit)
		self.add(fixed)
		self.show_all()

	def OnPlotBut(self,widget,data):
		global sid,time,resOut,dic,timedic,xb,xe
		global canvas,a,b,f
		
		if self.radio1.get_active():
			#plt.plot(x,S+1),ylabel('radio1')
			#print('radio1')
			win=gtk.Window()
			win.connect('destroy',lambda x: gtk.main_quit())
			win.set_default_size(900,600)
			win.set_title(sid+'-'+time)

			f=Figure()
			a=f.add_subplot(211)
			b=f.add_subplot(212)
			zhfont=matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc')
			
			#t=range(50)
			x=[]
			tx=[]
			y=[]
			y2=[]
			symbolID=""
			col=timedic[time]
			#xlim setting
			xbi=(-1)*int(xb)
			xei=int(xe)+1
			if(col+xbi<1):
				xbi=1-col
			if(col+xei>241):
				xei=241-col
			for i in range(xbi,xei):
				x.append(col+i)
				timestr=resOutSearch.col2time(col+i)
				tx.append(timestr)
				symbolID,price,vol = resOutSearch.search(sid,col+i,resOut,dic)
				y.append(price)
				y2.append(vol)
				
			#set ps
			#a
			symbolID,price,vol = resOutSearch.search(sid,col,resOut,dic)
			# output
			print "------------------------"
			print "SecurityID: ",sid
			print "symbol: ",symbolID
			print "timeSlice: ",time
			print "price: ",price
			print "vol: ",vol
			print "-------------"
			
			a.set_title(sid+'|'+symbolID+'|'+time+' (价格: '+str(price)+'元, 交易量: '+str(vol)+')',fontproperties=zhfont,fontsize=14)
			#print symbolID
			a.set_xlabel('Time')
			a.set_ylabel('Price')
			#a.set_xticklabels(tx)
			
			#b
			print symbolID
			b.set_xlabel('Time')
			b.set_ylabel('TradeVolume')
			#b.set_xticklabels(tx)   #,rotation=90,rotation_mode="anchor")
			
			#y=np.sin(t)
			a.plot(x,y,'o-')
			a.annotate(time+'|'+sid,xy=(col,price), xycoords='data',xytext=(10, 30), textcoords='offset points', fontsize=12,arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
			
			
			b.bar(x,y2)
			b.annotate(time+'|'+sid,xy=(col,vol), xycoords='data',xytext=(10, 30), textcoords='offset points', fontsize=12,arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
			

			canvas=FigureCanvas(f)
			win.add(canvas)

			win.show_all()
			gtk.main()
			
		else:
			x=[]
			tx=[]
			y=[]
			y2=[]
			symbolID=""
			col=timedic[time]
			#xlim setting
			xbi=(-1)*int(xb)
			xei=int(xe)+1
			if(col+xbi<1):
				xbi=1-col
			if(col+xei>241):
				xei=241-col
			for i in range(xbi,xei):
				x.append(col+i)
				timestr=resOutSearch.col2time(col+i)
				tx.append(timestr)
				symbolID,price,vol = resOutSearch.search(sid,col+i,resOut,dic)
				y.append(price)
				y2.append(vol)
			
			symbolID,price,vol = resOutSearch.search(sid,col,resOut,dic)
			# output
			print "------------------------"
			print "SecurityID: ",sid
			print "symbol: ",symbolID
			print "timeSlice: ",time
			print "price: ",price
			print "vol: ",vol
			print "-------------"
			
			a.plot(x,y,'o-')
			a.annotate(time+'|'+sid,xy=(col,price), xycoords='data',xytext=(10, 30), textcoords='offset points', fontsize=12,arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
			f.canvas.draw()
			 

	def OnNumPreBut(self,widget,data):
		print "preID buttion"
		global sid,index
		print "SecurityID from ",sid
		index=dic[sid]
		index-=1
		sid=resOut[index][0][0:6]
		print "to ",sid
		self.numtext.set_text(sid)

	def OnNumNexBut(self,widget,data):
		print "nextID button"
		global sid,index
		print "SecurityID from ",sid
		index=dic[sid]
		index+=1
		sid=resOut[index][0][0:6]
		print "to ",sid
		self.numtext.set_text(sid)

	def OnPreTimeBut(self,widget,data):
		print "preTime button"
		global time
		print "time from ",time
		col=timedic[time]
		col-=1
		time=resOutSearch.col2time(col)
		print "to ",time		
		self.timetext.set_text(time)

	def OnNexTimeBut(self,widget,data):
		print "nextTime button"
		global time
		print "time from ",time
		col=timedic[time]
		col+=1
		time=resOutSearch.col2time(col)
		print "to ",time	
		self.timetext.set_text(time)

	def on_key_release(self,widget,data):
		global sid
		sid=self.numtext.get_text()

	def on_time_release(self,widget,data):
		global time
		time=self.timetext.get_text()
		  
	def on_xbegin_release(self,widget,data):
		global xb
		xb=self.xbegin.get_text()

	def on_xend_release(self,widget,data):
		global xe
		xe=self.xend.get_text()
		  

		  
		  
mywindow()
gtk.main()
