from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox, QVBoxLayout, QLabel

class ExportModal(QDialog):

    def __init__(self, *args, **kwargs) -> None:
        super(ExportModal, self).__init__(*args, **kwargs)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        archiv_label = QLabel("Nome do arquivo para ser salvo:")
        self.archiev_name = QLineEdit()
        sim_type_label = QLabel("Qual tipo de exportação?")
        self.data_type = QComboBox()
        self.data_type.addItem("Calor")
        self.data_type.addItem("Particulas")
        self.layout.addWidget(archiv_label)
        self.layout.addWidget(self.archiev_name)
        self.layout.addWidget(sim_type_label)
        self.layout.addWidget(self.data_type)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
