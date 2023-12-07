import sys
from shaper.window import *

def main():
    app = QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()