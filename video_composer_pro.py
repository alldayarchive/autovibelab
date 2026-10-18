import os
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, 
    CompositeVideoClip, concatenate_videoclips
)
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip

class VideoComposerPro:
    def __init__(self, output_resolution=(1920, 1080)):
        self.width, self.height = output_resolution

    def create_video_with_subtitles(self, bg_clips_paths: list, audio_path: str, characters_info: dict, srt_path: str, output_filename: str = "longform_final.mp4") -> str:
        """
        배경 비디오 클립들, 음성 파일, 캐릭터 에셋 경로, SRT 자막 파일을 받아
        1080p 고화질 롱폼 완성본 비디오를 렌더링합니다.
        """
        output_path = os.path.join("exports", output_filename)
        os.makedirs("exports", exist_ok=True)
        print(f"🎬 [VideoComposerPro] 최종 롱폼 영상 합성 시작: {output_path}")

        try:
            # 1. 오디오 트랙 로드
            audio_track = AudioFileClip(audio_path)
            total_duration = audio_track.duration

            # 2. 배경 비디오 클립 연결 및 오디오 길이에 맞추기
            loaded_bg_clips = []
            current_dur = 0
            
            for path in bg_clips_paths:
                if current_dur >= total_duration:
                    break
                if os.path.exists(path):
                    clip = VideoFileClip(path).without_audio().resize(newsize=(self.width, self.height))
                    loaded_bg_clips.append(clip)
                    current_dur += clip.duration

            if not loaded_bg_clips:
                raise ValueError("⚠️ 유효한 배경 비디오 클립이 없습니다. MediaRetriever를 먼저 실행하세요!")

            final_bg = concatenate_videoclips(loaded_bg_clips).subclip(0, total_duration)

            # 3. 레이어 구성 (배경부터 시작)
            layers = [final_bg]

            # 캐릭터 A (왼쪽 아래 배치)
            luna_path = characters_info.get("luna", "")
            if luna_path and os.path.exists(luna_path):
                luna_img = ImageClip(luna_path).set_duration(total_duration).resize(height=300).set_position(("left", "bottom"))
                layers.append(luna_img)

            # 캐릭터 B (오른쪽 아래 배치)
            sunny_path = characters_info.get("sunny", "")
            if sunny_path and os.path.exists(sunny_path):
                sunny_img = ImageClip(sunny_path).set_duration(total_duration).resize(height=300).set_position(("right", "bottom"))
                layers.append(sunny_img)

            # 4. SRT 자막 렌더링 설정
            def generator(txt):
                return TextClip(
                    txt, 
                    font='Arial', 
                    fontsize=40, 
                    color='white', 
                    stroke_color='black', 
                    stroke_width=2,
                    method='caption',
                    size=(self.width * 0.8, None)
                )

            if os.path.exists(srt_path):
                subtitles = SubtitlesClip(srt_path, generator)
                subtitles_set = subtitles.set_position(('center', self.height - 220))
                layers.append(subtitles_set)

            # 5. 최종 합성 및 오디오 주입
            composite_video = CompositeVideoClip(layers).set_audio(audio_track)

            # 6. MP4 파일로 최종 렌더링
            print(f"⏳ [VideoComposerPro] MP4 파일 렌더링 중 (시간이 다소 소요될 수 있습니다)...")
            composite_video.write_videofile(
                output_path,
                fps=30,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=4
            )

            print(f"🎉 [VideoComposerPro] 롱폼 영상 완성 완료: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ [VideoComposerPro] 영상 합성 중 에러 발생: {e}")
            raise e
