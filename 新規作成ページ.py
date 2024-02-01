import streamlit as st
import sqlite3
import pandas as pd

# SQLiteデータベースに接続する関数
def get_connection():
    if 'conn' not in st.session_state:
        st.session_state['conn'] = sqlite3.connect("monketu.db")
    return st.session_state['conn']

# データベース内のテーブルの内容を表示する関数
def show_table_data():
    conn = get_connection()
    c = conn.cursor()

    # テーブルの内容を取得
    c.execute("SELECT * FROM taikai_table")  # your_tableを実際のテーブル名に変更
    data = c.fetchall()

    # Pandas DataFrameに変換して表示
    df = pd.DataFrame(data, columns=[description[0] for description in c.description])
    st.dataframe(df)

    # データベース接続を閉じる
    conn.close()

# メインのStreamlitアプリケーション
def main():
    st.title("Streamlit SQLiteアプリ")

    # データベース内のテーブルの内容を表示する
    show_table_data()

if __name__ == "__main__":
    main()
