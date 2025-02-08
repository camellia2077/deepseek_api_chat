from openai import OpenAI
from tqdm import tqdm
import time

# deepseek-reasoner
# deepseek-chat
MODEL = "deepseek-reasoner"
API_KEY = "sk-"
BASE_URL = "https://api.deepseek.com"   # 替换为正确的 API 地址
SYSTEM_MESSAGE = "You are a helpful assistant"
FILE_PATH = "D:\\sub\\test\\input.txt"  # 全局文件路径变量

class FileReader:
    """
    用于读取文件内容的类，同时使用 tqdm 显示读取进度。
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_content(self):
        """
        从指定文件路径逐行读取内容，并返回整个文件的字符串。
        使用 tqdm 显示读取每一行的进度条。
        """
        try:
            content = ""
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 使用 tqdm 遍历每一行，显示进度
                for line in tqdm(lines, desc="读取文件进度", unit="行"):
                    # 如果需要模拟处理耗时，可以添加延时，例如：
                    time.sleep(0.01)
                    content += line
            return content
        except Exception as e:
            print(f"读取文件 {self.file_path} 失败: {e}")
            return ""

class DeepSeekChat:
    def __init__(self, model, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def get_response(self, system_message, user_message):
        # 此处假设返回非流式响应，如需流式响应请设置 stream=True 并处理响应迭代
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        return response.choices[0].message.content

def main():
    # 读取文件内容，并通过 tqdm 显示进度
    file_reader = FileReader(FILE_PATH)
    user_message = file_reader.get_file_content()

    print("Chat Started-------------------.\n")
    
    if user_message:
        chat = DeepSeekChat(MODEL, API_KEY, BASE_URL)
        print("正在与 API 通信，请稍候...")
        # 模拟等待 API 响应的进度条（实际调用 API 时可能不需要此进度条）
        for _ in tqdm(range(100), desc="等待 API 响应", unit="%"):
            time.sleep(0.01)
        response = chat.get_response(SYSTEM_MESSAGE, user_message)
        print("API 响应:")
        print(response)
        print("Chat Finished-------------------.")
    else:
        print("没有读取到有效的用户提示词")

if __name__ == "__main__":
    main()
