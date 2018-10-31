import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   
from PyQt5.QtCore import *
import random
from query import predict
import json
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Movie Search'
        self.top = 350
        self.left = 150
        self.width = 650
        self.height = 400

        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        
        #For Window Size
        self.setGeometry(self.top, self.left, self.width, self.height)

        #For Window Icon
        self.setWindowIcon(QtGui.QIcon("GUI/icon2.png")) 

        #For Background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)        
        self.setPalette(p)
        
        #For Logo of Search Engine
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('GUI/images.png'))
        self.label.setGeometry(50,-140,550,400)

        #Create Status Bar
        self.statusBar().showMessage('Created by- Gaurab Dasgupta, Kaustabh Welankar, Aman Kumar Jain')

        #Create Search Text Label
        self.central_widget = QWidget(self)              # Create a central widget
        self.setCentralWidget(self.central_widget)       # Install the central widget
 
        self.grid_layout = QGridLayout(self)         # Create QGridLayout
        self.central_widget.setLayout(self.grid_layout)   # Set this accommodation in central widget
 
        self.grid_layout.addWidget(QLabel("  Query       ", self), 0, 0)
        self.central_widget.setFont(QtGui.QFont('Times Roman',15))
 
        # Create an input field for Search Box
        self.lineEdit = QLineEdit(self)
        self.strList = []    # Create a list of words
        with open("clean_data/stats.csv",'r') as f:
            index = json.loads(f.readline())
        for m in index:
            for t in index[m]:
                self.strList.append(t)
        self.strList = set(self.strList)
        self.strList = list(self.strList)
        # Create AutoComplete feature
        # We create QCompleter, in which we establish the list, and also the pointer to the parent
        self.autocompleter = QCompleter(self.strList, self.lineEdit)
        self.lineEdit.setCompleter(self.autocompleter)        # Set QCompleter in the input field
        self.grid_layout.addWidget(self.lineEdit, 0, 1)   # Add the input field to the grid

        # Create SEARCH button in the window
        self.button1 = QPushButton('Search', self)
        self.button1.move(200,220)
        self.button1.setToolTip("Press this to get Results")
 
        # connect SEARCH button to function SearchQuery
        self.button1.clicked.connect(self.SearchQuery)

        # Create QUIT button in the window
        self.button2 = QPushButton('Quit',self)
        self.button2.move(320,220)
        self.button2.setToolTip("This closes the Application")

        # Connect QUIT button to funtion CloseApp
        self.button2.clicked.connect(self.CloseApp)


        self.show()
 
    #@pyqtSlot()
    def SearchQuery(self):
        queryText = self.lineEdit.text()
        res = predict("clean_data", queryText)
        #print(queryText)
        self.SW = SecondWindow()
        print(type(res))
        self.SW.setText(res)
        self.SW.show()
        
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are you sure to exit the application",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()




class SecondWindow(QMainWindow):
    def __init__(self, *args,**kwargs):    
        super().__init__()
        self.title = 'Results'
        self.top = 950
        self.left = 150
        self.width = 550
        self.height = 400
        self.toDisplay = ["Banana"]
        self.initUI()
        self.lbl = QLabel("",self)
        self.lbl.resize(300,300)
        self.lbl.move(30,0)
        

    def initUI(self):
        self.setWindowTitle(self.title)
        
        #For Window Size
        self.setGeometry(self.top, self.left, self.width, self.height)

        #For Window Icon
        self.setWindowIcon(QtGui.QIcon("icon2.png"))

        #For Background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)        
        self.setPalette(p)

        #Show result box
        strToDisplay = "These are the results of the search query"
        
        for r in self.toDisplay:
            strToDisplay = strToDisplay +"\n"+ (r[:-4])
        #self.lbl = QLabel(strToDisplay,self)
        #self.lbl.resize(300,300)
        #self.lbl.move(30,-100)
        
        #Create close button
        self.button3 = QPushButton('OK',self)
        self.button3.move(300,250)
        self.button3.setToolTip("Click to search a different query")
        
        self.button3.clicked.connect(self.CloseApp)

    def CloseApp(self):
        self.close()

    def setText(self,arr):
        self.toDisplay = arr
        print(type(arr))
        #Show result box
        strToDisplay = "These are the results of the search query"
        
        for i,r in enumerate(self.toDisplay):
            strToDisplay = strToDisplay +"\n\n"+ str(i+1) +". "+ r[:-4]
        self.lbl.setText(strToDisplay)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())