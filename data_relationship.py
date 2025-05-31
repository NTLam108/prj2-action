import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# 1. Đọc dữ liệu từ file CSV
file_path = 'data.csv'
df = pd.read_csv(file_path)

# 2. Kiểm tra cột chứa thông tin địa điểm (thay 'Location' bằng tên cột thực tế trong file của bạn)
location_column = 'Location'  # Ví dụ: 'City', 'Station', 'District'
locations = df[location_column].unique()

print(f" Các địa điểm trong dữ liệu: {list(locations)}")

# 3. Lặp qua từng địa điểm để phân tích riêng
for location in locations:
    print(f"\n Đang phân tích dữ liệu cho {location}...")
    
    # Lọc dữ liệu theo địa điểm
    df_location = df[df[location_column] == location].copy()
    
    # Làm sạch dữ liệu (xử lý missing values)
    df_location_cleaned = df_location.dropna()
    
    # Tính toán ma trận tương quan với AQI
    correlation_matrix = df_location_cleaned.select_dtypes(include=['number']).corr(method='pearson')
    aqi_correlations = correlation_matrix['AQI'].sort_values(ascending=False)
    
    print(f"\n Hệ số tương quan giữa AQI và các chỉ số tại {location}:")
    print(aqi_correlations)
    
    # Vẽ heatmap tương quan
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Ma trận tương quan tại {location}')
    plt.show()
    
    # Vẽ scatter plot cho 3 chỉ số tương quan mạnh nhất với AQI (trừ chính AQI)
    top_features = aqi_correlations.index[1:4]  # Bỏ qua 'AQI' (tự tương quan)
    
    for feature in top_features:
        plt.figure(figsize=(8, 5))
        sns.regplot(x=feature, y='AQI', data=df_location_cleaned, 
                    scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
        plt.title(f'Mối quan hệ giữa AQI và {feature} tại {location}')
        plt.show()
    
    # Phân tích hồi quy tuyến tính (nếu có đủ dữ liệu)
    if len(top_features) >= 1:
        X = df_location_cleaned[top_features]
        y = df_location_cleaned['AQI']
        
        model = LinearRegression()
        model.fit(X, y)
        
        print(f"\n Kết quả hồi quy tuyến tính tại {location}:")
        print(f"- Các biến độc lập: {list(top_features)}")
        print(f"- Hệ số hồi quy (ảnh hưởng lên AQI):")
        for feature, coef in zip(top_features, model.coef_):
            print(f"  + {feature}: {coef:.4f}")
        print(f"- Độ chính xác (R²): {model.score(X, y):.2f}")

# 4. Xuất dữ liệu đã làm sạch theo từng địa điểm (tùy chọn)
output_folder = 'location_data/'
import os
os.makedirs(output_folder, exist_ok=True)

for location in locations:
    df_location = df[df[location_column] == location]
    df_location.to_csv(f'{output_folder}{location}_data.csv', index=False)

print(f"\nĐã lưu dữ liệu từng địa điểm vào thư mục '{output_folder}'")
