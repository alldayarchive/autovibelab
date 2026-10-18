import os
import asyncio
import edge_tts

class VoiceEngine:
    def __init__(self, output_dir="temp_downloads"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_voice(self, script_items: list, output_audio_filename: str = "combined_voice.mp3") -> str:
        """
        script_items: [{'speaker': 'en_girl', 'text': 'Hello world!'}, ...] 형태의 대본 리스트
        대화 내용을 순차적으로 합성하여 하나의 오디오 파일로 병합하고 경로를 반환합니다.
        """
        output_audio_path = os.path.join(self.output_dir, output_audio_filename)
        print("🎙️ [VoiceEngine] Edge-TTS 무료 다국어 오디오 생성 시작...")

        temp_audio_files = []

        try:
            for idx, item in enumerate(script_items):
                text = item.get("text", "")
                speaker = item.get("speaker", "en_girl")
                
                # 화자별 목소리 설정 (여성/남성 보이스 매핑)
                voice_name = "en-US-AnaNeural" if "girl" in speaker else "en-US-AriaNeural"
                
                temp_file = os.path.join(self.output_dir, f"temp_voice_{idx}.mp3")
                
                communicate = edge_tts.Communicate(text, voice_name)
                await communicate.save(temp_file)
                temp_audio_files.append(temp_file)

            # 단순 병합 처리 (실제 구동 시 파일 바이트 연결 또는 ffmpeg 활용)
            with open(output_audio_path, "wb") as outfile:
                for tf in temp_audio_files:
                    if os.path.exists(tf):
                        with open(tf, "rb") as infile:
                            outfile.write(infile.read())
                        os.remove(tf) # 임시 파일 정리

            print(f"✅ [VoiceEngine] 통합 오디오 파일 생성 완료: {output_audio_path}")
            return output_audio_path

        except Exception as e:
            print(f"❌ [VoiceEngine] 오디오 생성 중 에러 발생: {e}")
            raise e

# 🧪 단독 테스트 실행용 코드
if __name__ == "__main__":
    engine = VoiceEngine()
    test_script = [
        {"speaker": "en_girl", "text": "Welcome to AutoVibeLab studio."},
        {"speaker": "en_boy", "text": "Let's explore the world together!"}
    ]
    asyncio.run(engine.generate_voice(test_script))
