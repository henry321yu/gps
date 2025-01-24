import serial
from datetime import datetime, timedelta

def parse_nmea(data):
    """解析 NMEA 資料，回傳時間和所有衛星數"""
    utc_time = None
    satellites_in_view = None

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

        if data.startswith('$GNGSV') or data.startswith('$GPGSV'):
            # 總衛星數 (第 3 欄)
            if fields[3].isdigit():
                satellites_in_view = int(fields[3])
    except (IndexError, ValueError):
        # 忽略解析錯誤，返回 None
        pass

    return utc_time, satellites_in_view

def main():
    # 設定 USB 串口
    port = 'COM3'  # 根據實際情況修改
    baud_rate = 115200       # 根據裝置設定
    ser = serial.Serial(port, baud_rate, timeout=1)

    print("正在接收 NMEA 資料...")

    # 用於累積衛星數的變數
    last_satellites_in_view = None
    last_utc_time = None

    try:
        while True:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line:
                utc_time, satellites_in_view = parse_nmea(line)

                # 更新時間
                if utc_time:
                    last_utc_time = utc_time

                # 確認衛星數據
                if satellites_in_view is not None:
                    # 只有當總衛星數改變時才顯示
                    if satellites_in_view != last_satellites_in_view:
                        last_satellites_in_view = satellites_in_view
                        if last_utc_time:
                            print(f"{last_utc_time}, 總衛星數: {satellites_in_view}")
                        else:
                            print(f"總衛星數: {satellites_in_view}")
    except KeyboardInterrupt:
        print("\n程式結束")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
