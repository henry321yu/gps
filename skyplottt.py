import numpy as np
import matplotlib.pyplot as plt
import georinex as gr

# 觀測站坐標 (APPROX POSITION XYZ) - 請換成你的數據
Xr, Yr, Zr = 1111111.0, 2222222.0, 3333333.0

# 讀取 RINEX 觀測檔和導航檔
# obs = gr.load("你的觀測檔.obs")  # 請替換為實際的 .obs 檔案路徑
nav = gr.load("LOG01077.nav")  # 請替換為實際的 .nav 檔案路徑

def compute_azimuth_elevation(Xs, Ys, Zs, Xr, Yr, Zr):
    dX, dY, dZ = Xs - Xr, Ys - Yr, Zs - Zr
    rho = np.sqrt(dX**2 + dY**2)
    elevation = np.arctan2(dZ, rho) * 180 / np.pi  # 轉換為度
    azimuth = np.arctan2(dY, dX) * 180 / np.pi
    if azimuth < 0:
        azimuth += 360  # 確保範圍在 0-360°
    return azimuth, elevation

# 檢查 nav 的結構
print(nav)

# 提取衛星 PRN
prns = nav.coords['sv'].values  # 這行根據實際結構調整

# 提取衛星位置
sat_positions = {}

for prn in prns:
    try:
        Xs, Ys, Zs = nav.sel(sv=prn)['X'].values, nav.sel(sv=prn)['Y'].values, nav.sel(sv=prn)['Z'].values
        sat_positions[prn] = (Xs, Ys, Zs)
    except KeyError:
        print(f"警告: PRN {prn} 沒有完整的 X, Y, Z 坐標數據，跳過")

# 記錄方位角與仰角
azimuths, elevations, prn_labels = [], [], []

for prn, (Xs, Ys, Zs) in sat_positions.items():
    az, el = compute_azimuth_elevation(Xs, Ys, Zs, Xr, Yr, Zr)
    if el > 0:  # 只顯示仰角大於 0 的衛星
        azimuths.append(np.radians(az))  # 轉換為弧度
        elevations.append(90 - el)  # Skyplot 以 90° 為天頂
        prn_labels.append(prn)

# 建立 Skyplot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N')  # 0° 指向北方
ax.set_theta_direction(-1)  # 角度順時針遞增
ax.set_ylim(0, 90)  # 設定範圍 (0 = 天頂, 90 = 地平線)
ax.set_yticks(range(0, 91, 30))  # 設定刻度

# 繪製衛星位置
ax.scatter(azimuths, elevations, c='r', marker='o', label="Satellites")

# 標示 PRN
for i, prn in enumerate(prn_labels):
    ax.text(azimuths[i], elevations[i], prn, fontsize=12, ha='center', va='center', color='blue')

ax.set_title("Skyplot of Satellites")
plt.legend()
plt.show()
