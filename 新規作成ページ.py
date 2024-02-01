import streamlit as st
import hashlib
import sqlite3

# sqliteに接続
def get_connection():
    if 'conn' not in st.session_state:
        st.session_state['conn'] = sqlite3.connect("monketsu.db")
    return st.session_state['conn']
    
def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_user(username, password):
    # 大会IDが既に存在するかを確認
    conn = get_connection() #ここでコネクション確立？？name errorが出てしまう
    c.execute('SELECT * FROM taikai_data WHERE taikaiid = ?', (username,))
    existing_user = c.fetchone()
    if existing_user:
        return True
    else:
        c.execute('INSERT INTO taikai_data (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return False

# パスワードのハッシュ化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    status_area = st.empty()
    
    # タイトル
    st.title('新規作成') 
    #st.markdown('新規大会IDとパスワードの作成をする')
    #st.markdown('ID発行されたらそのIDと「完了しました」的な何か出力させたい。ページも変えられたら〇')

    # ここから本作成
    new_taikai = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
    new_password = st.text_input("大会パスワードを入力してください",type='password')
    num_match = st.selectbox("大会の試合数を入力してください", range(1, 15),format_func=lambda x: f'{x} 回')
    num_universities = st.number_input("参加大学数を入力してください", min_value=1, step=1)
    
    universities = []
    for i in range(num_universities):
        university_name = st.text_input(f"参加大学名{i+1}を入力してください")
        universities.append(university_name)

    if st.button('ID発行', use_container_width=True, help='ページ準備中'):
        if add_user(new_user, make_hashes(new_password)):
            st.warning("その大会名は既に使用されています")
        else:
            create_user()
            st.success(f"新しい大会({new_taikai})の作成に成功しました")
            st.info("参加者にアンケートのURL（https://monketsu-questionnaire.streamlit.app/）を送ってください。")
            st.info("アンケートの回答には大会IDと大会パスワードの入力が必要です")
            

if __name__ == '__main__':
    main()
