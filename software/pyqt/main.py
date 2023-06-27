from PyQt5.QtWidgets import QApplication
import sys
from app import *

def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

if __name__ == "__main__":
    main()