import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.setGeometry(360, 250, 1330, 615)

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(lambda _: self._update())
        self.updatebt_lay = QHBoxLayout()
        self.vbox.addLayout(self.updatebt_lay)
        self.updatebt_lay.addWidget(self.update_button)

        self._create_schedule_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="tabletime",
                                     user="admin",
                                     password="admin",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_schedule_tab(self):
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Расписание")
        days = [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота']

        day_tab = QTabWidget(self)

        for i in days:
            day_tab.addTab(self._create_day_table(i.upper()), i)
        day_tab_layout = QVBoxLayout()
        day_tab_layout.addWidget(day_tab)
        self.schedule_tab.setLayout(day_tab_layout)

    def _create_day_table(self, day):
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["id", "Неделя", "День", "Аудитория", "Время", "Teacher_id", "", ""])
        self._update_day_table(table, day)
        return table

    def _update_day_table(self, table, day):
        self.cursor.execute(f"SELECT * FROM timetable WHERE day='{day}' "
                            f"ORDER BY timetable.id")
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            # print(f'i = {i}, r = {r}')
            r = list(r)
            editButton = QPushButton("Edit")
            ed_sql = "UPDATE timetable SET week=%s, day=%s,  room_numb=%s, start_time=%s, teacher_id=%s WHERE id=%s"
            delButton = QPushButton("Delete")
            del_sql = "DELETE FROM timetable WHERE id=%s"
            table.setItem(i, 0,
                          QTableWidgetItem(str(r[0])))
            table.setItem(i, 1,
                          QTableWidgetItem(str(r[1])))
            table.setItem(i, 2,
                          QTableWidgetItem(str(r[2])))
            table.setItem(i, 3,
                          QTableWidgetItem(str(r[3])))
            table.setItem(i, 4,
                          QTableWidgetItem(str(r[4])))
            table.setItem(i, 5,
                          QTableWidgetItem(str(r[5])))
            table.setCellWidget(i, 6, editButton)
            table.setCellWidget(i, 7, delButton)

            editButton.clicked.connect(
                lambda _, num=i, tabl=table, edit=True, sql=ed_sql, tab="timetable":
                self._change_from_table(num, tabl, edit, sql, tab))
            delButton.clicked.connect(
                lambda _, num=i, tabl=table, edit=False, sql=del_sql, tab="timetable":
                self._change_from_table(num, tabl, edit, sql, tab))

        addButton = QPushButton("Add")
        add_sql = "INSERT INTO timetable VALUES (%s, %s, %s, %s, %s, %s)"
        addButton.clicked.connect(
            lambda _, num=len(records), tabl=table, sql=add_sql, tab="timetable": self._add_row(num, tabl, sql, tab))
        table.setCellWidget(len(records), 6, addButton)
        table.resizeRowsToContents()

    def _create_teachers_tab(self):
        self.teachers = QWidget()
        self.tabs.addTab(self.teachers, "Преподаватели")
        table = QTableWidget(self)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["id", "Имя", "Предмет", "Тип", "", ""])

        teachers_tab_layout = QVBoxLayout()
        teachers_tab_layout.addWidget(table)

        self._update_teachers_tab(table)
        self.teachers.setLayout(teachers_tab_layout)

    def _update_teachers_tab(self, table):
        self.cursor.execute(f"SELECT * FROM teacher ORDER BY teacher.id")
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            # print(f'i = {i}, r = {r}')
            r = list(r)
            editButton = QPushButton("Edit")
            ed_sql = "UPDATE teacher SET full_name=%s, subject=%s,  type=%s WHERE id=%s"
            delButton = QPushButton("Delete")
            del_sql = "DELETE FROM teacher WHERE id=%s"
            table.setItem(i, 0,
                          QTableWidgetItem(str(r[0])))
            table.setItem(i, 1,
                          QTableWidgetItem(str(r[1])))
            table.setItem(i, 2,
                          QTableWidgetItem(str(r[2])))
            table.setItem(i, 3,
                          QTableWidgetItem(str(r[3])))
            table.setCellWidget(i, 4, editButton)
            table.setCellWidget(i, 5, delButton)

            editButton.clicked.connect(
                lambda _, num=i, tabl=table, edit=True, sql=ed_sql, tab="teacher":
                self._change_from_table(num, tabl, edit, sql, tab))
            delButton.clicked.connect(
                lambda _, num=i, tabl=table, edit=False, sql=del_sql, tab="teacher":
                self._change_from_table(num, tabl, edit, sql, tab))
        addButton = QPushButton("Add")
        add_sql = "INSERT INTO teacher VALUES (%s, %s, %s, %s)"
        addButton.clicked.connect(
            lambda _, num=len(records), tabl=table, sql=add_sql, tab="teacher": self._add_row(num, tabl, sql, tab))
        table.setCellWidget(len(records), 4, addButton)
        table.resizeRowsToContents()

    def _create_subjects_tab(self):
        self.subjects = QWidget()
        self.tabs.addTab(self.subjects, "Предметы")
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Предмет", "", ""])

        subjects_tab_layout = QVBoxLayout()
        subjects_tab_layout.addWidget(table)

        self._update_subjects_tab(table)
        self.subjects.setLayout(subjects_tab_layout)

    def _update_subjects_tab(self, table):
        self.cursor.execute(f"SELECT * FROM subjects")
        records = list(self.cursor.fetchall())
        table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            # print(f'i = {i}, r = {r}')
            r = list(r)
            editButton = QPushButton("Edit")
            delButton = QPushButton("Delete")
            table.setItem(i, 0,
                          QTableWidgetItem(str(r[0])))
            table.setCellWidget(i, 1, editButton)
            table.setCellWidget(i, 2, delButton)
            editButton.clicked.connect(
                lambda _, num=i, tabl=table, old=r[0]: self._change_subjects(num, table, old))
            delButton.clicked.connect(
                lambda _, num=i, tabl=table: self._delete_subjects(num, table))

        add_sql = "INSERT INTO subjects VALUES (%s)"
        addButton = QPushButton("Add")
        addButton.clicked.connect(
            lambda _, num=len(records), tabl=table, sql=add_sql, tab='subjects': self._add_row(num, tabl, sql, tab))
        table.setCellWidget(len(records), 1, addButton)
        table.resizeRowsToContents()

    def _change_subjects(self, rowNum, table, old):
        row = list()
        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"SELECT * FROM teacher WHERE subject=%s", (old,))
            records = list(self.cursor.fetchall())
            self.cursor.execute("DELETE FROM teacher where subject=%s", (old,))
            self.cursor.execute("UPDATE subjects SET name=%s WHERE name=%s", (row[0], old))
            for e in records:
                r = list(e)
                r[2] = row[0]
                self.cursor.execute("INSERT INTO teacher VALUES (%s, %s, %s, %s)", tuple(r))
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _delete_subjects(self, rowNum, table):
        row = list()
        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"SELECT * FROM teacher WHERE subject=%s", (row[0],))
            records = list(self.cursor.fetchall())
            for e in records:
                self.cursor.execute("DELETE FROM timetable where teacher_id=%s", (e[0],))
            self.cursor.execute("DELETE FROM teacher where subject=%s", (row[0],))
            self.cursor.execute("DELETE FROM subjects where name=%s", (row[0],))
            self.conn.commit()
            table.setRowCount(0)
            self._update_subjects_tab(table)
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _change_from_table(self, rowNum, table, edit, sql, tab):
        row = list()
        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        row.append(row[0])
        row = row[1:]
        if edit:
            try:
                print(row)
                print(rowNum)
                self.cursor.execute(sql, (tuple(row)))
                self.conn.commit()
            except Exception as e:
                QMessageBox.about(self, "Error", str(e))
                self._connect_to_db()
        else:
            try:
                if tab == 'timetable':
                    print(row)
                    self.cursor.execute(sql, (row[-1],))
                    self.conn.commit()
                    table.setRowCount(0)
                    self._update_day_table(table, row[1])
                elif tab == 'teacher':
                    print(row)
                    self.cursor.execute("DELETE FROM timetable where teacher_id=%s", (row[-1],))
                    self.cursor.execute(sql, (row[-1],))
                    self.conn.commit()
                    table.setRowCount(0)
                    self._update_teachers_tab(table)
            except Exception as e:
                print(e)
                QMessageBox.about(self, "Error", str(e))
                self._connect_to_db()

    def _add_row(self, rowNum, table, sql, tab):
        row = list()
        for i in range(table.columnCount() - 2):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print(row)
            if tab == 'timetable':
                self.cursor.execute(f"SELECT  MAX(id) FROM timetable")
                max_id = self.cursor.fetchone()[0] + 1
                if row[0] == '' or row[0] is None or int(row[0]) < max_id:
                    row[0] = max_id
                self.cursor.execute(sql, (tuple(row)))
                self.conn.commit()
                table.setRowCount(0)
                self._update_day_table(table, row[2])
            elif tab == 'teacher':
                print(row)
                self.cursor.execute(f"SELECT  MAX(id) FROM teacher")
                max_id = self.cursor.fetchone()[0] + 1
                if row[0] == '' or row[0] is None or int(row[0]) < max_id:
                    row[0] = max_id
                self.cursor.execute(sql, (tuple(row)))
                self.conn.commit()
                table.setRowCount(0)
                self._update_teachers_tab(table)
            elif tab == 'subjects':
                self.cursor.execute(sql, (tuple(row)))
                self.conn.commit()
                table.setRowCount(0)
                self._update_subjects_tab(table)
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", str(e))
            self._connect_to_db()

    def _update(self):
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
        self._create_schedule_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
