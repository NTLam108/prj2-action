import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

CSV_FILE = "data.csv"
OUTPUT_DIR = "AIOcharts"

# Danh sách các chỉ số cần vẽ (bỏ Pressure như yêu cầu)
INDICATORS = ["AQI", "PM2.5", "PM10", "CO", "NO2", "O3", "SO2", "Temperature", "Humidity", "Wind Speed"]

# Màu riêng cho từng chỉ số
COLORS = {
    "AQI": "black",
    "PM2.5": "blue",
    "PM10": "green",
    "CO": "orange",
    "NO2": "red",
    "O3": "purple",
    "SO2": "brown",
    "Temperature": "cyan",
    "Humidity": "magenta",
    "Wind Speed": "olive"
}

def draw_all_indicators():
    if not os.path.exists(CSV_FILE):
        print("Không tìm thấy file dữ liệu.")
        return

    df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')

    # Đảm bảo các cột có định dạng đúng
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp', 'Station Name'])
    df = df.sort_values("Timestamp")

    # Tạo thư mục chứa biểu đồ
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stations = df['Station Name'].unique()

    for station in stations:
        sub_df = df[df['Station Name'] == station]

        if len(sub_df) < 2:
            continue  # Bỏ qua nếu ít dữ liệu

        plt.figure(figsize=(14, 8))

        for indicator in INDICATORS:
            if indicator in sub_df.columns and sub_df[indicator].notna().sum() > 0:
                plt.plot(
                    sub_df['Timestamp'],
                    pd.to_numeric(sub_df[indicator], errors='coerce'),
                    marker='o',
                    linestyle='-',
                    label=indicator,
                    color=COLORS.get(indicator, 'gray'),
                    alpha=0.8
                )

        plt.title(f"Tổng hợp các chỉ số chất lượng không khí theo thời gian\nTrạm: {station}")
        plt.xlabel("Thời gian")
        plt.ylabel("Giá trị chỉ số")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.legend()
        plt.tight_layout()

        safe_name = station.replace('/', '_').replace(' ', '_').replace(':', '_')
        filename = f"{OUTPUT_DIR}/{safe_name}.png"
        plt.savefig(filename, dpi=300)
        plt.close()

if __name__ == "__main__":
    draw_all_indicators()

