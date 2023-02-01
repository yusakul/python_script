import os
import zipfile
import sys
from bs4 import BeautifulSoup
import re
import csv

'''
处理一般的chm木马，利用控件adb880a6-d8ff-11cf-9377-00aa003b7a11
具体为提取htm参数到csv
'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dir_chm = sys.argv[1]
    listpathZip= []

    csvname = 'result.csv'
    csvfile = open(csvname, "w+" ,newline='')
    filednames = ['Hash','htmName', 'classid','PARAM1','PARAM2','PARAM3','PARAM4',
                  'value1','value2','value3','value4','url']

    writer = csv.DictWriter(csvfile, fieldnames=filednames)
    writer.writeheader()

    list_dochtm = []

    classid=''

    # 解压chm 文件名称为hash
    for file_name in os.listdir(dir_chm): # list hash
        print(file_name)
        listpathZip.append(dir_chm+'/'+file_name)
        dst_path=dir_chm + '/' + file_name
        cmd = "hh -decompile ./out/" + file_name + ' ' +  dst_path
        res = os.system(cmd)

        dst_path = "./out/" + file_name + '/'
        try:
            for htm_name in os.listdir(dst_path):
                if '.htm' in htm_name:
                    list_dochtm.append(dst_path +htm_name)
        except:
            continue



    for file_name in list_dochtm:

        tmpfs = open(file_name, 'r')
        tmpdata = tmpfs.read()
        if 'document.write(unescape(' in tmpdata:
            tmpfs2 = open('other.txt', 'a+')
            tmpfs2.write(file_name+" need unescape\n")
            continue
        tmpfs.close()

        url = ''

        soup = BeautifulSoup(open(file_name), features="html.parser")  # html.parser是解析器，也可是lxml
        object=  soup.body.object
        print(soup.body.object)

        try:
            sttt = str(object).replace('^','')
            url= re.search(r'http([^\s]+)', sttt).group()
            url = url.split('"')[0]
            print(url)
        except Exception as e:
            print(e)

        try:
            classid = object.attrs['classid']
            #classid = re.match(r'[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', sttt)
            print(classid)
        except Exception as e:
            print(e)
            # 没有clsid
            continue


        list_name=[]
        list_value=[]
        list_contents = object.contents

        i=0
        for content in list_contents:
            if content == '\n':
                list_contents.pop(i)
            i=i+1

        for content in list_contents:
            print(content)
            list_name.append(content['name'])
            list_value.append(content['value'])

            # csvfile.write("Hash,classid,PARAM1,PARAM2,PARAM3,PARAM4,value1,value2,value3,value4,url\n")

        if len(list_name)==3:
            writer.writerow({'Hash':file_name.split('./out/')[1].split('/')[0],
                             'htmName':file_name.split('./out/')[1].split('/')[1], 'classid': classid,
                             'PARAM1': list_name[0], 'PARAM2': list_name[1],
                             'PARAM3': list_name[2], 'value1': list_value[0],
                             'value2': list_value[1], 'value3': list_value[2], 'url':url})
        if len(list_name) == 4:
            writer.writerow({'Hash':file_name.split('./out/')[1].split('/')[0],
                             'htmName':file_name.split('./out/')[1].split('/')[1],
                             'classid':classid,
                             'PARAM1': list_name[0], 'PARAM2': list_name[1],
                             'PARAM3': list_name[2], 'PARAM4': list_name[3],
                             'value1': list_value[0], 'value2': list_value[1],
                             'value3': list_value[2], 'value4': list_value[3], 'url':url})
