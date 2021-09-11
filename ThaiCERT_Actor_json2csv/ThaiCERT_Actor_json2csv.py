# coding: utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import json
import sys
import io

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    files_in = "ThreatGroupCard-Allgroups.json"

    files_out = "out.csv"
    fo = open(files_out,'w+',newline='')
    fieldnames = ['名称', '别名', '关键字','国家','资助背景','动机','行业目标','国家目标','第一次活跃时间','描述','TTPs','参考链接','工具名称','是否apt','是否apt的描述','来源','历史活动','反制行动']  # 这是标题栏的内容
    writer = csv.DictWriter(fo, fieldnames=fieldnames)  # 把标题栏加入到csv文件中
    writer.writeheader()  # 这一行是写入第一行的标题栏，放在for循环的外面，不然就会出现很多个标题栏

    try:
        with open(files_in, mode="r", encoding="utf-8") as fe:
            data = json.load(fe)
            # writer.writerow({'title': data['attributes']['title'], 'content': line, 'data': json.dumps(line)})
            for value in data['values']: # 遍历actor
                actor = value['actor']
                actor = actor.encode('utf-8').decode('GB2312')

                # name
                names = value['names']
                names_total = ''
                for name_meta in names:
                    names_total += name_meta['name'] + ' (' + name_meta['name-giver'] + ')'
                    names_total += '\r\n'
                names_total = names_total.encode('utf-8').decode('GB2312')

                country = value['country'][0]
                country = country.encode('utf-8').decode('GB2312')

                try:
                    sponsor_total = value['sponsor']
                    sponsor_total = sponsor_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    sponsor_total = ''

                try:
                    motivation = value['motivation']
                    motivation_total = ''
                    for motivation_meta in motivation:
                        motivation_total += motivation_meta
                        motivation_total += '\r\n'
                    motivation_total = motivation_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    motivation_total = ''

                try:
                    observed_sectors = value['observed-sectors']
                    observed_sectors_total = ''
                    for observed_sectors_meta in observed_sectors:
                        observed_sectors_total += observed_sectors_meta
                        observed_sectors_total += '\r\n'
                    observed_sectors_total = observed_sectors_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    observed_sectors_total = ''

                try:
                    observed_countries = value['observed-countries']
                    observed_countries_total = ''
                    for observed_countries_meta in observed_countries:
                        observed_countries_total += observed_countries_meta
                        observed_countries_total += '\r\n'
                    observed_countries_total = observed_countries_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    observed_countries_total = ''

                try:
                    first_seen = value['first-seen']
                except Exception as err:
                    first_seen = ''

                try:
                    description = value['description']
                    description = description.encode('utf-8').decode('GB2312')
                except Exception as err:
                    description = ''

                try:
                    tools = value['tools']
                    tools_total = ''
                    for tools_meta in tools:
                        tools_total += tools_meta
                        tools_total += '\r\n'
                    tools_total = tools_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    tools_total = ''

                try:
                    operations = value['operations']
                    operations_total = ''
                    for operations_meta in operations:
                        operations_total += operations_meta['date'] + ' : ' + operations_meta['activity']
                        operations_total += '\r\n'
                        operations_total += '\r\n'
                    operations_total = operations_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    operations_total = ''

                try:
                    counter_operations = value['counter_operations']
                    counter_operations_total = ''
                    for counter_operations_meta in counter_operations:
                        counter_operations_total += counter_operations_meta['date'] + ' : ' + counter_operations_meta['activity']
                        counter_operations_total += '\r\n'
                    counter_operations_total = counter_operations_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    counter_operations_total = ''

                try:
                    information = value['information']
                    information_total = ''
                    for information_meta in information:
                        information_total += information_meta
                        information_total += '\r\n'
                    information_total = information_total.encode('utf-8').decode('GB2312')
                except Exception as err:
                    information_total = ''

                try:
                    mitre_attack = value['mitre-attack']
                    mitre_attack = mitre_attack.encode('utf-8').decode('GB2312')
                except Exception as err:
                    mitre_attack = ''

                writer.writerow({'名称': actor, '别名':names_total, '关键字':'','国家':country,'资助背景':sponsor_total,'动机':motivation_total,'行业目标':observed_sectors_total, '国家目标':observed_countries_total,'第一次活跃时间':first_seen,'描述':description,'TTPs':mitre_attack,'参考链接':information_total,'工具名称':tools_total,'是否apt':'是','是否apt的描述':'','来源':'','历史活动':operations_total,'反制行动':counter_operations_total})

    except Exception as err:
        print(err)

    fo.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
