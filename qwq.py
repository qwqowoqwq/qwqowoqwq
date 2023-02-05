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
		self.eat = 0
		self.eatcount = 500
		self.musicplay = False

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
		self.oo_music = QtGui.QImage.scaled(QtGui.QImage("oo_music.png", format = None), self.width, self.height)

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
		elif self.walk == 1:
			self.walk = 2
			self.drawPalette(self.oo_normal)
		elif self.walk == 2:
			self.walk = 3
			self.drawPalette(self.oo_walk2)
		else:
			self.walk = 0
			self.drawPalette(self.oo_normal)

	def ooWalk(self):
		if self.count > 0:
			self.count -= 1
		else:
			self.count = 5
			self.pos().x
			self.pos().y
			centerx = self.screenWidth//2
			centery = self.screenHeight//2
			diffx = centerx - self.pos().x()
			diffy = centery - self.pos().y()
			if diffx >= 10 or diffy >= 10:
				self.move(self.pos().x() + diffx//10, self.pos().y() + diffy//10)
				self.walkChange()

	def timerFire(self): 
		# Check file collision
		if self.follow_mouse:
			if sys.platform == "win32":
				self.eat = desktop.desktop_intersect(self.pos().x(), self.pos().y(),
						self.width, self.height)

		# OO Animation render
		if self.eat != 0: self.eatcount = 500
		if 490 <= self.eatcount <= 500: 
			self.drawPalette(self.oo_openmouth_small)
			self.eatcount -= 1
			return
		elif self.eatcount >= 480: 
			self.drawPalette(self.oo_openmouth_big)
			self.eatcount -= 1
			return
		elif self.eatcount >= 470: 
			self.drawPalette(self.oo_openmouth_small)
			self.eatcount -= 1
			return
		elif self.eatcount > 0: 
			self.eatcount -= 1
			if self.eatcount // 10 % 2 == 0:
				self.drawPalette(self.oo_eat1)
			else: 
				self.drawPalette(self.oo_eat2)
			return
		if self.musicplay:
			self.drawPalette(self.oo_music)
			return
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
			else: 
				self.ooWalk() 
				return
			if self.oo_state == 0: self.drawPalette(self.oo_normal)
			else: self.drawPalette(self.oo_toothache)


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
	
	# def keyPressed(self, keyboard):
	# 	if keyboard.is_pressed(" "):
	# 		print("space detected")
	 
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Space:
			self.music = QtMultimedia.QSound("qhj.wav")
			self.musicplay = True
			self.music.play()
		if event.key() == QtCore.Qt.Key_O:
			self.musicplay = False
			self.music.stop()

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
