import os

'''
使用os模块可以获取指定文件夹下所有文件名，有两个方法os.walk()和os.listdir().

(1)os.walk可以用于遍历指定文件下所有的子目录、非目录子文件。
(2)os.listdir()用于返回指定的文件夹下包含的文件或文件夹名字的列表，这个列表按字母顺序排序。
'''
file_dir = r'D:\SpiderProjects\Code\os_operate'
#=================================返回指定路径下所有文件和子文件夹中所有文件列表
def file_name_walk(file_dir):
    for root, dirs, files in os.walk(file_dir, topdown=False):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前目录下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        print(root,dirs,files)
# file_name_walk(file_dir)
file_name_walk("./")


#================================返回指定路径下所有的文件和文件夹列表,但是子目录下文件不遍历。
def file_name_listdir(file_dir):
    for files in os.listdir(file_dir):  # 不仅仅是文件，当前目录下的文件夹也会被认为遍历到
            print("files", files)
# file_name_listdir("./")