import os
import pickle as pkl


class FileWriter:

    def __init__(self, path):
        """path - путь до файла"""
        if self._check_path(path):
            self.path_ = path
            self.file = None

    @property
    def path(self):
        """является геттером"""
        return self.path_

    @path.setter
    def path_set(self, new_path):
        if new_path[0] == '.':
            new_path = os.path.realpath(new_path)
        """проверяем новый маршрут на доступность"""
        if os.access(new_path, os.F_OK):
            """если маршрут нормальный и файл существует, то добавляем путь в объект (а именно заменяем)"""
            self.path_ = new_path

    @path.deleter
    def path_del(self):
        """Очищаем переменную (и пути больше нет)"""
        self.path_ = None

    # проверка доступа к файлу через модификатор os.F_Ok
    def _check_path(self, path):
        if path[0] == '.':
            # возвращает нормальный путь, если мы через точку обозначили наш каталог
            path = os.path.realpath(path)
        path = os.path.dirname(path)
        return os.path.isdir(path)

    def print_file(self):
        if os.access(self.path_, os.R_OK):
            if self.file.readable():
                return self.file.read()
            else:
                self.file.close()
                self.file = open(self.path_, 'r')
                print(self.file.read())
                self.file.close()
                self.file = None
            return
        else:
            print("I don't know what it's file")
            raise FileExistsError()

    def write(self, some_string):
        if os.access(self.path_, os.W_OK):
            self.file.write(some_string)

    def save_yourself(self, file_name):
        with open(file_name, 'wb') as f:
            pkl.dump(self, f)

    @classmethod
    def load_file_writer(cls, pickle_file):
        with open(pickle_file, 'rb') as f:
            obj = pkl.load(f)
        return obj

    def __enter__(self):
        self.file = open(self.path_, 'a')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is not None and self.file.closed is not False:
            self.file.close()
        self.file = None
