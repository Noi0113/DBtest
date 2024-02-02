import streamlit as st
import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('test_monketsu3.db')
c = conn.cursor()

# テーブルが存在しない場合は作成
c.execute('''CREATE TABLE IF NOT EXISTS user_inputs (
                id INTEGER PRIMARY KEY,
                input TEXT
             )''')

# Streamlitアプリケーション
st.title('データベース更新テスト')

# ユーザーからの入力を受け取り、データベースに追加
user_input = st.text_input("何か入力してください")
if st.button("送信"):
    c.execute("INSERT INTO user_inputs (input) VALUES (?)", (user_input,))
    conn.commit()
    st.success("データがデータベースに追加されました！")

# データベース内のデータを表示
st.subheader("データベース内のデータ:")
result = c.execute("SELECT * FROM user_inputs")
for row in result:
    st.write(row)

# データベースとの接続を閉じる
conn.close()
