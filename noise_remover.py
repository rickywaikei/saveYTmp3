import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from scipy.signal import butter, sosfilt

def normalize_audio(audio_data, target_db=-1.0):
    """
    將音訊振幅正規化至指定的 dBFS Peak (預設 -1.0 dB，避免數位破音)
    """
    # 計算目前的最高峰值振幅
    max_peak = np.max(np.abs(audio_data))
    
    if max_peak == 0:
        return audio_data  # 靜音檔案直接返回
    
    # 計算目標振幅比例 (target_db -> linear scale)
    target_amplitude = 10 ** (target_db / 20)
    
    # 計算增益倍數並進行拉升
    gain = target_amplitude / max_peak
    return audio_data * gain

def remove_vinyl_noise_and_boost(input_path, output_path):
    print("1. 正在加載音訊檔案...")
    data, sr = librosa.load(input_path, sr=None, mono=False)
    
    is_mono = False
    if data.ndim == 1:
        data = np.expand_dims(data, axis=0)
        is_mono = True

    processed_channels = []

    for channel_idx in range(data.shape[0]):
        channel_data = data[channel_idx]
        
        print(f"2. 正在處理第 {channel_idx + 1} 聲道...")
        
        # --- 步驟 A: 低頻轟鳴濾波 ---
        sos = butter(10, 35, 'hp', fs=sr, output='sos')
        filtered_data = sosfilt(sos, channel_data)

        # --- 步驟 B: 頻譜降噪 ---
        reduced_noise = nr.reduce_noise(
            y=filtered_data, 
            sr=sr, 
            prop_decrease=0.75,
            stationary=True,
            n_fft=2048
        )

        # --- 步驟 C: 爆裂聲修復 ---
        threshold = np.std(reduced_noise) * 5
        peaks = np.abs(reduced_noise) > threshold
        
        cleaned_channel = np.copy(reduced_noise)
        for idx in np.where(peaks)[0]:
            start = max(0, idx - 2)
            end = min(len(cleaned_channel), idx + 3)
            cleaned_channel[idx] = np.median(cleaned_channel[start:end])
            
        processed_channels.append(cleaned_channel)

    # 重組聲道
    final_data = np.array(processed_channels)
    
    # --- 步驟 D: 音量正規化 (Peak Normalization) ---
    print("3. 正在放大音量 (正規化至 -1.0 dB)...")
    final_data = normalize_audio(final_data, target_db=-1.0)

    if is_mono:
        final_data = final_data[0]
    else:
        final_data = final_data.T

    print("4. 正在導出處理後的音訊...")
    sf.write(output_path, final_data, sr)
    print(f"✅ 處理完成！音量已放大並儲存至: {output_path}")

# ================= 執行處理 =================
input_mp3 = "attached_song.mp3"
output_mp3 = "cleaned_boosted_song.mp3"

remove_vinyl_noise_and_boost(input_mp3, output_mp3)