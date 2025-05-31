import pandas as pd
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu từ file CSV
df = pd.read_csv("data.csv", encoding='utf-8-sig')

# Chuyển cột thời gian sang định dạng datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Tạo cột ngày và giờ từ Timestamp
df['date'] = df['Timestamp'].dt.date
df['hour'] = df['Timestamp'].dt.hour

# Cột dữ liệu muốn vẽ: AQI
value_col = "AQI"

# Tạo thư mục lưu ảnh nếu chưa có
output_dir = "AQI_Timechart"
os.makedirs(output_dir, exist_ok=True)

# Lấy danh sách các trạm đo duy nhất
stations = df['Station Name'].unique()

for station in stations:
    df_station = df[df['Station Name'] == station]

    plt.figure(figsize=(12, 6))
    for date, group in df_station.groupby('date'):
        plt.plot(group['hour'], group[value_col], marker='o', label=str(date))

    plt.title(f"{value_col} theo giờ trong ngày - Trạm: {station}")
    plt.xlabel("Giờ trong ngày")
    plt.ylabel(value_col)
    plt.xticks(range(0, 24))
    plt.legend(title='Ngày', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()

    # Làm sạch tên trạm để dùng làm tên file
    safe_station_name = "".join(c if c.isalnum() or c in (' ', '-') else '_' for c in station).strip()
    output_file = os.path.join(output_dir, f"{safe_station_name}_{value_col}_time_chart.png")

    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Đã lưu biểu đồ AQI của trạm '{station}' vào: {output_file}")
