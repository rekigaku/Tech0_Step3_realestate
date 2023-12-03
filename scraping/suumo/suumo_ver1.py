import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# 空のDataFrameを作成
columns = ["物件名", "住所", "アクセス", "築年数", "階数", "家賃", "管理費", "間取り", "広さ"]
df = pd.DataFrame(columns=columns)

# ベースとなるURL（ページ番号を含む）
base_url = "https://bridal.suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13107&sc=13109&sc=13110&sc=13111&sc=13112&sc=13115&cb=0.0&ct=9999999&et=10&ts=1&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1"

# 1ページから135ページまでスクレイピング
for page_num in range(1, 136):
    # ページ番号をURLに組み込む
    url = f"{base_url}&page={page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sleep(1)

    # 各物件の情報をループ
    for property_row in soup.find_all('div', class_='cassetteitem'):
        property_name = property_row.find('div', class_='cassetteitem_content-title').text.strip()  # 物件名
        address = property_row.find('li', class_='cassetteitem_detail-col1').text.strip()  # 住所
        access = ' '.join([div.text.strip() for div in property_row.find_all('div', class_='cassetteitem_detail-text')])  # アクセス
        age = property_row.find('li', class_='cassetteitem_detail-col3').div.text.strip()  # 築年数

        # 同じ物件の異なる部屋情報を取得
        for room_row in property_row.find_all('tbody')[0].find_all('tr'):
            floor = room_row.find_all('td')[2].text.strip()  # 階数
            rent = room_row.find_all('td')[3].text.strip()  # 家賃
            management_fee = room_row.find_all('td')[4].text.strip() if room_row.find_all('td')[4].text.strip() != '-' else '0円'  # 管理費
            layout = room_row.find_all('td')[6].text.strip()  # 間取り
            size = room_row.find_all('td')[7].text.strip()  # 広さ

            # 新しい行を作成してDataFrameに追加
            new_row = pd.DataFrame([[property_name, address, access, age, floor, rent, management_fee, layout, size]], columns=columns)
            df = pd.concat([df, new_row], ignore_index=True)

# DataFrameをCSVファイルに出力
csv_file = 'suumo_rental_data.csv' 
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
