from pydoc_data.topics import topics
import sqlite3
from tabulate import tabulate

class SubjectStorage:
    def __init__(self, conn, log):
        self._conn = conn
        self._cursor = self._conn.cursor()
        self._log = log
        

    def create(self):
        self._cursor.execute("""
            create table if not exists Students(
                id INTEGER PRIMARY KEY, 
                username TEXT UNIQUE,
                firstname TEXT,
                lastname TEXT
        )
        """)
        
        self._cursor.execute("""
                create table if not exists Subjects(
                    id INTEGER PRIMARY KEY,
                    subject TEXT UNIQUE
                )
            """)
        
        self._cursor.execute("""
            create table if not exists Topics(
                id INTEGER PRIMARY KEY,
                topic TEXT, 
                grade INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES Subjects(id)
                )
            """)

        self._cursor.execute("""
            create table if not exists Contents(
                id INTEGER PRIMARY KEY, 
                content_paragraph TEXT,
                content_ex TEXT,
                content_sr TEXT,
                content_kr TEXT,
                content_ex_right TEXT,
                content_sr_right TEXT, 
                topic_id INTEGER NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES Topics(id)
                )
            """)

        self._cursor.execute("""
            create table if not exists Lessons(
                id INTEGER PRIMARY KEY,
                headline TEXT,
                student_id INTEGER NOT NULL,
                content_id INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students(id),
                FOREIGN KEY (content_id) REFERENCES Contents(id)
                )
        """)
        self._conn.commit()
        self._log.info('Cоздана таблица пользователей, статей и комментариев')

    def add_subject(self, name):
        try:
            self._cursor.execute(f"""
                insert into Subjects(subject) values ('{name}');
            """)
        except sqlite3.IntegrityError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            self._conn.commit()
            self._log.info('добавлен предмет')
            return True

    def show_subjects(self):
        try:
            self._cursor.execute("""
                select * from Subjects;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
        else:
            subjects = self._cursor.fetchall()
            print(tabulate(subjects, headers=['id', 'subj_name']))
            self._log.info('Предметы выведены.')

    def add_student(self, username, firstname, lastname):
        try:
            self._cursor.execute(f"""
                insert into Students(username, firstname, lastname) values ('{username}', '{firstname}', '{lastname}');
            """)
        except sqlite3.IntegrityError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            self._conn.commit()
            self._log.info('Студент добавлен')
            return True

    def show_students(self):
        try:
            self._cursor.execute("""
                select * from Students;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
        else:
            students = self._cursor.fetchall()
            print(tabulate(students, headers=['id', 'username', 'firstname', 'lastname']))
            self._log.info('Студенты выведены.')
            return True


    def _get_sb_id(self, subject):
        try:
            self._cursor.execute(f"""
                    select id from Subjects WHERE subject = '{subject}';
                """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return None
        else:
            subj_id = self._cursor.fetchone()
            if subj_id:
                self._log.info('ID предмета получен')
                return subj_id[0]
            else:
                self._log.warning('ай ди предмета не получен')
                return None


    def _get_sb(self):
        try:
            self._cursor.execute(f"""
                select subject from Subjects
            """)
            subjects = self._cursor.fetchall()
        except sqlite3.OperationalError:
            self._log.warning('Таблицы Subjects не существет')
            return None
        else:
            if subjects:
                self._log.info(f'Получаем имена предметов')
                subjects_s = [sb[0] for sb in subjects]
                return subjects_s
            return None

    def _get_st_id(self, username):
        try:
            self._cursor.execute(f"""
                    select id from Students WHERE username = '{username}';
                """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            st_id = self._cursor.fetchone()
            if st_id:
                self._log.info('ID человека получен')
                return st_id[0]
            else:
                self._log.warning('ай ди человека не получен')
                return None

    def add_topic(self, subject, topic, grade):
        try:
            subject_id = self._get_sb_id(subject)
            self._cursor.execute(f"""
                insert into Topics(topic, grade, subject_id) values ('{topic}', {grade}, {subject_id});
            """)
        except sqlite3.IntegrityError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            self._conn.commit()
            self._log.warning('Топики добавлены')
            return True

    def show_topics(self):
        try:
            self._cursor.execute("""
                select * from Topics;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
        else:
            topics_s = self._cursor.fetchall()
            print(tabulate(topics_s, headers=['id', 'Topic', 'Grade', 'Subject']))
            self._log.info('Темы выведены.')

    def _get_top_id(self, topic):
        try:
            self._cursor.execute(f"""
                    select id from Topics WHERE topic = '{topic}';
                """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return None
        else:
            top_id = self._cursor.fetchone()
            if top_id:
                self._log.info('ID темы получен')
                return top_id[0]
            else:
                self._log.warning('ай ди темы не получен')
                return None
    
    def add_content(self, topic, paragraph, ex, sr, kr):
        try:
            top_id = self._get_top_id(topic)
            print('0000000000000000000000000000', top_id)
            self._cursor.execute(f"""
                insert into Contents(content_paragraph, content_ex, content_sr, content_kr, topic_id) values ('{paragraph}', '{ex}', '{sr}', '{kr}', {top_id});
            """)
            print('**************')
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            self._conn.commit()
            self._log.info('Контент добавлен')
            return True

    def show_contents(self):
        try:
            self._cursor.execute("""
                select * from Contents;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
        else:
            content = self._cursor.fetchall()
            print(tabulate(content, headers=['id', 'paragraph', 'ex', 'sr', 'kr', 'Topic_id']))
            self._log.info('Контент выведен.')
    
    def _get_cont_id(self, paragraph):
        try:
            self._cursor.execute(f"""
                    select id from Contents WHERE content_paragraph = '{paragraph}';
                """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return None
        else:
            cont_id = self._cursor.fetchone()
            if cont_id:
                self._log.info('ID контента получен')
                return cont_id[0]
            else:
                self._log.warning('ай ди контента не получчен(')
                return None

    def add_lesson(self, username, content_paragraph, headline):
        try:
            st_id = self._get_st_id(username)
            content_id = self._get_cont_id(content_paragraph)
            print('***', st_id, content_id)
            self._cursor.execute(f"""
                insert into Lessons(headline, student_id, content_id) values ('{headline}', {st_id}, {content_id});
            """)
        except sqlite3.IntegrityError:
            self._log.warning('Таблицы не существует')
            return False
        else:
            self._conn.commit()
            self._log.info('Всё ок, уроки добавлены')
            return True

    def show_lessons(self):
        try:
           self._cursor.execute("""
                select * from Lessons;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
        else:
            lesson = self._cursor.fetchall()
            print(tabulate(lesson, headers=['id', 'Headline', 'student_id', 'content_id']))
            
            self._log.info('Уроки выведены.') 

    def get_subjects(self):
        try:
            self._cursor.execute("""
                select id, subject from Subjects;
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существует')
            return None
        else:
            subjects = self._cursor.fetchall()
            
            self._log.info('Предметы получены')
            if subjects:
                return subjects
            return None
    
    def get_topics(self, subject_id, grade):
        try:
            self._cursor.execute(f"""
                select id, topic from Topics
                WHERE subject_id = {subject_id} and grade = {grade};
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы не существет')
            return None
        else:
            topics = self._cursor.fetchall()
            self._log.info('Темы получены')
            if topics:
                return topics
            return None

    def get_content(self, topic_id):
        try:
            self._cursor.execute(f"""
                select id, content_paragraph, content_ex, content_sr, content_kr from Contents
                WHERE topic_id = {topic_id}
            """)
        except sqlite3.OperationalError:
            self._log.warning('Таблицы с контентом не существует')
            return None
        else:
            content = self._cursor.fetchone()
            self._log.info('пар. получены')
            if content:
                return content
            return None






if __name__ == '__main__':
    # conn = sqlite3.connect('logic/db.sqlite3')
    pass

    # subjects_storage = SubjectStorage(conn, log)
    # subjects_storage.create()
    # subjects_storage.add_subject('Русский язык')
    # subjects_storage.show_subjects()