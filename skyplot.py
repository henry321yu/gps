import numpy as np
import matplotlib.pyplot as plt

def parse_obs_file(obs_file):
    print("parse_obs_file(obs_file):")
    azimuths = []
    elevations = []
    prn_list = []  # 儲存衛星 PRN 號

    with open(obs_file, 'r', encoding='ascii') as file:
        lines = file.readlines()

    data_start = False
    for line in lines:
        if "END OF HEADER" in line:
            data_start = True
            continue
        if not data_start:
            continue  # 跳過 Header

        # 解析衛星數據行
        tokens = line.split()
        if len(tokens) < 5:
            continue  # 略過無效行

        # 檢查是否是衛星數據行（以 G 或 R 開頭）
        if tokens[0].startswith('G') or tokens[0].startswith('R') or tokens[0].startswith('E'):
            # print(tokens)
            try:
                prn = tokens[0]  # 衛星 PRN
                az = float(tokens[1])  # 方位角
                el = float(tokens[3])  # 仰角（假設仰角在第四列）

                azimuths.append(az)
                elevations.append(el)
                prn_list.append(prn)
            except ValueError:
                continue  # 避免轉換錯誤

    return azimuths, elevations, prn_list

#### **步驟 2：繪製 Skyplot**
def plot_skyplot(azimuths, elevations, prn_list):
    print("plot_skyplot(azimuths, elevations, prn_list):")
    print(azimuths)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(90, 0)  # 90 度在外圈，0 度在內圈
    ax.set_yticks([0, 30, 60, 90])
    ax.set_yticklabels(["90°", "60°", "30°", "0°"])
        
    ax.scatter(np.radians(azimuths), 90 - np.array(elevations), s=50)
        
    plt.title("GNSS Skyplot")
    plt.show()

# **執行**
obs_file = "C:\\Users\\sgrc-325\\Desktop\\git\\test.obs"
azimuths, elevations, prn_list = parse_obs_file(obs_file)
plot_skyplot(azimuths, elevations, prn_list)
