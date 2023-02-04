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
		self.mouse_drag_pos = self.pos()
		self.show()

		self.initUI()

	def initUI(self):
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
		QtCore.Qt.FramelessWindowHint |
		QtCore.Qt.Tool)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.randomPosition()
		pic = QtWidgets.QLabel(self)
		pic.setPixmap(QtGui.QPixmap(QtGui.QImage("oo_normal", format = None)))
		pic.show()
		self.show()


	#When press left button of mouse, bind the position of mouse and desktop pet 
	def mousePressEvent(self,event):
		if event.button() == QtCore.Qt.LeftButton:
			self.follow_mouse = True
			self.mouse_drag_pos = event.globalPos() - self.pos()
			event.accept()

		if event.button() == QtCore.Qt.RightButton:
			self.follow_mouse = False
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
	

	def closeEvent(self):
		quit()

	def quit(self):
		self.close()
		sys.exit()

if __name__ == '__main__':
	app = QtWidgets.QApplication([]) #app = QApplication(sys.argv)?
	qwqWidget = QwQWidget(app) #pet = QwQWidget()
	sys.exit(app.exec())
