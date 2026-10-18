import os

class SubtitleEngine:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _format_time(self, seconds: float) -> str:
        """초(Second) 단위를 SRT 자막 표준 타임코드 형식 (00:00:00,000)으로 변환합니다."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def generate_global_srt(self, script_items: list, output_filename: str = "global_subtitles.srt") -> str:
        """
        script_items: [{'text': 'Hello world!'}, {'text': 'Welcome to AutoVibeLab.'}] 형태의 대본 리스트
        정밀한 타이밍을 계산하여 표준 .srt 파일을 생성하고 경로를 반환합니다.
        """
        srt_path = os.path.join(self.output_dir, output_filename)
        print("🌐 [SubtitleEngine] 글로벌 표준 SRT 자막 파일 생성 중...")

        srt_content = []
        current_time = 0.0

        for idx, item in enumerate(script_items, start=1):
            text = item.get("text", "")
            
            # 문장 글자 수에 따른 대략적인 노출 시간 계산 (글자당 약 0.07초, 최소 2.5초 보장)
            duration = max(2.5, len(text) * 0.07)
            start_time = current_time
            end_time = current_time + duration

            start_str = self._format_time(start_time)
            end_str = self._format_time(end_time)

            # SRT 포맷 표준 구조 작성
            srt_content.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")
            
            # 문장 간 미세한 여유 공백(0.3초) 추가
            current_time = end_time + 0.3

        # 파일 저장
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_content))

        print(f"✅ [SubtitleEngine] SRT 자막 생성 완료: {srt_path}")
        return srt_path

# 🧪 단독 테스트 실행용 코드
if __name__ == "__main__":
    engine = SubtitleEngine()
    test_script = [
        {"text": "Welcome to paradise. Today we explore Aoshima Cat Island."},
        {"text": "Look at all these adorable cats roaming around freely!"}
    ]
    engine.generate_global_srt(test_script, "test_global.srt")
