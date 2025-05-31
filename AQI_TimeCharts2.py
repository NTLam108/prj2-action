import pandas as pd
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu
df = pd.read_csv("data.csv", encoding='utf-8-sig')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['hour'] = df['Timestamp'].dt.hour

# Chỉ số cần vẽ
value_col = "AQI"

# Chuyển dữ liệu AQI sang số
df[value_col] = pd.to_numeric(df[value_col], errors='coerce')

# Tạo thư mục lưu ảnh nếu chưa có
output_dir = "AQI_Timechart2"
os.makedirs(output_dir, exist_ok=True)

# Lấy danh sách các trạm (thành phố) duy nhất
stations = df['Station Name'].unique()

for station in stations:
    df_station = df[df['Station Name'] == station]
    
    if df_station.empty:
        continue
    
    agg = df_station.groupby('hour')[value_col].agg(['mean', 'std']).reset_index()

    plt.figure(figsize=(12, 6))
    plt.plot(agg['hour'], agg['mean'], marker='o', color='red', label='AQI trung bình')
    plt.fill_between(agg['hour'], agg['mean'] - agg['std'], agg['mean'] + agg['std'],
                     color='salmon', alpha=0.3, label='± Độ lệch chuẩn')

    plt.title(f'AQI trung bình theo giờ - Trạm: {station}')
    plt.xlabel('Giờ trong ngày')
    plt.ylabel('AQI')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Làm sạch tên trạm để dùng đặt tên file
    safe_name = "".join(c if c.isalnum() or c in (' ', '-') else '_' for c in station).strip()
    output_path = os.path.join(output_dir, f"{safe_name}_AQI_std_by_hour.png")
    
    plt.savefig(output_path, dpi=300)
    plt.close()


