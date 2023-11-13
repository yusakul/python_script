import os

#银狐配置提取

def extract_wide_strings_from_binary_files(folder_path):
    """
    从指定文件夹下的所有二进制文件中提取包含“codemark”之后的宽字节字符串
    """
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                data = f.read()

                # 查找“codemark”字符串的位置
                index = data.find(b"codemark")
                if index < 0:
                    continue

                # 提取“codemark”字符串之后的数据
                data = data[index + len(b"codemark"):]

                # 查找宽字节字符串
                i = 0
                while i < len(data):
                    if data[i] == 0 and i + 1 < len(data) and data[i + 1] != 0:
                        # 找到了宽字节字符串的起始位置
                        j = i + 1
                        while j < len(data) and data[j] != 0:
                            j += 1

                        # 提取宽字节字符串
                        wide_string = data[i:j].decode("utf-16-le","ignore")
                        print(f"File {filename}: {wide_string}")

                        i = j
                    else:
                        i += 1

if __name__ == "__main__":
    folder_path = "./11689491609"
    extract_wide_strings_from_binary_files(folder_path)
