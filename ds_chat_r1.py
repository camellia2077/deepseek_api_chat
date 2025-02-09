import os
import time
from openai import OpenAI

class TextAnalyzer:
    """
    文本分析器类，用于处理文本文件并通过API获取分析结果。
    """
    
    def __init__(self, input_file, output_dir=None, system_prompt="You are a helpful assistant", 
                 user_prompt="{user_input}", model_type="deepseek-chat", 
                 api_key="", base_url="https://api.deepseek.com"):
        """
        初始化TextAnalyzer类。

        :param input_file: 输入文件路径
        :param output_dir: 输出目录路径，默认为None，表示与输入文件同一目录
        :param system_prompt: 系统提示语，默认为"You are a helpful assistant"
        :param user_prompt: 用户提示语，默认为"请分析以下文本内容：\n{user_input}"
        :param model_type: 使用的模型类型，默认为"deepseek-chat"
        :param api_key: API密钥，默认为"sk-f6993dab2faf4348ab9be61d53eff2d4"
        :param base_url: API基础URL，默认为"https://api.deepseek.com"
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.model_type = model_type
        self.api_key = api_key
        self.base_url = base_url

    def validate_input_file(self):
        """
        验证输入文件是否符合要求。

        :raises FileNotFoundError: 如果输入文件不存在
        :raises ValueError: 如果输入文件不是有效的文件或不是.txt文件
        """
        #检测文件是否为空
        if os.path.getsize(self.input_file) == 0:
            print(f"输入文件 {self.input_file} 为空，请检查文件内容。")
            exit()  # 结束程序
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"输入文件 {self.input_file} 不存在")
        if not os.path.isfile(self.input_file):
            raise ValueError(f"{self.input_file} 不是有效的文件")
        if not self.input_file.lower().endswith('.txt'):
            raise ValueError("只支持.txt文件,请输入txt文件")

    def get_api_response(self, user_input):
        """
        获取API响应。

        :param user_input: 用户输入的文本内容
        :return: API返回的响应内容或错误码
        """
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt.format(user_input=user_input)},
        ]
        
        time.sleep(5)  # 每次调用前等待5秒
        
        # 记录API调用的开始时间
        start_time = time.time()
        
        try:
            response = client.chat.completions.create(
                model=self.model_type,
                messages=messages,
                stream=False
            )
            
            # 记录API调用的结束时间
            end_time = time.time()
            
            # 计算并输出API响应时间
            api_response_time = end_time - start_time
            print(f"API响应时间: {api_response_time:.2f}秒")
            
            return response.choices[0].message.content
        
        except Exception as e:
            # 记录API调用的结束时间
            end_time = time.time()
            
            # 计算并输出API响应时间
            api_response_time = end_time - start_time
            print(f"API调用失败，响应时间: {api_response_time:.2f}秒")
            
            # 返回错误码
            return f"API调用失败，错误码: {str(e)}"

    def save_result(self, content):
        """
        保存结果到输出目录。
        :param content: 要保存的内容
        :return: 保存结果的文件路径
        """
        # 如果 OUTPUT_DIR 为 None，则使用输入文件所在的目录
        output_dir = self.output_dir if self.output_dir is not None else os.path.dirname(self.input_file)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成输出文件名
        input_filename = os.path.basename(self.input_file)
        output_filename = f"{os.path.splitext(input_filename)[0]}_response.txt"
        output_path = os.path.join(output_dir, output_filename)
        # 检测是否存在同名文件
        if os.path.exists(output_path):
            print(f"检测到同名文件 {output_filename}，将覆盖该文件。")
        else:
            print(f"未检测到同名文件，将新建文件 {output_filename}。")
        
        # 保存结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path

    def run(self):
        """
        运行文本分析器，处理输入文件并保存结果。
        """
        try:
            # 验证输入文件
            self.validate_input_file()
            
            # 读取输入文件内容
            with open(self.input_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # 获取API响应
            api_response = self.get_api_response(file_content)
            
            # 保存结果
            output_path = self.save_result(api_response)
            print(f"处理完成，结果已保存至：{output_path}")
            
        except Exception as e:
            print(f"程序运行出错：{str(e)}")

if __name__ == "__main__":
    # 实例化TextAnalyzer类并运行
    print("Program has started--------------------------------")
    analyzer = TextAnalyzer(input_file="D:\\sub\\request\\request.txt")
    analyzer.run()
    print("Program has Finished--------------------------------")
