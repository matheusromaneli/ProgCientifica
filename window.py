from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from canvas import *
from model import *


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.model = MyModel()
        self.canvas.setModel(self.model)
        tb = self.addToolBar("File")
        fit = QAction(QIcon("icons/fit.png"),"fit",self)
        rotate = QAction(QIcon("icons/fit.jpg"),"rotate",self)
        color = QAction(QIcon("icons/fit.jpg"),"color",self)
        tb.addAction(fit)
        tb.addAction(rotate)
        tb.addAction(color)
        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()