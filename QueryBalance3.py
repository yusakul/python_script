import csv
import requests
import json
import argparse
from tqdm import tqdm

def query_usdt_balance(address, token_symbol, debug):
    api_url = "https://apilist.tronscan.org/api/account"
    
    dict_info = {'address':address, "token_symbol":token_symbol, "balance":0, "addressTag":0, "accountType":0, "name": ""}
    
    try:
        response = requests.get(api_url, headers={"TRON-FREE-API-KEY":"a897c5ea-b033-4586-b81f-e4ac147bbfec"}, params={"address": address} , proxies={"http":"http://127.0.0.1:7890", "https":"http://127.0.0.1:7890"})
        
        if debug:
            print(json.loads(response.text))
        data = json.loads(response.text)
        trc20token_balances = data["trc20token_balances"]

        if "addressTag" in data:
            dict_info["addressTag"] = data["addressTag"]
            print(dict_info["addressTag"])
            
        if "accountType" in data:
            dict_info["accountType"] = data["accountType"]
            print(dict_info["accountType"])

        if "name" in data:
            dict_info["name"] = data["name"]
            print(dict_info["name"])
        
        token_balance = next((item for item in trc20token_balances if item["tokenAbbr"] == token_symbol), None)
        if token_balance == None:
            #print("Address:", address)
            #print(token_symbol,":", "None")
            
            dict_info["balance"] = 0
            return dict_info
        else:
            balance = int(token_balance["balance"]) / 1000000
            print("Address:", address)
            print(token_symbol,":", balance)
            
            dict_info["balance"] = balance
            return dict_info
        
        
        
    except Exception as e:
        print("Error occurred with ", address, " : ", e)
        dict_info["balance"] = "None"
        return dict_info
        
        



def main():

    # 创建参数解析器
    parser = argparse.ArgumentParser()

    # 添加参数选项
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-file", help="查询地址列表")
    group.add_argument("-addr", help="查询单一地址")
    parser.add_argument("-symbol", required=True, help="查询目标代币")

    # 解析命令行参数
    args = parser.parse_args()
    symbol = args.symbol
    #print("symbol：", symbol)
    
    
    # 根据参数执行相应的功能
    if args.file:
        filename = args.file
        print("地址列表：", filename)
        
        # 从文件中读取地址列表
        with open(filename, "r") as file:
            addresses = file.read().splitlines()

        # 创建CSV文件并写入表头
        with open("usdt_balances.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Address", symbol + " Balance", "addressTag"， "accountType", "name"])

            # 查询并写入地址和余额
            for i, address in tqdm(enumerate(addresses), total=len(addresses), desc="Processing", leave=True):
            #for address in addresses:
                #dict_info = {'address':address, "token_symbol":token_symbol, "balance":0, "addressTag":0, "accountType":0, "name": ""}
                dict_info = query_usdt_balance(address, symbol, False)
                #print(dict_info)
                balance = str(dict_info["balance"])
                addressTag = str(dict_info["addressTag"])   #交易所等tag
                accountType = str(dict_info["accountType"])  #判断是否合约地址或者钱包地址
                name = str(dict_info["name"])  #合约名称
                writer.writerow([address, balance,addressTag, accountType, name])
        
        print("查询完成，结果已保存到usdt_balances.csv文件中")

    if args.addr:
        # 执行地址相关的功能
        address = args.addr
        # 在这里编写处理地址的代码
        #print("查询地址：", address)
        balance = query_usdt_balance(address, symbol, True)
    

if __name__ == '__main__':
    main()