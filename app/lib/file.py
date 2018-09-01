from os import listdir
from os.path import join
from uuid import uuid4

class File:
    def __init__(self, dirname: str, name: str = '', ext: str = ''):
        self.dirname = dirname
        self.name = name or File.get_safe_file_name(dirname)
        self.ext = File.get_exist_ext(dirname, name) if name else ext

    def write(self, file):
        self.ext = file.filename.split('.')[-1]
        file.save(str(self))
        return self

    def read(self, mode='r') -> str:
        with open(str(self), mode) as file:
            return file.read()

    def __str__(self) -> str:
        return join(self.dirname, '{}.{}'.format(self.name, self.ext))

    @staticmethod
    def get_safe_file_name(dirname: str) -> str:
        files = list(map(lambda x: x.split('.')[0], listdir(dirname)))
        while True:
            name = str(uuid4())
            if name not in files: break
        return name

    @staticmethod
    def get_exist_ext(dirname: str, filename: str) -> str:
        return {'.'.join(name.split('.')[:-1]): name.split('.')[-1] for name in listdir(dirname)}.get(filename, '')
