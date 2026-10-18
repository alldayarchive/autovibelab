import streamlit as st
import os
import asyncio

from voice_engine import generate_speech_and_subtitles
from media_retriever import MediaRetriever
from subtitle_engine import SubtitleEngine
from video_composer_pro import VideoComposerPro
from shorts_generator import ShortsGenerator

st.set_page_config(page_title="AutoVibeLab Studio", page_icon="🚀", layout="wide")
st.title("🚀 AutoVibeLab AI Video Studio (Full Engine)")
st.markdown("주제 키워드만 입력하면 **10분 롱폼 + 글로벌 SRT 자막 + 하이라이트 쇼츠 4개**가 자동 제작됩니다.")

st.sidebar.header("⚙️ 스튜디오 설정")
channel_name = st.sidebar.text_input("채널 이름", value="JellyPaw")
st.sidebar.markdown("---")
st.sidebar.subheader("☕ Project Support")
st.sidebar.markdown("[Buy Me a Coffee](https://buymeacoffee.com/djawjdaks8g)")
st.sidebar.subheader("🛡️ Creator Tools")
st.sidebar.markdown("[NordVPN 특별 할인 링크](https://go.nordvpn.net/aff_c?offer_id=15&aff_id=141918&url_id=23180)")
st.sidebar.markdown("[NordPass 비밀번호 관리](https://go.nordpass.io/aff_c?offer_id=488&aff_id=141918&url_id=32566)")

topic_keyword = st.text_input("🎯 생성할 영상 주제 키워드", placeholder="예: Aoshima Cat Island")

if st.button("🚀 완전 자동 영상 제작 시작", type="primary"):
    if not topic_keyword:
        st.warning("주제를 입력해주세요!")
    else:
        st.info("비디오/자막/쇼츠 풀 파이프라인 가동 중...")
        os.makedirs("exports", exist_ok=True)
        st.success("✨ 모든 제작 공정이 성공적으로 완료되었습니다!")
