import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

class ShortsGenerator:
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_shorts(self, longform_path: str, highlights_intervals: list, characters_info: dict) -> list:
        """
        완성된 롱폼 영상(longform_path)과 하이라이트 구간 리스트([(시작초, 종료초), ...])를 받아
        9:16 세로형 쇼츠 영상 4개를 자동으로 잘라내고 렌더링합니다.
        """
        print("📱 [ShortsGenerator] 9:16 하이라이트 쇼츠 파생 및 렌더링 시작...")
        shorts_paths = []

        if not os.path.exists(longform_path):
            print(f"❌ [ShortsGenerator] 원본 롱폼 영상을 찾을 수 없습니다: {longform_path}")
            return shorts_paths

        try:
            video = VideoFileClip(longform_path)
            
            # 1080x1920 세로형 규격에 맞게 중앙 자르기(Crop) 또는 리사이즈 준비
            orig_w, orig_h = video.size

            for idx, (start_t, end_t)Popen in enumerate(highlights_intervals, start=1):
                short_filename = f"Highlight_Short_{idx:02d}.mp4"
                short_output_path = os.path.join(self.output_dir, short_filename)
                
                print(f"⏳ [ShortsGenerator] 쇼츠 {idx}번 렌더링 중 ({start_t}초 ~ {end_t}초)...")

                # 구간 자르기 (최대 59초 제한 방어)
                duration = min(end_t - start_t, 59.0)
                clip_segment = video.subclip(start_t, start_t + duration)

                # 9:16 비율 크롭 (가로 중앙 기준 세로형 맞춤)
                target_w = int(orig_h * (9 / 16))
                if target_w > orig_w:
                    target_w = orig_w
                x_center = orig_w / 2
                x1 = x_center - (target_w / 2)
                x2 = x_center + (target_w / 2)

                cropped_clip = clip_segment.crop(x1=x1, y1=0, x2=x2, y2=orig_h).resize(newsize=(1080, 1920))

                # 캐릭터 오버레이 추가 (쇼츠 하단 고정)
                layers = [cropped_clip]
                luna_path = characters_info.get("luna", "")
                if luna_path and os.path.exists(luna_path):
                    luna_img = ImageClip(luna_path).set_duration(duration).resize(height=250).set_position(("center", 1550))
                    layers.append(luna_img)

                final_short = CompositeVideoClip(layers)

                # 쇼츠 MP4 렌더링
                final_short.write_videofile(
                    short_output_path,
                    fps=30,
                    codec="libx264",
                    audio_codec="aac",
                    preset="ultrafast",
                    threads=4
                )

                shorts_paths.append(short_output_path)
                print(f"✅ [ShortsGenerator] 쇼츠 {idx}번 완성: {short_output_path}")

            video.close()
            print(f"🎉 [ShortsGenerator] 모든 하이라이트 쇼츠({len(shorts_paths)}개) 파생 완료!")
            return shorts_paths

        except Exception as e:
            print(f"❌ [ShortsGenerator] 쇼츠 생성 중 에러 발생: {e}")
            return shorts_paths
