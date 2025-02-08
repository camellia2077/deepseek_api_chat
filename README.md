![image](https://github.com/user-attachments/assets/7583aad0-cfe1-48b4-948a-d2ba677bb668)# 程序功能
调用deepseek进行长文本输入

# 环境配置
1创建虚拟库

python -m venv .venv

2激活虚拟库

python3 -m venv .venv

3安装库

pip install openai

pip install tqdm

#api获取
https://platform.deepseek.com/api_keys 在这里获取并且创建你的deepseek api key


# 程序使用说明

全局变量MODEL = "deepseek-reasoner" 设置可选的模型名称，可以选MODEL = "deepseek-chat"

全局变量API_KEY = "sk-9de" ""里的内容替换为你的api_key

全局变量SYSTEM_MESSAGE = "You are a helpful assistant" 在""里面输入你想要的系统提示词

全局变量FILE_PATH = "D:\\sub\\test\\input.txt"  在""里面输入用户提示词的目录，注意是\\而不是\

