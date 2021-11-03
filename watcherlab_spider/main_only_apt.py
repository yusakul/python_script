# coding: utf-8
# python3

import json
import os
import random
import re
import shutil
import time
import requests
import urllib3
import csv
from contextlib import closing

urllib3.disable_warnings()

import zipfile


def get_zip(files:list, zip_name):
    zp = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zp.write(file)


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names,file_name + "_files/")
    zip_file.close()

key = 'watcherlab'
base_url = 'https://www.watcherlab.com/threatlib/apt/home/aptnotes'  # url 入口

# 添加 设置浏览器Header
USER_AGENT_LIST = [
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
      "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

pdf_basic_url = "https://www.watcherlab.com/threatlib/feed/anon/pdf/"
headers = {
    'Host': 'www.watcherlab.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    'token': 'null',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.watcherlab.com/index/apt',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

def encodeContent(List, str):
    try:
        ret = List[str].encode('utf-8').decode('GB2312')
    except Exception as err:
        ret = ''
    return ret


class ProgressBar(object):
    def __init__(self, titleCn, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.titleCn = titleCn
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # [名称] 状态 进度 单位 分割线 总数 单位
        _info = self.info % (
        self.titleCn, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
        self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), '\n',)

def formatStr(str):
    str = str.replace(' ', '')
    str = re.findall(r'[^\*"/:?\\|<>]', str, re.S)
    str = "".join(str).encode('utf-8','ignore').decode('utf-8','ignore')
    return str


def downlaod_pdf(index, titleCn, year, count):
    # pdf下载
    pdf_url = pdf_basic_url + index['fileUuid']
    filename_pdf = formatStr(titleCn + '.pdf')
    path_pdf = os.getcwd() + '\\' + year + '\\' + filename_pdf
    with closing(requests.request("GET", pdf_url, headers=headers)) as response:
        chunk_size = 1024
        # content_size = int(response.headers['content-length'])
        content_size = len(response.content)
        if response.status_code == 200:
            print('%s, ' % year, '第%d个, ' % count, '文件名称:%s, ' % filename_pdf,
                  '文件大小:%0.2f KB' % (content_size / chunk_size))
            progress = ProgressBar("%s下载进度" % filename_pdf
                                   , total=content_size
                                   , unit="KB"
                                   , chunk_size=chunk_size
                                   , run_status="正在下载"
                                   , fin_status="下载完成")

            with open(path_pdf, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    # progress.refresh(count=len(data))
                file.close()
        else:
            print('链接异常')

    return filename_pdf

def downloadEvent(year):

    # result
    files_out = year + "_result.csv"
    fo = open(files_out, 'w+', encoding='utf-8', newline='')
    fieldnames = ['titleCn', 'titleCn', 'comment', 'commentCn', 'url', 'time', 'fileUuid', 'iocsUuid', 'vender',
                  'operandi', 'groups', 'region', 'industry', 'toolset', 'malware', 'tags']  # 这是标题栏的内容
    writer = csv.DictWriter(fo, fieldnames=fieldnames)  # 把标题栏加入到csv文件中
    writer.writeheader()  # 这一行是写入第一行的标题栏，放在for循环的外面，不然就会出现很多个标题栏



    url = "https://www.watcherlab.com/threatlib/apt/home/aptnotes"

    payload = json.dumps({
        "type": "year",
        "data": year
    })
    headers = {
        'Host': 'www.watcherlab.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)],
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.watcherlab.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.watcherlab.com/index/apt',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    json1 = json.loads(response.text)
    report_total = json1['data']

    time.sleep(0.5)

    # download ***************************************************************************************************

    # pdf_url = "https://www.watcherlab.com/threatlib/feed/anon/pdf/e7fba351-78ea-4480-84f3-f614314ad999"

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    print('*' * 50)
    print('*' *15 + year + ' Download Start.'+ '*' *15 )
    print('*' * 50)
    # url = input('请输入需要下载的文件链接:\n')

    count = 0
    if os.path.exists(os.getcwd() + '\\' + year):
        shutil.rmtree(os.getcwd() + '\\' + year)  # 空目录、有内容的目录都可以删
    os.mkdir(os.getcwd() + '\\' + year)
    for index in report_total:

        try:
            # group
            group_id = json.dumps(index['groups'])
            alias = ''
            #group_id1 = "[\"2a815198-d67b-441e-8ee4-76cdfa089cc2\"]"
            if len(index['groups']):
                response_groups = requests.request("POST", 'https://www.watcherlab.com/threatlib/apt/home/many/groups', headers=headers, data= group_id)
                json2 = json.loads(response_groups.text)
                groups_json = json2['data']
                if len(groups_json[0]['alias']):
                    alias = groups_json[0]['alias'][0]['alias']
                    print("alias: "+alias)
                    if len(alias)<4:
                        continue
                else:
                    continue
            else:
                continue


            writer.writerow(
                {'titleCn': formatStr(index['titleCn']),
                 'comment': encodeContent(index, 'comment'), \
                 'commentCn': encodeContent(index, 'commentCn'), 'url': encodeContent(index, 'url'),
                 'time': encodeContent(index, 'time'), \
                 'fileUuid': encodeContent(index, 'fileUuid'), 'iocsUuid': encodeContent(index, 'iocsUuid'),
                 'vender': encodeContent(index, 'vender'), \
                 'operandi': encodeContent(index, 'operandi'), 'groups': alias,
                 'region': encodeContent(index, 'region'), \
                 'industry': encodeContent(index, 'industry'), 'toolset': encodeContent(index, 'toolset'),
                 'malware': encodeContent(index, 'malware'), \
                 'tags': encodeContent(index, 'tags')})
        except Exception as err:
            print(err)

        time.sleep(0.5)

        try:
            count += 1

            # 情报数据下载
            if index['iocsUuid']==None:
                print('iocsUuid Null')
                # pdf下载

                titleCn = formatStr(index['titleCn'])
                filename_pdf = downlaod_pdf(index, titleCn, year, count)
                time.sleep(random.randint(4, 10))
                zipfiles = [year + '/' + filename_pdf]
                zip_file = os.getcwd() + '\\' + year + '\\' + formatStr(titleCn) + '.zip'
                get_zip(zipfiles, zip_file)
                os.remove(zipfiles[0])
                continue
            ti_url = "https://www.watcherlab.com/threatlib/feed/anon/manyquery/" +index['iocsUuid']
            #ti_url = 'https://www.watcherlab.com/threatlib/feed/anon/manyquery/42687918-b151-4110-8453-6ce672ddd0a0'
            response_manyquery_ = requests.request("GET", ti_url, headers=headers)
            #print(response.text)
            json_manyquery = json.loads(response_manyquery_.text)
            manyquery = json_manyquery['data']



            ## 情报数据csv
            ip_list=[]
            domain_list=[]
            ssl_list=[]
            email_list=[]
            url_list=[]
            hash_list=[]
            Time = index['time']
            titleCn = formatStr(index['titleCn'])


            try:
                if manyquery['iocs'] != None:
                    if len(manyquery['iocs']['ip']):
                        for ip in manyquery['iocs']['ip']:
                            ip_list.append(ip['basicInfo']['data'])
                    if len(manyquery['iocs']['domain']):
                        for domain in manyquery['iocs']['domain']:
                            domain_list.append(domain['basicInfo']['data'])
                    if len(manyquery['iocs']['ssl']):
                        for ssl in manyquery['iocs']['ssl']:
                            ssl_list.append(ssl['basicInfo']['data'])
                    if len(manyquery['iocs']['email']):
                        for email in manyquery['iocs']['email']:
                            email_list.append(email['basicInfo']['data'])
                    if len(manyquery['iocs']['url']):
                        for url in manyquery['iocs']['url']:
                            url_list.append(url['basicInfo']['data'])
                    if len(manyquery['iocs']['hash']):
                        for hash in manyquery['iocs']['hash']:
                            hash_list.append(hash['basicInfo']['data'])
            except Exception as err_2:
                print(err_2)


            ## yara
            filename_yara = formatStr(titleCn + '.yar')
            path_yara = os.getcwd() + '\\' + year + '\\' + filename_yara
            yara_text = manyquery['rules']['yara']
            with open(path_yara, "w" , encoding='utf-8') as file:
                file.write(yara_text)

            ## suricata
            filename_suricata = formatStr(titleCn + '.rules')
            path_suricata = os.getcwd() + '\\' + year + '\\' + filename_suricata
            suricata_text = manyquery['rules']['suricata']
            with open(path_suricata, "w", encoding='utf-8') as file:
                file.write(suricata_text)


            # 情报csv
            filename_csv = formatStr(titleCn + '.csv')
            path_csv = os.getcwd() + '\\' + year + '\\' + filename_csv
            fo_ti = open(path_csv, 'w+', encoding='utf-8')#, newline='')
            fieldnames_ti = ['titleCn', 'Actor','ip', 'domain', 'ssl', 'email', 'url', 'hash', 'suricata', 'yara', 'Time',
                             'fileUuid']  # 这是标题栏的内容
            writer_ti = csv.DictWriter(fo_ti, fieldnames=fieldnames_ti)  # 把标题栏加入到csv文件中
            writer_ti.writeheader()  # 这一行是写入第一行的标题栏，放在for循环的外面，不然就会出现很多个标题栏
            try:
                writer_ti.writerow(
                    {'titleCn': titleCn, 'Actor': alias ,'ip': "\r\n".join(ip_list), 'domain': "\r\n".join(domain_list),
                     'ssl': "\r\n".join(ssl_list), 'email': "\r\n".join(email_list), \
                     'url': "\r\n".join(url_list), 'hash': "\r\n".join(hash_list), 'suricata': suricata_text, \
                     'yara': yara_text, 'Time': Time, 'fileUuid': index['fileUuid']})
                fo_ti.close()
            except Exception as err_ti:
                print(err_ti)

            # 情报csv
            ioc_csv = formatStr(titleCn + '_ioc.csv')
            path_ioc_csv = os.getcwd() + '\\' + year + '\\' + ioc_csv
            fo_ioc = open(path_ioc_csv, 'w+', encoding='utf-8')  # , newline='')
            fieldnames_ioc = ['IOC', 'Type', 'Actor']  # 这是标题栏的内容
            writer_ioc = csv.DictWriter(fo_ioc, fieldnames=fieldnames_ioc)  # 把标题栏加入到csv文件中
            writer_ioc.writeheader()  # 这一行是写入第一行的标题栏，放在for循环的外面，不然就会出现很多个标题栏
            try:
                for ip1 in ip_list:
                    writer_ioc.writerow({'IOC': ip1,  'Type': 'ip', 'Actor': alias})
                for domain1 in domain_list:
                    writer_ioc.writerow({'IOC': domain1,  'Type': 'domain', 'Actor': alias})
                for hash1 in hash_list:
                    writer_ioc.writerow({'IOC': hash1,  'Type': 'hash', 'Actor': alias})
                for url1 in url_list:
                    writer_ioc.writerow({'IOC': url1,  'Type': 'url', 'Actor': alias})
                for email1 in email_list:
                    writer_ioc.writerow({'IOC': email1,  'Type': 'email', 'Actor': alias})
                fo_ioc.close()
            except Exception as err_ti:
                print(err_ti)

            # pdf下载
            filename_pdf = downlaod_pdf(index, titleCn, year, count)

            time.sleep(random.randint(4, 10))

            zipfiles = [year +'\\' + filename_pdf, year +'\\' + filename_csv,year +'\\' + ioc_csv,  year +'\\' + filename_suricata,year +'\\' + filename_yara]
            zip_file = os.getcwd() + '\\' + year + '\\' + formatStr(titleCn) +'.zip'
            get_zip(zipfiles, zip_file)
            for p in zipfiles:
                os.remove(p)



        except Exception as err:
            print(err)
    print(year+' ok')

if __name__ == '__main__':
    start_year = 2021
    while start_year>=2018:
        downloadEvent(str(start_year))
        start_year-=1
    print('over')




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
