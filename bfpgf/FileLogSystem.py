import io
from datetime import datetime


def write_log_with_time(file_path, name, str):
    f = open(file_path + '/' + name + '.txt', 'a', encoding='utf-8')
    f.write(datetime.now().__str__() + ": " + str+'\n')
