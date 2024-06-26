import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
df = pd.read_excel(r'xyz.xlsx')

# 将时间字符串转换为 datetime 类型
df['会话开始时间'] = pd.to_datetime(df['会话开始时间'], format='%Y/%m/%d %H:%M:%S')

# 添加条件，只绘制表格列"总负载"值大于1000的有效数据
df_valid = df[df['总负载'] > 10]

# 提取小时信息
df_valid['会话开始时间'] = df_valid['会话开始时间'].dt.hour

# 绘制时间段分布图
plt.figure(figsize=(10, 6))
plt.hist(df_valid['会话开始时间'], bins=24, color='skyblue', edgecolor='black')
plt.xlabel('Hour of Day')
plt.ylabel('Frequency')
plt.title('Distribution of Time Periods')
plt.xticks(range(0, 24))
plt.grid(axis='y', alpha=0.75)
plt.show()
