import random
import sys
from PyQt5 import QtCore, QtWidgets, QtGui

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
	
	def timerFire(self): 
		if self.follow_mouse:
			if not self.angry1:
				self.drawPalette(self.oo_angry1)
				self.angry1 = True
			else:
				self.drawPalette(self.oo_angry2)
				self.angry1 = False
		else:
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
