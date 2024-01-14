from PyQt5.QtWidgets import QApplication
import sys
from app import *
import generator


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

main()
