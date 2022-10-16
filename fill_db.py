import sqlite3
import logging
# import log.log

from learnlogic.storage import SubjectStorage


if __name__ == '__main__':
    logger = logging.getLogger('lessons_log')
    conn = sqlite3.connect('db.sqlite3')

    subject_storage = SubjectStorage(conn, logger)
    subject_storage.create()

    subject_storage.add_subject('Математика')
    subject_storage.add_subject('Русский язык')
    subject_storage.add_subject('Английский язык')
    subject_storage.add_subject('Физика')
    subject_storage.add_subject('История')
    subject_storage.add_subject('Биология')
    subject_storage.add_subject('Химия')
    subject_storage.add_subject('Литература')
    subject_storage.add_subject('Физическая культура')
    subject_storage.add_subject('Информатика')
    subject_storage.add_subject('Немецкий язык')
    subject_storage.add_subject('Алгебра')
    subject_storage.add_subject('Геометрия')
    subject_storage.add_subject('Музыка')
    subject_storage.show_subjects()

    subject_storage.add_student('peeee', 'petr', 'petrov')
    subject_storage.add_student('ooo', 'olga', 'olegovna')
    subject_storage.add_student('mm', 'Masha', 'orlova')
    subject_storage.add_student('no', 'nora', 'sheggg')
    subject_storage.add_student('zero', 'hero', 'lemon')
    subject_storage.show_students()

    print(subject_storage._get_sb_id('Математика'))
    print(subject_storage._get_st_id('ooo'))

    subject_storage.add_topic('Математика', 'Что изучает математика?', 1)
    subject_storage.add_topic('Физика', 'Некоторые физические термины', 7)
    subject_storage.add_topic('Английский язык', 'Алфавит', 2)
    subject_storage.add_topic('Русский язык', 'Слоги и ударение', 1)
    subject_storage.add_topic('Алгебра', 'Координатная плоскость', 7)
    subject_storage.add_topic('Химия', 'Кислород', 7)
    subject_storage.add_topic('Геометрия', 'Треугольники', 8)
    subject_storage.add_topic('Литература', 'Война и мир', 10)
    subject_storage.add_topic('Биология', 'Скелет человека', 8)
    subject_storage.add_topic('Музыка', 'Ромео и Джульета', 7)
    subject_storage.add_topic('Немецкий язык', 'Спряжения глаголов', 5)
    subject_storage.add_topic('Информатика', 'Системы счисления', 8)
    subject_storage.add_topic('История', 'Мастерская мира', 9)
    subject_storage.add_topic('Геометрия', 'Четыре замечательные точки', 8)
    subject_storage.add_topic('Алгебра', 'Схема Горнера', 9)
    subject_storage.add_topic('Химия', 'Углерод', 9)
    subject_storage.add_topic('Информатика', 'Функции', 10)
    subject_storage.add_topic('Алгебра', 'Пропорция', 5)
    subject_storage.show_topics()

    subject_storage.add_content('Что изучает математика?', '_____________текст по теме Что изучает математика?____________')
    # subject_storage.add_content('Пропорция', '_________________ТЕКСТ О ПРОПОРЦИЯХ_______________')
    # subject_storage.add_content('Пропорция', '_________________ВИДЕО О ПРОПОРЦИЯХ_______________')
    # subject_storage.add_content('Пропорция', '_________________СР ПО ПРОПОРЦИЯМ 1_______________')
    # subject_storage.add_content('Схема Горнера', '_________________ТЕКСТ О ГОРНЕРА_______________')
    # subject_storage.add_content('Спряжения глаголов', '_________________ТЕКСТ О СПРЯЖЕНИИ ГЛАГОЛОВ_______________')
    # subject_storage.add_content('Мастерская мира', '_________________ТЕКСТ О МАСТЕРСКОЙ МИРА_______________')
    # subject_storage.add_content('Системы счисления', '_________________ТЕКСТ О СС_______________')
    # subject_storage.add_content('Системы счисления', '_________________ВИДЕО О СС_______________')
    # subject_storage.add_content('Углерод', '_________________ТЕКСТ ОБ УГЛЕРОДЕ_______________')
    # subject_storage.add_content('Углерод', '_________________ВИДЕО ОБ УГЛЕРОДЕ_______________')
    # subject_storage.add_content('Функции', '_________________ТЕКСТ О ФУНКЦИЯХ_______________')
    # subject_storage.add_content('Функции', '_________________ВИДЕО О ФУНКЦИЯХ_______________')
    # subject_storage.add_content('Война и мир', '_________________ТЕКСТ О ВОЙНЕ И МИР_______________')
    # subject_storage.add_content('Война и мир', '_________________ВИДЕО О ВОЙНЕ И МИр_______________')
    # subject_storage.add_content('Война и мир', '_________________АНАЛИЗ_______________')
    # subject_storage.add_content('Спряжения глаголов', '_________________ТЕКСТ О СПРЯЖЕНИИ ГЛАГОЛОВ_______________')
    # subject_storage.add_content('Спряжения глаголов', '_________________ВИДЕО О СПРЯЖЕНИИ ГЛАГОЛОВ_______________')
    # subject_storage.add_content('Спряжения глаголов', '_________________УПРАЖНЕНИЯ НА СПРЯЖЕНИЕ ГЛАГОЛОВ_______________')
    # subject_storage.show_contents()
    
    # subject_storage.add_lesson('ooo', '_________________ТЕКСТ О ПРОПОРЦИЯХ_______________', 'Урок1')
    # subject_storage.show_lessons()

    # print(subject_storage.get_subjects())
    print(subject_storage.get_topics(1, 1))
    print(subject_storage.get_content(1))

    