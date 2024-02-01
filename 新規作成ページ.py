import streamlit as st
import hashlib
import sqlite3

# sqliteに接続
conn = sqlite3.connect('monketsu-option.db')
c = conn.cursor()

def create_user():
    c.execute('CREATE TABLE IF NOT EXISTS userstable (username TEXT PRIMARY KEY, password TEXT)')

def add_user(username, password):
    # ユーザーが既に存在するかを確認
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    existing_user = c.fetchone()
    if existing_user:
        return True
    else:
        c.execute('INSERT INTO userstable (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return False

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# パスワードのハッシュ化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    status_area = st.empty()

    # タイトル
    st.title('新規作成') 
    st.markdown('新規大会IDとパスワードの作成をする')
    st.markdown('ID発行されたらそのIDと「完了しました」的な何か出力させたい。ページも変えられたら〇')

    # ここから本作成
    new_user = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
    new_password = st.text_input("大会パスワードを入力してください",type='password')
    num_player = st.selectbox("大会に参加する人数を入力してください", range(1, 100),format_func=lambda x: f'{x} 人')
    num_match = st.selectbox("大会の総試合回数を入力してください", range(1, 100),format_func=lambda x: f'{x} 回')
            ♯↑「総試合回数」って表現わかりにくいかな…？？いい表現あったら変更しておいてください
    num_universities = st.number_input("参加大学数を入力してください", min_value=1, step=1,format_func=lambda x: f'{x} 校')
    
    universities = []
    for i in range(num_universities):
        university_name = st.text_input(f"参加大学名{i+1}を入力してください")
        universities.append(university_name)

    if st.button('ID発行', use_container_width=True, help='ページ準備中'):
        if add_user(new_user, make_hashes(new_password)):
            st.warning("その大会名は既に使用されています")
        else:
            create_user()
            st.success("新しい大会の作成に成功しました")
            st.info("大会ログイン画面からログインしてください")

if __name__ == '__main__':
    main()
