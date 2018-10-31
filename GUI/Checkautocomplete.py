import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   
from PyQt5.QtCore import *

def get_data(model):
    model.setStringList(["completion", "data", "goes", "going", "here"])

if __name__ == "__main__":

    app = QApplication(sys.argv)
    edit = QLineEdit()
    completer = QCompleter()
    edit.setCompleter(completer)

    model = QStringListModel()
    completer.setModel(model)
    get_data(model)

    edit.show()
    sys.exit(app.exec_())