import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# MP3 파일 경로 설정
mp3_file_path = "/Users/dryoon04/Documents/GitHub/schoolproject/Exercise audio image/ISEGYE IDOL-SuperHero.mp3"

# MP3 파일을 WAV 파일로 변환 (MP3 파일을 직접 처리하기 위해 pydub 라이브러리 사용 가능)
from pydub import AudioSegment
audio = AudioSegment.from_mp3(mp3_file_path)
audio.export("output.wav", format="wav")

# WAV 파일 읽기
sample_rate, audio_data = wavfile.read("output.wav")

# 스테레오 오디오의 경우 왼쪽 채널만 선택
if len(audio_data.shape) > 1:
    audio_data = audio_data[:, 0]

# 푸리에 변환
n = len(audio_data)  # 신호의 길이
k = np.arange(n)
T = n / sample_rate  # 주파수 샘플링 간격
frq = k / T  # 주파수 범위 (0부터 sample_rate까지)

Y = np.fft.fft(audio_data) / n  # 푸리에 변환 및 정규화
Y = Y[:n // 2]  # 절반까지만 선택 (대칭성 때문)

# 결과를 시각화
plt.figure(figsize=(10, 4))
plt.plot(frq[:4000], np.abs(Y[:4000]))  # 주파수 범위를 제한하여 플롯
plt.xlabel('(Hz)')
plt.ylabel('wave size')
plt.title('result')
plt.show()
