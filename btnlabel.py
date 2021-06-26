from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
import sys
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self. setWindowTitle("Quantum Simulator")
        self.setWindowIcon(QIcon("./images/icon.jpg"))
        self.setGeometry(300, 300, 900, 700)
        
        self.create_widgets()

    def create_widgets(self):
        btn = QPushButton("Click Me", self)
        #btn.move(100, 100)
        btn.setGeometry(100,100,100,100)
        btn.setStyleSheet('background-color:red')
        btn.setIcon(QIcon('./images/Y.jpg'))

        btn.clicked.connect(self.clicked_btn)

        self.label = QLabel("Label", self)
        #self.label.move(100,200)
        self.label.setGeometry(100,220,200,100)

        self.label.setStyleSheet('color:green')

    def clicked_btn(self):
        self.label.setText("Text has changed")
        self.label.setStyleSheet('background-color:red')


app = QApplication([])
window = Window()

window.show()

sys.exit(app.exec())