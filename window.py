from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from canvas import *
from tools import TOOLS

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        tb = self.addToolBar("File")

        for tool in TOOLS:
            new_action = QAction(QIcon("assets/"+tool["asset"]), tool["name"], self)
            tb.addAction(new_action)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "curve":
            self.canvas.setState("curve")
