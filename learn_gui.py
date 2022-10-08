from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QWidget
from PyQt5 import uic
import sys
import logging
import sqlite3
from learnlogic.storage import SubjectStorage

class WindowContent(QWidget):
    def __init__(self, parent, topic_id):
        super().__init__()
        self._parent = parent
        self._topic_id = topic_id
        self.initUI()

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
        
        for id_, topic in topics:
            self.listWidget.addItem(topic)
        # self.listWidget.selectedItems()[0].text()
        # self._selected_topic[topic] = id_
        self.show()
    
    def click_top(self):
        self.ListWidget.itemClicked.connect(self.ok_button_t)

    def ok_button_t(self):
        self.win_cont = WindowContent(self, self._selected_topic)

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
        subject = self.listWidgetLessons.selectedItems()[0].text()
        self.comboBox.clear()
        for i_class in range(1, 12):
            self.comboBox.addItem(str(i_class))
        

class Grade(QWidget):
    def __init__(self):
        super(self).__init__()
        self.initUI()

    def initUI(self):
        new_window = uic.loadUi('window_2.ui') 
        item = self.listWidgetLessons.currentItem()
        new_window.setWindowTitle("item.text")
        new_window.show()

    
if __name__ == '__main__':

    app = QApplication(sys.argv)
    conn = sqlite3.connect('db.sqlite3')
    s_storage_log = logging.getLogger('users_storage_log')
    subject_storage = SubjectStorage(conn, s_storage_log)
    window = WindowSubjects(subject_storage)

    sys.exit(app.exec_())

