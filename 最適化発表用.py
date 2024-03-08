import streamlit as st
import time
import pandas as pd

# CSVファイルのパス
csv_file_path = "data25結果.csv"  # CSVファイルのパスを適切なものに置き換える

# ボタンが押されたときの処理
if st.button("CSVファイルを読み込む"):
    # ボタンが押されたら10秒待つ
    with st.spinner("対戦表を作成中..."):
        time.sleep(10)
    
    # CSVファイルを読み込む
    try:
        df = pd.read_csv(csv_file_path)
        st.dataframe(df)
    except FileNotFoundError:
        st.error("CSVファイルが見つかりませんでした。")
