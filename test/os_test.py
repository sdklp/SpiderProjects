import os

file_list=os.listdir(r'D:\SpiderProjects\book')
# for d in file_list:
    # print(d)


# current_address = os.path.dirname(os.path.abspath(__file__))
current_address =r'D:\SpiderProjects\test'
for parent, dirnames, filenames in os.walk(current_address):
     # Case1: traversal the directories
     for dirname in dirnames:
        print("Parent folder:", parent)
        print("Dirname:", dirname)
     # Case2: traversal the files
     # for filename in filenames:
     #     print("Parent folder:", parent)
     #     print("Filename:", filename)