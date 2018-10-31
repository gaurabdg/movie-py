import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   
from PyQt5.QtCore import *
import random

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Movie Search'
        self.top = 350
        self.left = 150
        self.width = 550
        self.height = 400

        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        
        #For Window Size
        self.setGeometry(self.top, self.left, self.width, self.height)

        #For Window Icon
        self.setWindowIcon(QtGui.QIcon("icon2.png")) 
        """
        #For Background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)        
        self.setPalette(p)
        """
        """
        #Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width, self.height)
        """
        """
        #For Logo of Search Engine
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('images.png'))
        self.label.setGeometry(0,-160,550,400)
        """
        #Create Status Bar
        self.statusBar().showMessage('Created by- Gaurab Dasgupta, Kaustabh Welankar, Aman Kumar Jain')

        #Create Search Text
        #central_widget = QWidget(self)              # Create a central widget
        #self.setCentralWidget(central_widget)       # Install the central widget
 
        #grid_layout = QGridLayout(self)         # Create QGridLayout
        #central_widget.setLayout(grid_layout)   # Set this accommodation in central widget
 
        #grid_layout.addWidget(QLabel("  Search       ", self), 0, 0)
        #central_widget.setFont(QtGui.QFont('Times Roman',15))
        """ 
        #Create an input field
        lineEdit = QLineEdit(self)
        strList = ['Python', 'PyQt5', 'Qt', 'Django', 'QML']    # Create a list of words

        # We create QCompleter, in which we establish the list, and also the pointer to the parent
        autocompleter = QCompleter(strList, lineEdit)
        self.lineEdit.setCompleter(autocompleter)        # Set QCompleter in the input field
        #grid_layout.addWidget(lineEdit, 0, 1)   # Add the input field to the grid
        """
        # Create a button in the window
        self.button = QPushButton('Show text', self)
        #self.button.move(20,80)
 
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
 
"""
class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setPen(Qt.white)
        size = self.size()

        qp.setBrush(QColor(240,240,240))
        qp.drawRect(0,0,4800,4400)

        qp.setBrush(QColor(255,255,255))
        qp.drawRect(0,-100,1800,400)
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())