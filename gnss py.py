import numpy as np
import matplotlib.pyplot as plt
import re

# 設定篩選條件
AZIMUTH_RANGE = (90, 180)  # 方位角範圍 (degrees)
ELEVATION_MIN = 15  # 最小仰角 (degrees)

def parse_obs_file(input_file):
    """
    解析 RINEX .obs 檔案，讀取衛星數據
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_end_idx = 0
    for i, line in enumerate(lines):
        if "END OF HEADER" in line:
            header_end_idx = i
            break

    header = lines[:header_end_idx + 1]  # 保留標頭
    data_lines = lines[header_end_idx + 1:]  # 觀測數據

    # 解析數據
    satellites = []
    for line in data_lines:
        if line.startswith(">"):  # 時間戳記行
            current_epoch = line.strip()
        else:
            match = re.match(r"([GREC]\d+)\s+([\d.]+)\s+([\d.]+)", line)
            if match:
                sat_id = match.group(1)  # 衛星 ID
                azimuth = float(match.group(2))  # 方位角
                elevation = float(match.group(3))  # 仰角
                
                satellites.append((current_epoch, sat_id, azimuth, elevation, line))

    return header, satellites

def filter_satellites(satellites, az_range, elev_min):
    """
    根據方位角與仰角篩選衛星數據
    """
    filtered_satellites = [
        sat for sat in satellites if not (az_range[0] <= sat[2] <= az_range[1] or sat[3] < elev_min)
    ]
    return filtered_satellites

def save_new_obs_file(output_file, header, satellites):
    """
    輸出新的 RINEX .obs 檔案
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(header)
        for sat in satellites:
            f.write(f"{sat[4]}")  # 原始數據行

def plot_skyplot(satellites, title="Skyplot"):
    """
    繪製 skyplot，檢查衛星分佈
    """
    az = [sat[2] for sat in satellites]
    el = [sat[3] for sat in satellites]

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    azimuth_rad = np.radians(az)
    elevation = 90 - np.array(el)  # 轉換仰角為極座標

    ax.scatter(azimuth_rad, elevation, s=20, c='b', alpha=0.6, label="衛星")
    ax.set_title(title)
    plt.legend()
    plt.show()

# 主流程
input_file = "LOG01077.obs"  # 替換為你的檔案
output_file = "filtered.obs"

header, satellites = parse_obs_file(input_file)

# 原始 Skyplot
plot_skyplot(satellites, title="原始 Skyplot")

# 進行篩選
filtered_satellites = filter_satellites(satellites, AZIMUTH_RANGE, ELEVATION_MIN)

# 篩選後的 Skyplot
plot_skyplot(filtered_satellites, title="篩選後 Skyplot")

# 輸出新 .obs 檔案
save_new_obs_file(output_file, header, filtered_satellites)

print(f"已產生新的 OBS 檔案: {output_file}")
