import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 讀取 CSV
file_path = r"D:\gps file\auto_rinex_time_ranges.csv"
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 合併時間
df['start'] = pd.to_datetime(df['開始日期(UTC+8)'] + ' ' + df['開始時間(UTC+8)'])
df['end']   = pd.to_datetime(df['結束日期(UTC+8)'] + ' ' + df['結束時間(UTC+8)'])

# 取得時間範圍
start_date = df['start'].min().normalize()
end_date   = df['end'].max().normalize()

# 建立完整日期序列
all_days = pd.date_range(start=start_date, end=end_date, freq='D')

# === 🎨 建立顏色對應 ===
files = df['原檔案'].unique()
cmap = plt.get_cmap('tab20')  # 可改 tab10 / viridis / rainbow

color_map = {f: cmap(i % 20) for i, f in enumerate(files)}

# 畫圖
fig, ax = plt.subplots(figsize=(14, 6))

for _, row in df.iterrows():
    current = row['start']
    end = row['end']
    file_name = row['原檔案']
    color = color_map[file_name]

    while current.date() <= end.date():
        day_start = datetime.combine(current.date(), datetime.min.time())
        day_end = day_start + timedelta(days=1)

        segment_start = max(current, day_start)
        segment_end = min(end, day_end)

        y_start = segment_start.hour + segment_start.minute/60 + segment_start.second/3600
        y_end   = segment_end.hour + segment_end.minute/60 + segment_end.second/3600

        x = (segment_start.date() - start_date.date()).days

        ax.plot([x, x], [y_start, y_end],
                linewidth=4,
                color=color)

        current = day_end

# X軸
ax.set_xticks(range(len(all_days)))
ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in all_days], rotation=45)

# Y軸
ax.set_ylim(0, 24)
ax.set_ylabel("Hour of Day")
ax.set_xlabel("Date")

# === 🧾 Legend（避免重複）===
handles = []
labels = []
for f, c in color_map.items():
    handles.append(plt.Line2D([0], [0], color=c, lw=4))
    labels.append(f)

ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# 格線
ax.grid(True, linestyle='--', alpha=0.4)

plt.title("GPS Time Coverage (Colored by File)")
plt.tight_layout()
plt.show()