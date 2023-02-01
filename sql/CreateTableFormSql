import os, sys

if __name__ == '__main__':

    # 打开文件
    COOKED_FOLDER = './sql/'  # 文件夹的地址
    dirs = os.listdir(COOKED_FOLDER)

    # 输出结果
    fout = open('result.txt', 'a+', encoding='utf-8')


    # 输出所有文件和文件夹
    for file in dirs:
        print(file)  # 读出所有文件夹名字

        file_object1 = open('./sql/' + file, 'r', encoding='utf-8')
        try:
            line = file_object1.readline()
            if line:
                print("line=", line)
                str1 = line[line.index('('):]
                list_split = str1.split(' VALUES ')
                key = list_split[0]
                value = list_split[1]

                key = key[1:-1]
                value = value[1:-3]

                list_key = key.split(',')
                list_value = value.split(',')

                name = file.split('.')[0]
                result = 'create table ' + name + '('

                size = len(list_key)
                for index in range(size):
                    _key = list_key[index].replace('`', '')
                    _value = list_value[index]

                    result = result+ _key
                    tem = result[-1]



                    if '\'' in _value:
                        # 字符串
                        result = result + ' '
                        result = result + 'char(255)'
                    else:
                        if '.' in _value:
                            # 浮点型
                            result = result + ' '
                            result = result + 'double'
                        else:
                            # int
                            result = result + ' '
                            result = result + 'int'
                    if result[-1] != ',' and result[-1] != '(':
                        result = result + ','

                result = result[0:-1]
                result = result + ');'

                print(result)


                fout.writelines(result+'\n')



        finally:
            pass

    file_object1.close()
    fout.close()
