import pandas as pd
import matplotlib.pyplot as plt

# 讀取 RINEX `.obs` 文件
obs_file = "output.obs"
data = pd.read_csv(obs_file, delim_whitespace=True, comment='>', header=None)

# 過濾衛星數據（假設衛星 PRN 在第 1 列，仰角在第 3 列，方位角在第 4 列）
sat_data = data[[1, 3, 4]].dropna()

# 繪製 skyplot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(sat_data[4] * (3.14159 / 180), 90 - sat_data[3], label="Satellites")  # 轉換為極座標
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
plt.show()
