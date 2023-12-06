import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 基本となるURL
base_url = "https://www.goodrooms.jp/tokyo/search/area_list/"

# 初期パラメータ
params = {
    'layout': '1LDK-2K-2DK-2LDK-3K-3DK-3LDK-3LDK_more',
    'small_area_cd': '1000-1001-1002-1003-1004-1005-1011-1020-1021-1022-1030-1031-1032-1033',
    'rent_select': '1',
    'is_contain_full': '0'
}

# 物件情報を格納するリスト
properties = []

# 85ページ分のデータをループで取得
for page_num in range(1, 86):
    # ページ番号をパラメータに追加
    params['p'] = page_num

    # 完成したURLを生成して表示
    full_url = requests.Request('GET', base_url, params=params).prepare().url
    print("Accessing URL:", full_url)

    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 各物件の情報を取得
    estate_elements = soup.find_all("div", class_="searchEstateList__info")
    for estate in estate_elements:
        property_info = {}

        # 物件名（クラス名に注意）
        property_name_element = estate.find("h2", class_="searchEstateList__title")
        
        if property_name_element:
            property_info["物件名"] = property_name_element.get_text(strip=True)
        else:
            continue  # 物件名が見つからない場合はこの物件をスキップ

        # 住所、階数、間取り、広さ（クラス名に注意）
        spec_text = estate.find("div", class_="searchEstateList__spec").get_text(separator=" / ", strip=True).split(" / ")
        if len(spec_text) >= 4:  # 必要な情報が全て含まれているか確認
            property_info["住所"] = spec_text[0]
            property_info["階数"] = spec_text[1]
            property_info["間取り"] = spec_text[2]
            property_info["広さ"] = spec_text[3]
        else:
            continue  # 必要な情報が不足している場合はスキップ

        # アクセス情報（クラス名に注意）
        access_element = estate.find("div", class_="searchEstateList__traffic")
        property_info["アクセス"] = access_element.get_text(strip=True) if access_element else '情報なし'

        # 家賃と管理費（クラス名に注意）
        price_element = estate.find("div", class_="searchEstateList__price")
        if price_element:
            price_info = price_element.get_text(separator=" / ", strip=True).split(" / ")
            property_info["家賃"] = price_info[0]
            property_info["管理費"] = price_info[1].replace("管理費", "").strip() if len(price_info) > 1 else '情報なし'
        else:
            property_info["家賃"] = '情報なし'
            property_info["管理費"] = '情報なし'

        properties.append(property_info)
        print(property_info)  # 各物件の情報をコンソールに表示

    time.sleep(1)  # サーバーに負担をかけないようにウェイトを設定

# データフレームに変換
df_properties = pd.DataFrame(properties)

# CSVファイルに保存
df_properties.to_csv('goodrooms_property_data.csv', index=False, encoding='utf-8-sig')
