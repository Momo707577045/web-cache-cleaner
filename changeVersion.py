# -*- coding: utf-8 -*-
import hashlib
import os
import re
import sys

fileMap = {}  # 文件名与 hash 的映射
targetPath = sys.argv[1]


# 计算文件 hash 值
def calcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


# 获取各个文件的哈希值
def getHash():
    # root 表示当前正在访问的文件夹路径 # dirs 表示该文件夹下的子目录名list # files 表示该文件夹下的文件list
    for root, dirs, files in os.walk(targetPath):
        for fileName in files:
            fileMap[fileName] = calcMD5(os.path.join(root, fileName))


# 添加链接的 hash 值
def addHash(filepath):
    with open(filepath, 'r+') as file:
        fileContent = file.read()

        def changeURL(matched):
            fileName = matched.group()
            version = fileMap.get(fileName[:-1], 'null')
            if (version == 'null'): return fileName
            if (fileName[-1] == '?'):
                return fileName + 'version=' + version + '&'
            else:
                return fileName[:-1] + '?version=' + version + fileName[-1]

        result = re.sub('([^/]+\.js[\'"?])|([^/]+\.html[\'"?])|([^/]+\.css[\'"?])|([^/]+\.png[\'"?])|([^/]+\.jpg[\'"?])|([^/]+\.jpeg[\'"?])', changeURL, fileContent)
        file.seek(0)
        file.truncate()  # 清空文件
        file.write(result)


# 修改各文件中各资源链接
def readAll():
    for root, dirs, files in os.walk(targetPath):
        for fileName in files:
            if (re.match(r'.*\.html|.*\.js|.*\.css', fileName, re.I) and not re.match(r'.*min.*', fileName, re.I)):
                print (os.path.join(root, fileName))
                addHash(os.path.join(root, fileName))


print (targetPath)
getHash()
readAll()
print('changeVersion finish')