import os
import yt_dlp

class MediaRetriever:
    def __init__(self, download_dir="temp_downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def search_and_download_youtube(self, keyword: str, output_filename: str = "raw_source.mp4") -> str:
        """
        주어진 키워드로 유튜브 영상을 검색하여 최고 화질(최대 1080p) MP4소스를 다운로드합니다.
        """
        output_path = os.path.join(self.download_dir, output_filename)
        
        # 이미 다운로드된 파일이 있다면 중복 다운로드를 방지합니다.
        if os.path.exists(output_path):
            print(f"🔍 [MediaRetriever] 기존에 수집된 소스 파일 발견: {output_path}")
            return output_path

        print(f"🔍 [MediaRetriever] '{keyword}' 관련 유튜브 4K/1080p 브이로그 소스 탐색 및 다운로드 중...")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_dir, 'source_raw.mp4'),
            'noplaylist': True,
            'quiet': True,
        }

        try:
            # yt-dlp를 이용한 실전 검색 및 다운로드 (유튜브 검색 쿼리 활용)
            search_query = f"ytsearch1:{keyword} travel vlog 4k"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"📡 [MediaRetriever] Query executing: {search_query}")
                ydl.download([search_query])
            
            # 다운로드된 파일명을 지정된 이름으로 정돈
            downloaded_file = os.path.join(self.download_dir, 'source_raw.mp4.mp4')
            if os.path.exists(downloaded_file):
                os.rename(downloaded_file, output_path)
            else:
                # 확장자가 다를 경우를 대비한 유연한 탐색
                for f in os.listdir(self.download_dir):
                    if f.startswith('source_raw'):
                        os.rename(os.path.join(self.download_dir, f), output_path)
                        break

            print(f"✅ [MediaRetriever] 소스 미디어 수집 완료: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ [MediaRetriever] 소스 수집 중 에러 발생: {e}")
            # 에러 발생 시 비상용 더미 경로 반환 (파이프라인 중단 방지)
            return output_path

# 🧪 단독 테스트 실행용 코드
if __name__ == "__main__":
    retriever = MediaRetriever()
    retriever.search_and_download_youtube("Aoshima Cat Island")
