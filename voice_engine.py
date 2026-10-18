import os
import asyncio
import edge_tts

class VoiceEngine:
    def __init__(self, output_dir="temp_downloads"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_voice(self, text: str, voice_name: str = "en-US-AnaNeural", filename: str = "output_voice.mp3"):
        """
        주어진 텍스트를 마이크로소프트 Edge TTS를 이용해 고품질 오디오 파일로 변환합니다.
        """
        output_path = os.path.join(self.output_dir, filename)
        print(f"🎙️ [VoiceEngine] 음성 합성 시작 (Voice: {voice_name})...")
        
        try:
            communicate = edge_tts.Communicate(text, voice_name)
            await communicate.save(output_path)
            print(f"✅ [VoiceEngine] 음성 파일 생성 완료: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ [VoiceEngine] 음성 합성 중 에러 발생: {e}")
            raise e

# 🧪 단독 테스트 실행용 코드 (필요시 터미널에서 python voice_engine.py로 테스트 가능)
if __name__ == "__main__":
    engine = VoiceEngine()
    sample_text = "Welcome to AutoVibeLab. This is a real, functional AI voice generation engine running locally on your computer."
    asyncio.run(engine.generate_voice(sample_text))
