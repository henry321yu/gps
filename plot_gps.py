import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from math import sqrt
from threading import Thread

# 設定序列埠
port = "COM30"
baudrate = 115200  # 根據實際情況調整
dataL = 1000 # 設定要繪圖的資料數
k=5 #y軸留白大小

# 建立存放資料的 deque，只保留最新 100 筆資料
time_data = deque(maxlen=dataL)
lon_data = deque(maxlen=dataL)
lat_data = deque(maxlen=dataL)
sats_data = deque(maxlen=dataL)
hAcc_data = deque(maxlen=dataL)
vAcc_data = deque(maxlen=dataL)
Acc3d_data = deque(maxlen=dataL)

# 初始化繪圖
fig, ax = plt.subplots(figsize=(10, 7))
line_coord, = ax.plot([], [], '.')
ax.set_title("real-time plot")
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")
# 添加文本框
info_text = fig.text(0.7, 0.85, "", ha='left', va='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

def update_plot(frame):
    """更新繪圖資料"""
    if time_data and Acc3d_data:
        # 更新線條資料
        line_coord.set_data(lon_data, lat_data)
        
        # 動態調整 x 軸和 y 軸範圍
        ax.set_xlim(min(lon_data)-k, max(lon_data)+k)
        ax.set_ylim(min(lat_data)-k, max(lat_data)+k)
        
        # # 更新軸標籤
        # ax.set_title(f"time: {time_data[-1]:.3f}   latitude: {lat_data[-1]:.8f}   longitude: {lon_data[-1]:.8f}   numSats: {sats_data[-1]} \nHorizontal Accuracy: {hAcc_data[-1]:.3f}   Vertical Accuracy: {vAcc_data[-1]:.3f}   3D Accuracy: {Acc3d_data[-1]:.3f}" if time_data else "")

        # 更新 textbox 內容
        info_text.set_text(
            f"time: {time_data[-1]:.3f} s\n"
            f"latitude: {lat_data[-1]:.8f}\n"
            f"longitude: {lon_data[-1]:.8f}\n"
            f"numSats: {sats_data[-1]}\n"
            f"hAcc: {hAcc_data[-1]:.3f} m\n"
            f"vAcc: {vAcc_data[-1]:.3f} m\n"
            f"Acc3d: {Acc3d_data[-1]:.3f} m"
        )
    return line_coord

def read_serial_data():
    """讀取序列埠資料並更新 deque"""
    while True:
        # 讀取一行資料並解碼
        line = ser.readline().decode('utf-8').strip()

        if line:  # 確保資料不為空
            data = line.split(',')  # 以 "," 分割資料

            # 檢查資料是否有正確的 10 個數據
            if len(data) == 8:
                try:
                    # 將各個資料轉為浮點數
                    time_value = float(data[0])
                    # date = float(data[1])
                    # gpst = float(data[2])
                    sats = float(data[3])
                    lat = float(data[4])
                    lon = float(data[5])
                    hAcc = float(data[6])
                    vAcc =float(data[7])
                    
                    global k

                    k=5e-6 #y軸留白大小
                    
                    # 計算向量長度 s（若需要）
                    Acc3d = sqrt(hAcc**2 + vAcc**2)

                    # 將時間和 x, y, z,s 存入 deque
                    time_data.append(time_value)
                    lon_data.append(lon)
                    lat_data.append(lat)
                    sats_data.append(sats)
                    hAcc_data.append(hAcc)
                    vAcc_data.append(vAcc)
                    Acc3d_data.append(Acc3d)

                    # 印出資料
                    print(line)
                except ValueError:
                    print(f"資料轉換失敗: {line}")
            else:
                print(f"接收到錯誤的資料格式: {line}")
                print(f"資料數: {len(data) }")

try:
    # 開啟序列埠
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"已連接到 {port}，波特率為 {baudrate}")

    # 啟動繪圖動畫
    ani = FuncAnimation(fig, update_plot, interval=100)

    # 啟動資料讀取執行緒
    data_thread = Thread(target=read_serial_data, daemon=True)
    data_thread.start()

    # 顯示繪圖
    plt.show()

except serial.SerialException as e:
    print(f"序列埠錯誤: {e}")
except KeyboardInterrupt:
    print("程式終止")
finally:
    if ser.is_open:
        ser.close()
        print("已關閉序列埠")
