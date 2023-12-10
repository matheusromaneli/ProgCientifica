from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QCheckBox, QSpinBox, QDoubleSpinBox, QDialogButtonBox, QVBoxLayout, QLabel

class AttrModal(QDialog):

    def __init__(self, *args, **kwargs) -> None:
        super(AttrModal, self).__init__(*args, **kwargs)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message_temp = QLabel("Temperature:")
        self.temperature = QSpinBox()
        self.temperature.setMinimum(-99)
        message_fix = QLabel("Fixed:")
        self.is_fixed = QCheckBox()
        message_force_value = QLabel("Force value (in N):")
        self.force_value = QSpinBox()
        self.force_value.setMinimum(-99)
        message_force_direction = QLabel("Force direction (x,y):")
        self.force_direction_x = QSpinBox()
        self.force_direction_x.setMinimum(-99)
        self.force_direction_y = QSpinBox()
        self.force_direction_y.setMinimum(-99)

        self.layout.addWidget(message_temp)
        self.layout.addWidget(self.temperature)
        
        self.layout.addWidget(message_fix)
        self.layout.addWidget(self.is_fixed)

        self.layout.addWidget(message_force_value)
        self.layout.addWidget(self.force_value)

        self.layout.addWidget(message_force_direction)
        self.layout.addWidget(self.force_direction_x)
        self.layout.addWidget(self.force_direction_y)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.exec_()

    def force_direction_values(self):
        return (self.force_direction_x.value(), self.force_direction_y.value())