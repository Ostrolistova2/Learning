from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QWidget
from PyQt5 import uic
import sys
import logging
import sqlite3
from learnlogic.storage import SubjectStorage


class WindowContent(QWidget):
    def __init__(self, parent, topic_id, topic_name):
        super().__init__()
        self._parent = parent
        self._topic_id = topic_id
        self._topic_name = topic_name
        self.initUI()

    def initUI(self):
        uic.loadUi('content_window.ui', self)
        self.setWindowTitle('Урок по теме:')
        content = self._parent._subject_storage.get_content(self._topic_id)

        if content:
            id_, content_text, content_ex, content_sr, content_kr, self.content_ex_right, self.content_sr_right, self.content_kr_right = content
            self.textEdit_text.setText(content_text)
            self.textEdit_ex.setText(content_ex)
            self.textEdit_sr.setText(content_sr)
            self.textEdit_kr.setText(content_kr)

            self.label_cont.setText(f'Темы : {self._topic_name}')
            # добавить в виджет

            self.cl_button.clicked.connect(self.close)
            self.show()

            print(content)

        self.pushButton_2.clicked.connect(self.check_ex)
        self.pushButton_3.clicked.connect(self.check_sr)
        self.pushButton_5.clicked.connect(self.check_kr)

        self.pushButton.clicked.connect(self.reset_ex)
        self.show()

    def check_sr(self):
        sr_text = self.textEdit_sr.toPlainText()
        if sr_text == self.content_sr_right:
            self.textEdit_sr.setText('ВСЕ ПРАВИЛЬНО!')
        else:
            self.textEdit_sr.setText('Ошибка!')

    def check_kr(self):
        kr_text = self.textEdit_kr.toPlainText()
        if kr_text == self.content_kr_right:
            self.textEdit_kr.setText('ВСЕ ПРАВИЛЬНО!')
        else:
            self.textEdit_kr.setText('Ошибка!')

    def check_ex(self):
        ex_text = self.textEdit_ex.toPlainText()
        # ex_text = ex_text.rstrip().lstrip()
        if ex_text == self.content_ex_right:
            self.textEdit_ex.setText('ВСЕ ПРАВИЛЬНО!')
        else:
            self.textEdit_ex.setText('Ошибка!')
            self.ex_text = ex_text

    def reset_ex(self):
        self.textEdit_ex.setText(self.ex_text)


class WindowTopics(QWidget):
    def __init__(self, parent, subject, grade):
        super().__init__()
        self._parent = parent
        self._subject_id = subject[0]
        self._subject = subject[1]
        self._selected_topic = {}
        self._grade = grade
        self.initUI()

    def initUI(self):
        uic.loadUi('window_topics.ui', self)
        self.setWindowTitle('Темы')
        self.label.setText(f'Темы по предмету {self._subject}')

        print(self._subject_id, self._grade)
        topics = self._parent._subject_storage.get_topics(self._subject_id, self._grade)

        if topics:
            for id_, topic in topics:
                self._selected_topic[topic] = id_
                self.listWidget.addItem(topic)
        else:
            print('Нет тем по выбранному предмету и классу')
        # self.listWidget.selectedItems()[0].text()
        # self._selected_topic[topic] = id_
        self.pushButton.clicked.connect(self.ok_button_t)
        self.show()

    def ok_button_t(self):
        topic_name = self.listWidget.selectedItems()[0].text()
        topic_id = self._selected_topic[topic_name]
        self.win_cont = WindowContent(self._parent, topic_id, topic_name)


class WindowSubjects(QMainWindow):
    def __init__(self, subject_storage):
        super().__init__()
        self._subject_storage = subject_storage
        self._selected_subjects = {}
        self.initUI()

    def initUI(self):
        uic.loadUi('window_subjects.ui', self)

        subjects = self._subject_storage.get_subjects()

        self.subjects_checkboxes = []
        for id_, subject in subjects:
            checkbox = QCheckBox(subject, self)
            self.verticalLayout.addWidget(checkbox)
            self.subjects_checkboxes.append((id_, subject, checkbox))

        self.tabWidget.currentChanged.connect(self.onTabChanged)
        self.okButton.clicked.connect(self.onOkClicked)

        self.show()

    def onTabChanged(self):
        self.listWidgetLessons.clear()
        self._selected_subjects.clear()
        for id_, subject, checkbox in self.subjects_checkboxes:
            if checkbox.checkState() == 2:
                self.listWidgetLessons.addItem(subject)
                self._selected_subjects[subject] = id_

        self.listWidgetLessons.itemClicked.connect(self.onItemChanged)

    def onOkClicked(self):
        subject = self.listWidgetLessons.selectedItems()[0].text()
        i_class = self.comboBox.currentText()

        self.win_topic = WindowTopics(self, (self._selected_subjects[subject], subject), i_class)

    def onItemChanged(self):
        # subject = self.listWidgetLessons.selectedItems()[0].text()
        self.comboBox.clear()
        for i_class in range(1, 12):
            self.comboBox.addItem(str(i_class))


class Grade(QWidget):
    def __init__(self):
        super(self).__init__()
        self.initUI()

    def initUI(self):
        new_window = uic.loadUi('window_2.ui')
        # item = self.listWidgetLessons.currentItem()
        new_window.setWindowTitle("item.text")
        new_window.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    conn = sqlite3.connect('db.sqlite3')
    s_storage_log = logging.getLogger('users_storage_log')
    subject_storage = SubjectStorage(conn, s_storage_log)
    window = WindowSubjects(subject_storage)
    # cont_window = WindowContent(window)

    sys.exit(app.exec_())
