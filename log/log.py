import logging

log_log = logging.getLogger('lessons_log')
log_log.setLevel(logging.DEBUG)

handler = logging.FileHandler('log/lessons_log.log', encoding='utf-8')

formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')

handler.setFormatter(formatter)

log_log.addHandler(handler)


