import pandas as pd
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu
df = pd.read_csv("data.csv", encoding='utf-8-sig')

# Chuyển Timestamp sang datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Hàm tách tên thành phố từ "Station Name"
def extract_city(station_name):
    if pd.isna(station_name):
        return "Không xác định"
    parts = station_name.split(',')
    if len(parts) >= 2:
        return parts[-1].strip()
    return "Không xác định"

df['City'] = df['Station Name'].apply(extract_city)

# Tạo thư mục lưu hình nếu chưa có
output_folder = "CityCharts"
os.makedirs(output_folder, exist_ok=True)

# Danh sách các thành phố duy nhất
cities = df['City'].unique()

for city in cities:
    df_city = df[df['City'] == city]
    if df_city.empty:
        continue

    plt.figure(figsize=(14,7))
    stations = df_city['Station Name'].unique()

    for station in stations:
        station_data = df_city[df_city['Station Name'] == station]
        plt.plot(station_data['Timestamp'], station_data['PM2.5'], marker='o', label=station)

    plt.title(f"Chỉ số PM2.5 theo thời gian - {city}")
    plt.xlabel("Thời gian")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()

    # Lưu file png, đổi khoảng trắng thành dấu gạch dưới
    filename = city.replace(' ', '_') + ".png"
    filepath = os.path.join(output_folder, filename)
    plt.savefig(filepath)
    plt.close()  # Đóng figure để tiết kiệm bộ nhớ

 
