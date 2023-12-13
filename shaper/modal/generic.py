from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QWidget, QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel

class GenericModal(QDialog):

    def __init__(self, *args, **kwargs) -> None:
        super(GenericModal, self).__init__(*args, **kwargs)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Distance of points:")
        self.input = QSpinBox()
        self.input.setValue(80)
        self.input.setMaximum(300)
        self.layout.addWidget(message)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
