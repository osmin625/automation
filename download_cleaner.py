import os
from pathlib import Path
from filecmp import cmp
class User:
    def __init__(self, categories):
        self.user_name = self.__set_user_name()
        self.download_path = self.__set_download_path()
        self.categories = categories
    def __set_user_name(self):
        return os.getenv('username')

    def __set_download_path(self):
        return f'/Users/{self.user_name}/Downloads'

    def make_folders(self,categories):
        for cat in categories:
            dir_path = os.path.join(self.download_path,cat)
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
    
categories = ['사진', '실행 파일', '서류', '압축 파일', '폴더 파일', '기타']
user = User(categories)
user.make_folders()
