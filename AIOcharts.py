import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

CSV_FILE = "data.csv"

# Các chỉ số muốn vẽ (đã bỏ "Pressure")
INDICATORS = [
    "AQI", "PM2.5", "PM10", "CO", "NO2", "O3", "SO2",
    "Temperature", "Humidity", "Wind Speed"
]

# Màu mặc định cho từng chỉ số (tương ứng số lượng chỉ số hiện tại)
COLORS = [
    "blue", "green", "red", "orange", "purple", "brown",
    "pink", "black", "cyan", "magenta", "olive"
]

# Thư mục lưu ảnh đầu ra
OUTPUT_DIR = "AIOcharts"

def draw_all_metrics_by_station():
    if not os.path.exists(CSV_FILE):
        print("Không tìm thấy file dữ liệu.")
        return

    df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    for col in INDICATORS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['Timestamp', 'Station Name'])
    df = df.sort_values("Timestamp")

    stations = df['Station Name'].unique()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for station in stations:
        sub_df = df[df['Station Name'] == station]
        if len(sub_df) < 2:
            continue

        plt.figure(figsize=(14, 8))

        for indicator, color in zip(INDICATORS, COLORS):
            if indicator in sub_df.columns and sub_df[indicator].notna().sum() > 0:
                plt.plot(
                    sub_df['Timestamp'], sub_df[indicator],
                    marker='o', linestyle='-', label=indicator,
                    color=color, alpha=0.8
                )

        plt.title(f"Các chỉ số theo thời gian - {station}")
        plt.xlabel("Thời gian")
        plt.ylabel("Giá trị")
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.tight_layout()

        safe_name = station.replace('/', '_').replace(' ', '_').replace(':', '_')
        filename = f"{OUTPUT_DIR}/{safe_name}.png"
        plt.savefig(filename, dpi=300)
        plt.close()

if __name__ == "__main__":
    draw_all_metrics_by_station()

