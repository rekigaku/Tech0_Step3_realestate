import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

base_url = "https://airdoor.jp/list?si=d-131016-131024-131032-131041-131059-131075-131091-131105-131113-131121-131130-131156-131164-131202-132021-132039-132047&a_id=16&o=arrived"

properties = []

for page_num in range(1, 81):
    # URLを修正: &page=と&p=の両方を含む
    url = f"{base_url}&page=80&p={page_num}"
    print("Accessing URL:", url)  # 現在のURLを表示
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 物件情報を含む全ての要素を検索
    property_panels = soup.find_all("div", class_="PropertyPanel_propertyPanel__MqCpF")

    for panel in property_panels:
        property_info = {}

        # 物件名
        property_info["物件名"] = panel.find("div", class_="PropertyPanelBuilding_buildingTitle__NbWmb").get_text(strip=True)

        # 住所、アクセス、築年数
        building_info = panel.find("div", class_="PropertyPanelBuilding_buildingInformation__kRI1U")
        property_info["住所"] = building_info.find_all("p")[2].get_text(strip=True)
        property_info["アクセス"] = building_info.find_all("p")[0].get_text(strip=True) + ", " + building_info.find_all("p")[1].get_text(strip=True)
        property_info["築年数"] = building_info.find_all("p")[3].get_text(strip=True)

        # 各部屋の情報
        rooms = panel.find_all("a", class_="PropertyPanelRoom_roomItem__3bVhC")
        for room in rooms:
            room_info = property_info.copy()  # 物件情報のコピーを作成

            room_info["階数"] = room.find("span", class_="is-ml5").get_text(strip=True).split("/")[0]
            room_info["家賃"] = room.find("div", class_="PropertyPanelRoom_rentPrice__HO4Jp").get_text(strip=True).split("(")[0]
            room_info["管理費"] = room.find("div", class_="PropertyPanelRoom_rentPrice__HO4Jp").get_text(strip=True).split("(")[1].strip(")")
            layout_and_size = room.find("span", class_="is-ml5").get_text(strip=True).split("/")
            room_info["間取り"] = layout_and_size[1].strip()
            room_info["広さ"] = layout_and_size[2].strip()

            properties.append(room_info)
    
    # Sleep処理
    time.sleep(1)

# データフレームに変換
df_properties = pd.DataFrame(properties)

# CSVファイルに保存
df_properties.to_csv('property_data.csv', index=False, encoding='utf-8-sig')

# 最終の数件の結果を表示
df_properties.tail()

