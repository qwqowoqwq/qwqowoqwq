import random
import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class QwQWidget(QtWidgets.QWidget):

    def __init__(self, app):
        super().__init__()

        screenSize = app.primaryScreen().size()
        self.screenWidth = screenSize.width()
        self.screenHeight = screenSize.height()
        self.left = self.screenWidth - 400
        self.top = self.screenHeight - 400
        self.width = 300
        self.height = 300

        self.follow_mouse = False
        self.mouse_drag_pos = self.pos()
        self.randomPosition()
		self.show()

        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.Tool)
        self.setGeometry(self.left, self.top, self.width, self.height)
        pic = QtWidgets.QLabel(self)
        pic.setPixmap(QtGui.QPixmap("image.png"))
        pic.show()
        self.show()
    
        
    #When press left button of mouse, bind the position of mouse and desktop pet 
    def mousePress(self,event):
        if event.button() == Qt.LeftButton:
            self.follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))

    #When the mouse move, desktop pet moves
    def mouseMoveEvent(self, event):
		if Qt.LeftButton and self.follow_mouse:
			self.move(event.globalPos() - self.mouse_drag_pos)
			event.accept()

    #When release mouse, cancel binding
	def mouseReleaseEvent(self, event):
		self.is_follow_mouse = False
		self.setCursor(QCursor(Qt.ArrowCursor))

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
		pet_geo = self.geometry()
		width = (screen_geo.width() - pet_geo.width()) * random.random()
		height = (screen_geo.height() - pet_geo.height()) * random.random()
		self.move(width, height)

    
    def quit(self):
		self.close()
		sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication([]) #app = QApplication(sys.argv)?
    qwqWidget = QwQWidget(app) #pet = QwQWidget()
    sys.exit(app.exec())
