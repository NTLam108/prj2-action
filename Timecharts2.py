import pandas as pd
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu
df = pd.read_csv("data.csv", encoding='utf-8-sig')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['hour'] = df['Timestamp'].dt.hour

# Chỉ số cần vẽ
value_col = "PM2.5"

# Tạo thư mục lưu ảnh nếu chưa có
output_dir = "Timechart2"
os.makedirs(output_dir, exist_ok=True)

# Tính trung bình và độ lệch chuẩn PM2.5 theo giờ
agg = df.groupby('hour')[value_col].agg(['mean', 'std']).reset_index()

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
plt.plot(agg['hour'], agg['mean'], marker='o', color='blue', label='PM2.5 trung bình')
plt.fill_between(agg['hour'], agg['mean'] - agg['std'], agg['mean'] + agg['std'],
                 color='skyblue', alpha=0.3, label='± Độ lệch chuẩn')

plt.title('PM2.5 trung bình theo giờ trong ngày (nhiều ngày)')
plt.xlabel('Giờ trong ngày')
plt.ylabel('PM2.5 (µg/m³)')
plt.xticks(range(0, 24))
plt.grid(True)
plt.legend()
plt.tight_layout()

# Lưu ảnh
output_path = os.path.join(output_dir, "PM2.5_by_hour.png")
plt.savefig(output_path, dpi=300)
plt.close()


