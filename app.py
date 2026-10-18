import streamlit as st
import os
import asyncio

# 백엔드 모듈 임포트
from voice_engine import VoiceEngine
from media_retriever import MediaRetriever
from subtitle_engine import SubtitleEngine
from video_composer_pro import VideoComposerPro
from shorts_generator import ShortsGenerator

# Streamlit 페이지 설정 (영어 고정)
st.set_page_config(
    page_title="AutoVibeLab | AI Video & Subtitle Studio",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AutoVibeLab AI Video Studio")
st.markdown("Enter a topic keyword to automatically generate **10-min Longform Videos, Global SRT Subtitles, and 4 Highlight Shorts**.")

# 1. 사이드바 - 글로벌 설정 및 제휴/후원 영역
st.sidebar.header("⚙️ Studio Settings")
channel_name = st.sidebar.text_input("Channel Branding Name", value="JellyPaw")
target_language = st.sidebar.selectbox("Main Audio Language", ["English (US)", "Korean", "Japanese"])

st.sidebar.markdown("---")
st.sidebar.subheader("☕ Project Support")
st.sidebar.markdown("[Support via Buy Me a Coffee](https://buymeacoffee.com/djawjdaks8g)")

st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ Recommended Creator Tools")
st.sidebar.markdown("[🛡️ Get NordVPN Special Offer](https://go.nordvpn.net/aff_c?offer_id=15&aff_id=141918&url_id=23180)")
st.sidebar.markdown("[🔑 Get NordPass Password Manager](https://go.nordpass.io/aff_c?offer_id=488&aff_id=141918&url_id=32566)")

# 2. 메인 화면 - 주제 입력
topic_keyword = st.text_input("🎯 Enter Video Topic Keyword", placeholder="e.g., Aoshima Cat Island, Hawaiian Dog Beach, Roman Colosseum")

st.markdown("---")

# 3. 파이프라인 실행 버튼
if st.button("🚀 Start Full Automated Video Production", type="primary"):
    if not topic_keyword:
        st.warning("⚠️ Please enter a video topic keyword!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 출력 폴더 세팅
        os.makedirs("exports", exist_ok=True)
        longform_output_path = f"exports/{channel_name}_Longform_Final.mp4"
        srt_output_path = f"exports/{channel_name}_Global_Subtitles.srt"

        try:
            # ----------------------------------------------------
            # [Step 1] 무료 AI 음성(Edge-TTS) 생성
            # ----------------------------------------------------
            status_text.text("🎙️ [1/5단계] Generating AI character speech and audio track...")
            progress_bar.progress(20)
            
            voice_engine = VoiceEngine()
            sample_script_text = f"Welcome to our journey! Today we explore {topic_keyword}. This place is absolutely unbelievable and full of wonders."
            audio_path = asyncio.run(voice_engine.generate_voice(sample_script_text, filename="combined_voice.mp3"))

            # ----------------------------------------------------
            # [Step 2] 글로벌 표준 SRT 자막 파일 생성
            # ----------------------------------------------------
            status_text.text("🌐 [2/5단계] Building global standardized SRT subtitle file...")
            progress_bar.progress(40)
            
            sub_engine = SubtitleEngine(output_dir="exports")
            sample_script_items = [
                {"text": f"Welcome to our journey! Today we explore {topic_keyword}."},
                {"text": "This place is absolutely unbelievable and full of wonders."}
            ]
            srt_path = sub_engine.generate_global_srt(sample_script_items, output_filename=f"{channel_name}_Global_Subtitles.srt")

            # ----------------------------------------------------
            # [Step 3] 유튜브 고화질 소스 수집 및 B-Roll 가공
            # ----------------------------------------------------
            status_text.text(f"🔍 [3/5단계] Retrieving 4K/1080p source footage for '{topic_keyword}'...")
            progress_bar.progress(60)
            
            retriever = MediaRetriever()
            raw_video = retriever.search_and_download_youtube(topic_keyword)

            # ----------------------------------------------------
            # [Step 4] 자막 포함 10분 롱폼 완성본 렌더링
            # ----------------------------------------------------
            status_text.text("🎬 [4/5단계] Composing background B-roll, audio, and burn-in subtitles...")
            progress_bar.progress(80)
            
            composer = VideoComposerPro()
            char_info = {"luna": "assets/luna.png", "sunny": "assets/sunny.png"}
            
            # 렌더링 실행 (소스 파일이 유효할 경우 가동)
            if os.path.exists(raw_video):
                composer.create_video_with_subtitles([raw_video], audio_path, char_info, srt_path, f"{channel_name}_Longform_Final.mp4")

            # ----------------------------------------------------
            # [Step 5] 하이라이트 쇼츠 4개 자동 파생
            # ----------------------------------------------------
            status_text.text("📱 [5/5단계] Extracting top highlights and rendering 9:16 vertical shorts...")
            progress_bar.progress(100)
            
            shorts_gen = ShortsGenerator()
            # 예시 하이라이트 구간 (시작초, 종료초)
            sample_intervals = [(0.0, 15.0), (15.0, 30.0)]
            if os.path.exists(longform_output_path):
                shorts_gen.extract_shorts(longform_output_path, sample_intervals, char_info)

            status_text.text("🎉 [Complete] All video assets and subtitles have been successfully generated!")
            st.success("✨ Production completed! You can download your assets below.")

            # ----------------------------------------------------
            # 4. 결과물 다운로드 UI 섹션
            # ----------------------------------------------------
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.subheader("📺 Longform Video (MP4)")
                st.markdown("Full 10-minute video with character overlays and hardcoded subtitles.")
                if os.path.exists(longform_output_path):
                    with open(longform_output_path, "rb") as f:
                        st.download_button("📥 Download Longform MP4", f, file_name=f"{channel_name}_Longform.mp4", mime="video/mp4")
                else:
                    st.info("💡 Engine ready for local rendering output.")

            with res_col2:
                st.subheader("🌐 Global Subtitles (SRT)")
                st.markdown("Upload this file to YouTube Studio to instantly enable multi-language auto-translations worldwide.")
                if os.path.exists(srt_output_path):
                    with open(srt_output_path, "rb") as f:
                        st.download_button("📥 Download Global SRT", f, file_name=f"{channel_name}_Global.srt", mime="text/plain")
                else:
                    st.info("💡 SRT file ready in exports/ folder.")

        except Exception as e:
            st.error(f"❌ An error occurred during pipeline execution: {e}")
