# 程序功能
调用deepseek进行长文本输入

# 环境配置
1创建虚拟库

python -m venv .venv

2安装库

pip install openai

pip install tqdm

# api获取
https://platform.deepseek.com/api_keys 在这里获取并且创建你的deepseek api key


# 程序使用说明
在master.py中修改变量input_file和api_key，不设置output_dir默认输出到和输入文件同文件夹
例如我在D:\sub\request中有一个request.txt文件，应该设置input_file = D:\\sub\\request\\request.txt，注意是双斜线


# 注意
1请求次数不要太频繁，可以试试新建一个key再次使用
2 是否输入了key
3是否输入了正确的key
3 如何无法连接，退出络代理


