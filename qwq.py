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

    def closeEvent(self, event):
        event.ignore()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    qwqWidget = QwQWidget(app)
    sys.exit(app.exec())
