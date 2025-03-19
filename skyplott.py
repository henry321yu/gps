import numpy as np
import matplotlib.pyplot as plt
from pyubx2 import UBXReader

def read_obs_file(file_path):
    satellites = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.split()
            
            # 確保每行包含有效的數字資料
            if len(parts) > 2 and parts[0].isdigit():
                try:
                    # 嘗試轉換方位角和仰角
                    azimuth = float(parts[1])  # 方位角
                    elevation = float(parts[2])  # 仰角
                    
                    # 如果轉換成功，將衛星資料加入列表
                    satellite = {
                        'prn': int(parts[0]),   # 衛星編號
                        'azimuth': azimuth,
                        'elevation': elevation
                    }
                    satellites.append(satellite)
                except ValueError:
                    # 如果轉換失敗（非數字資料），則忽略該行
                    continue

    return satellites


def plot_skyplot(satellites):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')

    for sat in satellites:
        # 將仰角轉換為弧度，方位角也轉換為弧度
        azimuth = np.deg2rad(sat['azimuth'])
        elevation = np.deg2rad(sat['elevation'])

        # 使用方位角和仰角來繪製衛星位置
        if elevation > 0:  # 只繪製仰角大於 0 的衛星
            ax.scatter(azimuth, elevation, marker='o', color='b')

    ax.set_ylim(0, np.pi/2)  # 限制仰角範圍在 0 到 90 度
    ax.set_title("Skyplot")

    # 設定標籤和網格
    ax.set_xlabel("Azimuth (degrees)")
    ax.set_ylabel("Elevation (degrees)")
    ax.grid(True)

    plt.show()

# 讀取 .obs 檔案資料
satellites = read_obs_file('test.obs')

# 繪製 Skyplot
plot_skyplot(satellites)
