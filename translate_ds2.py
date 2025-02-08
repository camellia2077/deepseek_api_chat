from openai import OpenAI
from tqdm import tqdm
import time
import re

class Config:
    """配置管理类"""
    MODEL_TYPE = "deepseek-chat"
    API_KEY = "sk-"
    BASE_URL = "https://api.deepseek.com"
    SYSTEM_PROMPT = """请严格遵循以下翻译规则：
    1. 只翻译日语文本部分
    2. 保持序号不变
    3. 保留所有特殊符号和格式
    4. 输出格式：[序号]\n[翻译结果]\n\n"""
    INPUT_PATH = "D:\sub\mvsd\\MVMD-041.HD_01.srt"
    OUTPUT_PATH = "D:\sub\mvsd\\MVMD-041.HD_01_output.srt"
    MAX_BLOCKS = 5

class SRTFileParser:
    """SRT文件解析处理器"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.blocks = []
    
    def parse(self):
        """执行解析操作"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return self._process_content(f.read())
        except Exception as e:
            print(f"文件解析失败: {e}")
            return False
    
    def _process_content(self, content):
        """处理文件内容"""
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n\n'
        matches = re.findall(pattern, content, re.DOTALL)
        
        self.blocks = [self._create_block(match) for match in tqdm(matches, desc="解析字幕块")]
        return True
    
    def _create_block(self, match):
        """创建字幕块结构"""
        return {
            'index': int(match[0]),
            'timestamp': match[1],
            'original': match[2].strip(),
            'translated': None
        }

class TranslationEngine:
    """翻译引擎核心类"""
    def __init__(self, Config):
        self.client = OpenAI(api_key=Config.API_KEY, base_url=Config.BASE_URL)
        self.model = Config.MODEL_TYPE
        self.prompt = Config.SYSTEM_PROMPT
    
    def process_batch(self, blocks):
        """处理批量翻译"""
        input_text = self._build_input(blocks)
        response = self._get_api_response(input_text)
        return self._parse_response(response)
    
    def _build_input(self, blocks):
        """构建API输入内容"""
        return "\n\n".join(f"[{b['index']}]\n{b['original']}" for b in blocks)
    
    def _get_api_response(self, input_text):
        """获取API响应"""
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": input_text},
                ],
                temperature=0.3,
                stream=False
            ).choices[0].message.content
        except Exception as e:
            print(f"API请求异常: {e}")
            return ""
    
    @staticmethod
    def _parse_response(response_text):
        """解析翻译结果"""
        translations = {}
        pattern = r'\[(\d+)\]\n(.+?)(?=\n\[\d+\]|$)'
        for index, text in re.findall(pattern, response_text, re.DOTALL):
            translations[int(index)] = text.strip()
        return translations

class OutputManager:
    """输出结果管理器"""
    def __init__(self, output_path):
        self.output_path = output_path
    
    def save_progress(self, blocks):
        """保存处理进度"""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                for block in blocks:
                    if block['translated']:
                        f.write(self._format_block(block))
        except Exception as e:
            print(f"保存失败: {e}")
    
    def finalize(self):
        """完成处理"""
        print(f"\n处理完成！结果已保存至：{self.output_path}")
    
    @staticmethod
    def _format_block(block):
        """格式化字幕块"""
        return f"{block['index']}\n{block['timestamp']}\n{block['translated']}\n\n"

class SRTProcessor:
    """主处理控制器"""
    def __init__(self, config):
        self.config = config
        self.parser = SRTFileParser(config.INPUT_PATH)
        self.translator = TranslationEngine(config)
        self.output = OutputManager(config.OUTPUT_PATH)
    
    def execute(self):
        """执行完整处理流程"""
        if not self.parser.parse():
            return
        
        groups = self._chunk_blocks(self.parser.blocks)
        progress = tqdm(total=len(groups), desc="翻译进度", unit="组")
        
        translated_blocks = []
        for group in groups:
            translations = self.translator.process_batch(group)
            translated_blocks.extend(self._merge_results(group, translations))
            self.output.save_progress(translated_blocks)
            progress.update(1)
            time.sleep(1)  # API限速保护
        
        progress.close()
        self.output.finalize()
    
    @staticmethod
    def _chunk_blocks(blocks):
        """分块处理"""
        return [blocks[i:i+Config.MAX_BLOCKS] for i in range(0, len(blocks), Config.MAX_BLOCKS)]
    
    @staticmethod
    def _merge_results(blocks, translations):
        """合并翻译结果"""
        return [
            {**b, 'translated': translations.get(b['index'], "")}
            for b in blocks
        ]

if __name__ == "__main__":
    processor = SRTProcessor(Config)
    processor.execute()