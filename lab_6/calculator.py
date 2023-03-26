import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowTitle('Калькулятор')
        self.input = QLineEdit()
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
                if button_text in ['+', '-', '*', '/']:
                    button.clicked.connect(lambda _, op=button_text: self._operation(op))
                elif button_text == '.':
                    button.clicked.connect(lambda: self._point())
                elif button_text == '=':
                    button.clicked.connect(lambda: self._result())
                elif button_text == 'C':
                    button.clicked.connect(lambda: self._clear())
                else:
                    button.clicked.connect(lambda _, param=button_text: self._button(param))
                hbox.addWidget(button)
            vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def _button(self, param):
        line = self.input.text()
        self.input.setText(line + param)

    def _operation(self, op):
        try:
            self.num_1 = float(self.input.text())
            self.op = op
        except:
            pass
        self.input.setText("")

    def _point(self):
        if not '.' in self.input.text() and self.input.text():
            self.input.setText(self.input.text() + '.')

    def _clear(self):
        self.input.setText('')

    def _result(self):
        try:
            self.num_2 = float(self.input.text())
            if self.op == "+":
                if float(self.num_1 + self.num_2) == int(self.num_1 + self.num_2):
                    self.input.setText(str(int(self.num_1 + self.num_2)))
                else:
                    self.input.setText(str(self.num_1 + self.num_2))

            elif self.op == "-":
                if float(self.num_1 - self.num_2) == int(self.num_1 - self.num_2):
                    self.input.setText(str(int(self.num_1 - self.num_2)))
                else:
                    self.input.setText(str(self.num_1 - self.num_2))

            elif self.op == "*":
                if float(self.num_1 * self.num_2) == int(self.num_1 * self.num_2):
                    self.input.setText(str(int(self.num_1 * self.num_2)))
                else:
                    self.input.setText(str(self.num_1 * self.num_2))

            elif self.op == "/":
                if self.num_2 != 0:
                    if float(self.num_1 / self.num_2) == int(self.num_1 / self.num_2):
                        self.input.setText(str(int(self.num_1 / self.num_2)))
                    else:
                        self.input.setText(str(self.num_1 / self.num_2))
                else:
                    self.input.setText('Деление на ноль')

        except:
            pass


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
