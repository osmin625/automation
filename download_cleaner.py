import os
from pathlib import Path
from filecmp import cmp
import pprint
class User:
    def __init__(self, threshold = 10):
        self.user_name = self.__set_user_name()
        self.download_path = self.__set_download_path()
        self.threshold = threshold
    def __set_user_name(self):
        return os.getenv('username')

    def __set_download_path(self):
        return os.path.join('\\Users',self.user_name,'Downloads')

    def make_folders(self,exts):
        for ext in exts:
            dir_path = os.path.join(self.download_path,ext)
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)

    def get_file_list(self):
        list_ = os.listdir(self.download_path)
        files = []
        dirs = []
        # TODO: 폴더 예외처리
        # 폴더의 경우 폴더 내부의 파일을 확인하여 해당 파일에 맞게 분류하자.

        for f in list_:
            file_path = os.path.join(self.download_path,f)
            if os.path.isdir(file_path):
                dirs.append(f)
                continue
            files.append(f)

        ext_dir = {}
        for f in files:
            fname, ext = os.path.splitext(f)
            ext = ext.lstrip('.')
            if not ext_dir.get(ext):
                ext_dir[ext] = []
            ext_dir[ext].append(fname)
        
        len_dir = sorted(map(lambda x:(x[0],len(x[1])),ext_dir.items()),reverse=True)
        ext_dir['기타'] = []
        etc_dir = {}
        for key, val in len_dir:
            if val < self.threshold:
                ext_dir['기타'].extend(ext_dir.get(key))
                for i in ext_dir.pop(key):
                    if not etc_dir.get(i):
                        etc_dir[i] = []
                    etc_dir[i].append(key)
        return ext_dir, etc_dir
    # TODO: 중복 제거하기
    # TODO: 폴더명 직관적으로 변경하기
def move_file(path, ext, fname):
    src = os.path.join(path, fname)
    dest = os.path.join(path, ext, fname)
    os.rename(src,dest)

user = User()
ext_dir, etc_dir = user.get_file_list()
# pprint.pprint(ext_dir)
# folder_names = [f'{name}_확장자_{cnt}개' for name, cnt in zip(ext_dir.keys(),map(len,ext_dir.values()))]
folder_names = ext_dir.keys()
user.make_folders(folder_names)
for ext, files in ext_dir.items():
    for file in files:
        if ext == '기타':
            fname = f'{file}.{etc_dir[file].pop()}'
        else:
            fname = f'{file}.{ext}'
        try:
            move_file(user.download_path, ext,fname)
        except Exception as e:
            print(e)

# TODO: precommit 추가하기 - black, linter
# TODO: Refactoring하기.