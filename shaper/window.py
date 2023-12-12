from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .canvas import *
from .tools import TOOLS
from .modal.generic import GenericModal
from .modal.attr_modal import AttrModal
from .modal.export_modal import ExportModal

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.mesh = [None]
        self.mesh_info = [None]
        self.export_type = [None]
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
        elif a.text() == "select":
            self.canvas.setState("select")
        elif a.text() == "square":
            self.canvas.setState("square")
        elif a.text() == "mesh":
            self.modal(self.mesh, GenericModal)
            self.update_mesh()
        elif a.text() == "attrinfo":
            self.modal(self.mesh_info, AttrModal)
            infos = self.mesh_info[0]
            self.canvas.setMeshAttrs(
                infos.temperature.value(),
                infos.is_fixed.checkState(),
                infos.force_value.value(),
                infos.force_direction_values(),
            )
        elif a.text() == "export":
            self.modal(self.export_type, ExportModal)
            infos = self.export_type [0]
            archiev_name = infos.archiev_name.text()
            if infos.data_type.currentText() == "Calor":
                self.canvas.export_temperature(archiev_name)
                self.canvas.run_temperature()
            elif infos.data_type.currentText() == "Particulas":
                self.canvas.export_particle(archiev_name)
                self.canvas.run_particle()


    def modal(self, var, modal_class):
        if var[0] is None:
            var[0] = modal_class(self)
        else:
            var[0].exec_()

    def update_mesh(self):
        value = self.mesh[0].input.value()
        self.canvas.setMesh(value)
            
    def keyPressEvent(self, event):
        if event.key() == 16777248:
            self.canvas.shift = True
    
    def keyReleaseEvent(self, event):
        if event.key() == 16777248:
            self.canvas.shift = False
