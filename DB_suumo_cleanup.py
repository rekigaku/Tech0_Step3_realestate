import pandas as pd

# CSVファイルを読み込む
file_path = 'DB_suumo.csv'  # CSVファイルのパスを指定
df = pd.read_csv(file_path)

# 元のデータ数を表示
print("元のデータ件数:", df.shape[0])

# 重複データを削除する
# 物件名, 築年数、階数、家賃、管理費、間取り、広さ、敷金、礼金の組み合わせが一致したものを削除
columns_to_check = ["物件名", "築年数", "階数", "家賃", "管理費", "間取り", "広さ", "敷金", "礼金"]
df_deduplicated = df.drop_duplicates(subset=columns_to_check)

# 重複データ数を表示
duplicate_count = df.shape[0] - df_deduplicated.shape[0]
print("重複データ件数:", duplicate_count)

df=df_deduplicated

#欠損値の確認
df.isnull().any()

# 'アクセス' カラムが存在するか確認
if 'アクセス' in df.columns:
    # 'アクセス' カラムを '分' で分割し、最大3つの新しいカラムに分割
    df[['アクセス1', 'アクセス2', 'アクセス3']] = df['アクセス'].str.split('分', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス', axis=1, inplace=True)
else:
    print("カラム 'アクセス' が存在しません。")

#アクセス１を分割

# 'アクセス' カラムが存在するか確認
if 'アクセス1' in df.columns:
    # 'アクセス' カラムを '/' で分割し、最大3つの新しいカラムに分割
    df[['アクセス1路線', 'アクセス1駅名と徒歩']] = df['アクセス1'].str.split('/', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス1', axis=1, inplace=True)
else:
    print("カラム 'アクセス1' が存在しません。")
    

#アクセス2を分割

# 'アクセス' カラムが存在するか確認
if 'アクセス2' in df.columns:
    # 'アクセス' カラムを '/' で分割し、最大3つの新しいカラムに分割
    df[['アクセス2路線', 'アクセス2駅名と徒歩']] = df['アクセス2'].str.split('/', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス2', axis=1, inplace=True)
else:
    print("カラム 'アクセス2' が存在しません。")

#アクセス3を分割

# 'アクセス' カラムが存在するか確認
if 'アクセス3' in df.columns:
    # 'アクセス' カラムを '/' で分割し、最大3つの新しいカラムに分割
    df[['アクセス3路線', 'アクセス3駅名と徒歩']] = df['アクセス3'].str.split('/', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス3', axis=1, inplace=True)
else:
    print("カラム 'アクセス3' が存在しません。")


#アクセス１を再分割

# 'アクセス' カラムが存在するか確認
if 'アクセス1駅名と徒歩' in df.columns:
    # 'アクセス' カラムを '駅' で分割し、最大3つの新しいカラムに分割
    df[['アクセス1駅名', 'アクセス1徒歩']] = df['アクセス1駅名と徒歩'].str.split('駅', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス1駅名と徒歩', axis=1, inplace=True)
else:
    print("カラム 'アクセス1駅名と徒歩' が存在しません。")

#アクセス2を再分割

# 'アクセス' カラムが存在するか確認
if 'アクセス2駅名と徒歩' in df.columns:
    # 'アクセス' カラムを '駅' で分割し、最大3つの新しいカラムに分割
    df[['アクセス2駅名', 'アクセス2徒歩']] = df['アクセス2駅名と徒歩'].str.split('駅', n=2, expand=True)
    # 元の 'アクセス' カラムを削除
    df.drop('アクセス2駅名と徒歩', axis=1, inplace=True)
else:
    print("カラム 'アクセス2駅名と徒歩' が存在しません。")
    

# 'アクセス3駅名と徒歩' カラムが存在するか確認
if 'アクセス3駅名と徒歩' in df.columns:
    # 'アクセス3駅名と徒歩' カラムを '駅' で分割し、最大2つの新しいカラムに分割
    df[['アクセス3駅名', 'アクセス3徒歩']] = df['アクセス3駅名と徒歩'].str.split('駅', n=1, expand=True)

    # 分割後のカラムに欠損値がある場合は '0分' で埋める
    df['アクセス3徒歩'] = df['アクセス3徒歩'].fillna('0分')

    # 元の 'アクセス3駅名と徒歩' カラムを削除
    df.drop('アクセス3駅名と徒歩', axis=1, inplace=True)
else:
    print("カラム 'アクセス3駅名と徒歩' が存在しません。")

# 新しいカラムの順序をリストとして作成
new_column_order = ['物件名', '住所', '築年数', '階数', '家賃', '管理費', '間取り', '広さ', '敷金', '礼金',
       '物件画像URL', '物件詳細URL', 'アクセス1路線', 'アクセス1駅名',
       'アクセス1徒歩', 'アクセス2路線', 'アクセス2駅名', 'アクセス2徒歩', 'アクセス3路線', 'アクセス3駅名', 'アクセス3徒歩']

# df を新しいカラムの順序で並べ替え
df = df.reindex(columns=new_column_order)

# "新築" を 0 に置き換え
df['築年数'] = df['築年数'].replace('新築', '0年')

# "築" と "年" を取り除く
df['築年数'] = df['築年数'].str.replace('築', '').str.replace('年', '')

# "階" を取り除く
df['階数'] = df['階数'].str.replace('階', '')

# "万円" を取り除く
df['家賃'] = df['家賃'].str.replace('万円', '')

# "円" を取り除く
df['管理費'] = df['管理費'].str.replace('円', '')

# "万円" を取り除く
df['敷金'] = df['敷金'].str.replace('万円', '')

# "万円" を取り除く
df['礼金'] = df['礼金'].str.replace('万円', '')

# "m2" を取り除く
df['広さ'] = df['広さ'].str.replace('m2', '')

# "歩" を取り除く
# アクセスに関連するカラムが存在するか確認し、存在する場合のみ処理を行う
if 'アクセス1徒歩' in df.columns:
    df['アクセス1徒歩'] = df['アクセス1徒歩'].str.replace('歩', '')
if 'アクセス2徒歩' in df.columns:
    df['アクセス2徒歩'] = df['アクセス2徒歩'].str.replace('歩', '')
if 'アクセス3徒歩' in df.columns:
    df['アクセス3徒歩'] = df['アクセス3徒歩'].str.replace('歩', '').str.replace('分', '')
    
#-を置き換える
df['敷金'] = df['敷金'].str.replace('-', '0')
df['礼金'] = df['礼金'].str.replace('-', '0')

# 結果を新しいCSVファイルに保存
output_file_path = 'DB_suumo_ver3.csv'
df.to_csv(output_file_path, index=False)

# 重複除去後のデータ件数を表示
print("重複除去後のデータ件数:", df_deduplicated.shape[0])

# 保存されたファイルのパスを出力（確認用）
print("Saved deduplicated file to:", output_file_path)



