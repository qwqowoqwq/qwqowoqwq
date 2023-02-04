import random
import sys
import ctypes
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia

if sys.platform == "win32":
	desktop = ctypes.cdll.LoadLibrary("./desktop.dll")

class QwQWidget(QtWidgets.QWidget):

	def __init__(self, app):
		super().__init__()

		screenSize = app.primaryScreen().size()
		self.app = app
		self.screenWidth = screenSize.width()
		self.screenHeight = screenSize.height()
		self.width = 200
		self.height = 200
		self.left = self.screenWidth - self.width - 100
		self.top = self.screenHeight - self.height - 100
		self.setMouseTracking(True)

		self.follow_mouse = False
		self.angry1 = False
		self.mouse_drag_pos = self.pos()

		self.animation = QtCore.QTimer()
		self.animation.timeout.connect(self.timerFire)
		self.animation.start(10)
		self.oo_state = 0
		self.freewalk = 5000
		self.count = 500
		self.walk = 0

		#images of oo
		self.oo_normal = QtGui.QImage.scaled(QtGui.QImage("oo_normal.png", format = None), self.width, self.height)
		self.oo_angry1 = QtGui.QImage.scaled(QtGui.QImage("oo_angry1.png", format = None), self.width, self.height)
		self.oo_angry2 = QtGui.QImage.scaled(QtGui.QImage("oo_angry2.png", format = None), self.width, self.height)
		self.oo_eat1 = QtGui.QImage.scaled(QtGui.QImage("oo_eat1.png", format = None), self.width, self.height)
		self.oo_eat2 = QtGui.QImage.scaled(QtGui.QImage("oo_eat2.png", format = None), self.width, self.height)
		self.oo_openmouth_big = QtGui.QImage.scaled(QtGui.QImage("oo_openmouth_big.png", format = None), self.width, self.height)
		self.oo_openmouth_small = QtGui.QImage.scaled(QtGui.QImage("oo_openmouth_small.png", format = None), self.width, self.height)
		self.oo_toothache = QtGui.QImage.scaled(QtGui.QImage("oo_toothache.png", format = None), self.width, self.height)
		self.oo_walk1 = QtGui.QImage.scaled(QtGui.QImage("oo_walk1.png", format = None), self.width, self.height)
		self.oo_walk2 = QtGui.QImage.scaled(QtGui.QImage("oo_walk2.png", format = None), self.width, self.height)

		self.initUI()

	def initUI(self):
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
		QtCore.Qt.FramelessWindowHint |
		QtCore.Qt.Tool)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.randomPosition()

		pat = QtGui.QPalette()
		pat.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(self.oo_normal)))
		self.setPalette(pat)

		self.show()

	def drawPalette(self, picture):
		pat = QtGui.QPalette()
		pat.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(picture)))
		self.setPalette(pat)
	
	def walkChange(self):
		if self.walk == 0:
			self.walk = 1
			self.drawPalette(self.oo_walk1)
		if self.walk == 1:
			self.walk = 2
			self.drawPalette(self.oo_normal)
		if self.walk == 2:
			self.walk = 3
			self.drawPalette(self.oo_walk2)
		if self.walk == 3:
			self.walk = 0
			self.drawPalette(self.oo_normal)

	def ooWalk(self):
		if self.count > 0:
			self.count -= 1
		else:
			self.count = 5
			self.pos().x
			self.pos().y
			centerx = self.screenWidth/2
			centery = self.screenHeight/2
			diffx = self.pos().x() - centerx
			diffy = self.pos().y() - centery
			self.move(diffx/10,diffy/10)
			self.walkChange()

	def timerFire(self): 
		# OO Animation render
		if self.follow_mouse:
			self.freewalk = 5000
			if not self.angry1:
				self.drawPalette(self.oo_angry1)
				self.angry1 = True
			else:
				self.drawPalette(self.oo_angry2)
				self.angry1 = False
		else:
			if self.freewalk > 0: self.freewalk -= 10
			if self.freewalk <= 0: self.ooWalk() 
			else: self.freewalk = False
			if self.oo_state == 0: self.drawPalette(self.oo_normal)
			else: self.drawPalette(self.oo_toothache)

		# Check file collision
		if self.follow_mouse:
			if sys.platform == "win32":
				count = desktop.desktop_intersect(self.pos().x(), self.pos().y(),
						self.width, self.height)
				if count != 0:
					print((self.pos().x(), self.pos().y(),
							self.width, self.height))
					print(count)


	#When press left button of mouse, bind the position of mouse and desktop pet 
	def mousePressEvent(self,event):
		if event.button() == QtCore.Qt.LeftButton:
			self.follow_mouse = True
			self.mouse_drag_pos = event.globalPos() - self.pos()
			event.accept()

		if event.button() == QtCore.Qt.RightButton:
			self.follow_mouse = False
			self.oo_state = random.randint(0, 1)
			self.freewalk = 5000
			self.walk = False
			event.accept()


	#When the mouse move, desktop pet moves
	def mouseMoveEvent(self, event):
		if self.follow_mouse:
			self.move(event.globalPos() - self.mouse_drag_pos)
			event.accept()

	def randomPosition(self):
		screen_geo = self.app.primaryScreen().size()
		pet_geo = self.geometry()
		width = int((screen_geo.width() - pet_geo.width()) * random.random())
		height = int((screen_geo.height() - pet_geo.height()) * random.random())
		self.move(width, height)
	

	def closeEvent(self, event):
		quit()

	def quit(self):
		self.animation.stop()
		self.close()
		sys.exit()

if __name__ == '__main__':
	app = QtWidgets.QApplication([]) #app = QApplication(sys.argv)?
	qwqWidget = QwQWidget(app) #pet = QwQWidget()
	sys.exit(app.exec())
