import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

CSV_FILE = "data.csv"

def draw_aqi_chart_station():
    if not os.path.exists(CSV_FILE):
        print("Không tìm thấy file dữ liệu.")
        return

    df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce')
    df = df.dropna(subset=['Timestamp', 'AQI', 'Station Name'])
    df = df.sort_values("Timestamp")

    stations = df['Station Name'].unique()
    os.makedirs("charts", exist_ok=True)

    for station in stations:
        sub_df = df[df['Station Name'] == station]
        if len(sub_df) < 2:
            continue

        plt.figure(figsize=(10, 6))
        plt.plot(sub_df['Timestamp'], sub_df['AQI'], marker='o', linestyle='-')
        plt.title(f"AQI theo thời gian - {station}")
        plt.xlabel("Thời gian")
        plt.ylabel("Chỉ số AQI")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.tight_layout()

        safe_name = station.replace('/', '_').replace(' ', '_').replace(':', '_')
        filename = f"charts/aqi_{safe_name}.png"
        plt.savefig(filename, dpi=300)
        plt.close()
if __name__ == "__main__":
    draw_aqi_chart_station()
