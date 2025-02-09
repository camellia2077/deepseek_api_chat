from ds_chat_2 import TextAnalyzer
import time

def main():
    print(f"Chat started---------------------\n")
    start = time.time()
    analyzer = TextAnalyzer(
        # 必填参数
        input_file="D:\\sub\\request\\request.txt", #输入txt文件目录
        api_key="",#输入你的key

        # 可选
        model_type="deepseek-chat",#可选deepseek-reasoner
        output_dir= None,
        )
    analyzer.run()
    end = time.time() 
    print(f"Time: {end - start} 秒\n")
    print(f"Chat finished---------------------")

if __name__ == "__main__":
    main()