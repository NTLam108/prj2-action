import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime

# Tạo thư mục CityCharts nếu chưa tồn tại
output_dir = "CityCharts"
os.makedirs(output_dir, exist_ok=True)

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data.csv')

# Chuyển đổi cột Timestamp sang kiểu datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Lọc các trạm ở Vũng Tàu (đã điều chỉnh tên trạm)
vung_tau_stations = df[df['Station Name'].str.contains('Vũng Tàu|Vung Tau|Bà Rịa - Vũng Tàu|BR-VT', case=False, na=False)]

# Kiểm tra nếu không có dữ liệu
if vung_tau_stations.empty:
    print("Không tìm thấy dữ liệu trạm Vũng Tàu")
    print("Các thành phố có trong dữ liệu:", df['Station Name'].unique())
    exit()

# Tạo biểu đồ với kích thước lớn hơn
plt.figure(figsize=(16, 9))

# Màu sắc đa dạng cho các trạm
colors = plt.cm.tab20.colors

# Vẽ đường PM2.5 cho từng trạm
for i, station in enumerate(vung_tau_stations['Station Name'].unique()):
    station_data = vung_tau_stations[vung_tau_stations['Station Name'] == station]
    plt.plot(station_data['Timestamp'], 
             station_data['PM2.5'], 
             label=station, 
             color=colors[i % len(colors)],
             marker='o', 
             markersize=5,
             linestyle='-',
             linewidth=2,
             alpha=0.8)

# Thiết lập định dạng trục x
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m\n%H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Thêm các thành phần cho biểu đồ
plt.title('DIỄN BIẾN CHỈ SỐ PM2.5 TẠI CÁC TRẠM VŨNG TÀU', fontsize=18, pad=20, fontweight='bold')
plt.xlabel('Thời gian', fontsize=14)
plt.ylabel('Nồng độ PM2.5 (µg/m³)', fontsize=14)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# Thêm các ngưỡng chất lượng không khí
plt.axhline(y=25, color='green', linestyle='--', linewidth=1.5, label='Ngưỡng an toàn WHO (25 µg/m³)')
plt.axhline(y=50, color='orange', linestyle='--', linewidth=1.5, label='Ngưỡng cảnh báo (50 µg/m³)')
plt.axhline(y=100, color='red', linestyle='--', linewidth=1.5, label='Ngưỡng nguy hại (100 µg/m³)')

# Đặt chú thích bên ngoài
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Tự động điều chỉnh layout
plt.tight_layout()

# Tạo tên file với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(output_dir, f"VungTau_PM25_{timestamp}.png")

# Lưu biểu đồ với chất lượng cao
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Đã lưu biểu đồ vào: {output_file}")

# Đóng biểu đồ để tiết kiệm bộ nhớ
plt.close()

