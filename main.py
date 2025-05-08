import requests
import pandas as pd
import time
import os
from datetime import datetime

CSV_FILE = "air_quality_weather_data.csv"

# Danh sách AQI ID của các trạm
AQI_IDS = ["13427", "13026", "13415","13439", "13422", "12960", "13027", 
           "13668", "5506", "13763", "14927", "12488", "1584", "13762", 
           "1585", "14643", "14642"]  

# Hàm đánh giá mức độ ô nhiễm
def get_aqi_level(aqi):
    if aqi is None:
        return "Không xác định"
    try:
        aqi = float(aqi)
        if aqi <= 50:
            return "Tốt"
        elif aqi <= 100:
            return "Trung bình"
        elif aqi <= 150:
            return "Không tốt cho nhóm nhạy cảm"
        elif aqi <= 200:
            return "Không tốt"
        elif aqi <= 300:
            return "Rất không tốt"
        else:
            return "Nguy hại"
    except:
        return "Không xác định"

# Hàm lấy dữ liệu từ API WAQI
def fetch_air_quality(id):
    url_aqi = f"https://api.waqi.info/feed/@{id}/?token=cc9a9074d2c475fcefb75d5d98a0c6bddb2866eb"
    response = requests.get(url_aqi)
    if response.status_code != 200:
        print(f"Lỗi khi lấy dữ liệu AQI cho ID {id}")
        return None

    data = response.json()
    try:
        name = data['data']['city']['name']
        timestamp = data['data']['time']['s']
        aqi = data['data'].get('aqi', None)
        iaqi = data['data'].get('iaqi', {})
        geo = data['data']['city'].get('geo', [None, None])
        
        return {
            "Timestamp": timestamp,
            "Station Name": name,
            "Latitude": geo[0],
            "Longitude": geo[1],
            "AQI": aqi,
            "PM2.5": iaqi.get('pm25', {}).get('v', None),
            "PM10": iaqi.get('pm10', {}).get('v', None),
            "CO": iaqi.get('co', {}).get('v', None),
            "NO2": iaqi.get('no2', {}).get('v', None),
            "O3": iaqi.get('o3', {}).get('v', None),
            "SO2": iaqi.get('so2', {}).get('v', None),
            "Temperature": iaqi.get('t', {}).get('v', None),
            "Humidity": iaqi.get('h', {}).get('v', None),
            "Pressure": iaqi.get('p', {}).get('v', None),
            "Wind Speed": iaqi.get('w', {}).get('v', None),
            "Air Quality Level": get_aqi_level(aqi),
        }
    except Exception as e:
        print("Lỗi khi xử lý dữ liệu AQI:", e)
        return None

# === MAIN LOGIC ===
def main():
    all_data = []

    for station_id in AQI_IDS:
        data = fetch_air_quality(station_id)
        if data:
            all_data.append(data)
        time.sleep(1)  # Tránh gọi API quá nhanh

    if all_data:
        df = pd.DataFrame(all_data)

        # Nếu file chưa tồn tại, ghi với header. Ngược lại, ghi tiếp mà không có header.
        if not os.path.isfile(CSV_FILE):
            df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
            print(f"Đã tạo file mới và lưu dữ liệu vào {CSV_FILE}")
        else:
            df.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            print(f"Đã cập nhật dữ liệu vào file {CSV_FILE}")
    else:
        print("Không có dữ liệu để ghi.")

if __name__ == "__main__":
    main()
