import os

class ShortsGenerator:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_shorts(self, longform_path, highlights, char_info):
        print("📱 [ShortsGenerator] 9:16 하이라이트 쇼츠 4개 세로형 파생 시작...")
        return []
