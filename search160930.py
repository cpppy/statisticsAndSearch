import gtk
from pylab import *
from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import matplotlib.pyplot as plt

class mywindow(gtk.Window):
	def __init__(self):
		super(mywindow,self).__init__()
		
		self.set_title("Search and PLot")
		self.set_size_request(800,800)
		self.set_position(gtk.WIN_POS_CENTER)

		fixed=gtk.Fixed()

		#shotnumber
		#shotnum label setting
		numlabel=gtk.Label('Security ID:')
		numlabel.set_size_request(100,30)
		fixed.put(numlabel,100,100)

		self.numtext=gtk.Entry()
		self.numtext.set_size_request(100,30)
		fixed.put(self.numtext,200,100)
		self.numtext.set_text('600123')
		global shotnum
		shotnum=self.numtext.get_text()
		shotnum=str(int(shotnum)-1)
		self.numtext.set_text(shotnum)

		self.numtext.connect('key-release-event',self.on_key_release)

		#shotnum button defination
		numprebut=gtk.Button('Previous ID')
		numprebut.set_size_request(120,30)
		fixed.put(numprebut,350,100)             
		numprebut.connect('clicked',self.OnNumPreBut,'Previous ID')

		numnexbut=gtk.Button('Next ID')
		numnexbut.set_size_request(120,30)
		fixed.put(numnexbut,500,100)
		numnexbut.connect('clicked',self.OnNumNexBut,'Next ID')

		#Timeslice
		#Timeslice label setting
		timelabel=gtk.Label('TimeSlice:')
		timelabel.set_size_request(100,30)
		fixed.put(timelabel,100,200)

		self.timetext=gtk.Entry()
		self.timetext.set_size_request(90,30)
		fixed.put(self.timetext,190,200)
		global time
		self.timetext.set_text('9:31')
		time=self.timetext.get_text()
		self.timetext.connect('key-release-event',self.on_time_release)

		timelabel2=gtk.Label('(9:31~11:30 or 13:01~15:00)')
		timelabel2.set_size_request(250,30)
		fixed.put(timelabel2,80,250)

		#Timeslice button defination
		pretimebut=gtk.Button('Previous')
		pretimebut.set_size_request(100,30)
		fixed.put(pretimebut,330,200)
		pretimebut.connect('clicked',self.OnPreTimeBut,'Previous')

		nextimebut=gtk.Button('Next')
		nextimebut.set_size_request(100,30)
		fixed.put(nextimebut,450,200)
		nextimebut.connect('clicked',self.OnNexTimeBut,'Next')


		#Plotbutton defination
		plotbut=gtk.Button('Plot')
		plotbut.set_size_request(100,60)
		fixed.put(plotbut,600,185)

		plotbut.connect('clicked',self.OnPlotBut,'Plot')


		#axes defination
		xlimlabel=gtk.Label('Xlim:')
		xlimlabel.set_size_request(50,30)
		fixed.put(xlimlabel,120,300)

		self.xbegin=gtk.Entry()
		self.xbegin.set_size_request(50,30)
		fixed.put(self.xbegin,170,300)
		self.xbegin.set_text('20')         
		global xb
		xb=self.xbegin.get_text()
		#self.xbegin.set_editable(False)
		self.xbegin.connect('key-release-event',self.on_xbegin_release)

		self.xend=gtk.Entry()
		self.xend.set_size_request(50,30)
		fixed.put(self.xend,230,300)
		self.xend.set_text('150')
		global xe
		xe=self.xend.get_text()
		#self.xend.set_editable(False)
		self.xend.connect('key-release-event',self.on_xend_release)



		ylimlabel=gtk.Label('Ylim:')
		ylimlabel.set_size_request(50,30)
		fixed.put(ylimlabel,340,300)

		self.ybegin=gtk.Entry()
		self.ybegin.set_size_request(50,30)
		fixed.put(self.ybegin,390,300)
		self.ybegin.set_text('0')
		global yb
		yb=self.ybegin.get_text()
		self.ybegin.connect('key-release-event',self.on_ybegin_release)

		self.yend=gtk.Entry()
		self.yend.set_size_request(50,30)
		fixed.put(self.yend,450,300)
		self.yend.set_text('20')
		global ye
		ye=self.yend.get_text()
		self.yend.connect('key-release-event',self.on_yend_release)

		#overlay setting
		olaylabel=gtk.Label('Overlay')
		olaylabel.set_size_request(80,30)
		fixed.put(olaylabel,280,400)

		self.radio1=gtk.RadioButton(None,'ON  (Max. 7)')
		fixed.put(self.radio1,360,400)

		self.radio2=gtk.RadioButton(self.radio1,'OFF')
		fixed.put(self.radio2,480,400)


		self.connect('destroy',gtk.main_quit)

		self.add(fixed)

		self.show_all()

	def OnPlotBut(self,widget,data):
		global shotnum,xb,xe,yb,ye
		global canvas
		global a
		global f
		
		if self.radio1.get_active():
			#plt.plot(x,S+1),ylabel('radio1')
			#print('radio1')
			win=gtk.Window()
			win.connect('destroy',lambda x: gtk.main_quit())
			win.set_default_size(900,300)
			win.set_title(shotnum)

			f=Figure()
			a=f.add_subplot(111)
			t=range(50)
			y=np.sin(t)
			a.plot(t,y)

			canvas=FigureCanvas(f)
			win.add(canvas)

			win.show_all()
			gtk.main()
			
		else:
			t=range(50)
			y=np.sin(t)+10
			a.plot(t,y)
			f.canvas.draw()
			 

	def OnNumPreBut(self,widget,data):
		global shotnum
		shotnum=str(int(shotnum)-1)
		self.numtext.set_text(shotnum)

	def OnNumNexBut(self,widget,data):
		global shotnum
		shotnum=str(int(shotnum)+1)
		self.numtext.set_text(shotnum)

	def OnPreTimeBut(self,widget,data):
		global time
		time=str(float(time)-0.0015)
		self.timetext.set_text(time)

	def OnNexTimeBut(self,widget,data):
		global time
		time=str(float(time)+0.0015)
		self.timetext.set_text(time)

	def on_key_release(self,widget,data):
		global shotnum
		shotnum=self.numtext.get_text()

	def on_time_release(self,widget,data):
		global time
		time=self.timetext.get_text()
		  
	def on_xbegin_release(self,widget,data):
		global xb
		xb=self.xbegin.get_text()

	def on_xend_release(self,widget,data):
		global xe
		xe=self.xend.get_text()
		  
	def on_ybegin_release(self,widget,data):
		global yb
		yb=self.ybegin.get_text()

	def on_yend_release(self,widget,data):
		global ye
		ye=self.yend.get_text()
		  
		  
mywindow()
gtk.main()
