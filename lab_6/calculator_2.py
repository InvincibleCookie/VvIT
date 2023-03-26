import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt


class Calculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Калькулятор')
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignRight)
        self.input.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.input)

        buttons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['0', '.', '/', 'C'],
            ['=']
        ]

        for row in buttons:
            hbox = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text)
                button.clicked.connect(self.buttonClicked)
                hbox.addWidget(button)
            vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.show()

    def buttonClicked(self):
        button = self.sender()
        if button.text() == '=':
            try:
                if int(eval(self.input.text())) == float(eval(self.input.text())):
                    self.input.setText(str(int(eval(self.input.text()))))
                else:
                    self.input.setText(str(eval(self.input.text())))
            except ZeroDivisionError:
                self.input.setText('Деление на ноль')
            except:
                pass
        elif button.text() == 'C':
            self.input.setText('')
        else:
            self.input.setText(self.input.text() + button.text())

    def clearClicked(self):
        self.input.setText('')


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
