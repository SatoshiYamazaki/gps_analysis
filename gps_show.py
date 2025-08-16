import exifread


def read_exif_from_image(image_path):
    """画像ファイルからEXIFデータを読み込む"""
    try:
        with open(image_path, "rb") as f:
            exif_data = exifread.process_file(f)
        return exif_data
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {image_path}")
        return None
    except IOError:
        print(f"ファイルの読み込みに失敗しました: {image_path}")
        return None

        
def dms_to_decimal(dms):
    """度分秒（DMS）リストから10進数の座標に変換する関数"""
    degrees, minutes, seconds = dms
    return degrees + (minutes / 60) + (seconds / 3600)


def get_coordinates(exif_data):
    """EXIFタグから緯度と経度を抽出してタプルで返す"""
    try:
        pre_latitude = eval(exif_data["GPS GPSLatitude"].printable)
        pre_longitude = eval(exif_data["GPS GPSLongitude"].printable)
        latitude = dms_to_decimal(pre_latitude)
        longitude = dms_to_decimal(pre_longitude)
        return (latitude, longitude)
    except KeyError:
        print("必要なGPS情報が含まれていません。")
        return None


def main():
    image_path = "sample.HEIC"
    image_path = "/Users/yamapan.121sy/workspace/gps_data/2025-08-16 14.35.30.jpg"
    image_path = "/Users/yamapan.121sy/workspace/gps_data/2025-08-15 10.54.32.HEIC"

    exif_data = read_exif_from_image(image_path)
    if exif_data:
        coordinates = get_coordinates(exif_data)
        if coordinates:
            print("緯度経度:", coordinates)
        else:
            print("GPS情報の取得に失敗しました。")
    else:
        print("EXIFデータの読み込みに失敗しました。")


if __name__ == "__main__":
    main()

