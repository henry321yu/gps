import serial
from datetime import datetime, timedelta

def parse_nmea(data):
    """解析 NMEA 資料，回傳時間和衛星數"""
    utc_time = None
    satellite_count = None

    try:
        fields = data.split(',')
        if data.startswith('$GNGGA') or data.startswith('$GPGGA'):
            # UTC 時間 (第 1 欄)
            utc_time = fields[1]
            if utc_time:
                # 轉換成 UTC+8 時間
                hours = int(utc_time[0:2])
                minutes = int(utc_time[2:4])
                seconds = int(utc_time[4:6])
                utc_datetime = datetime.utcnow().replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
                local_datetime = utc_datetime + timedelta(hours=8)
                utc_time = local_datetime.strftime('%H:%M:%S')

            # 衛星數 (第 7 欄)
            satellite_count = fields[7] if fields[7].isdigit() else None
    except (IndexError, ValueError):
        # 忽略解析錯誤，返回 None
        pass

    return utc_time, satellite_count

def main():
    # 設定 USB 串口
    port = 'COM3'  # 根據實際情況修改
    baud_rate = 115200       # 根據裝置設定
    ser = serial.Serial(port, baud_rate, timeout=1)

    print("正在接收 NMEA 資料...")

    try:
        while True:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line:
                utc_time, satellite_count = parse_nmea(line)
                if utc_time and satellite_count:
                    print(f"UTC+8 時間: {utc_time}, 衛星數: {satellite_count}")
                else:
                    # 處理未知字串但不停止程式
                    print(f"未知字串: {line}")
    except KeyboardInterrupt:
        print("\n程式結束")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
