import streamlit as st
import hashlib
import sqlite3

# sqliteに接続
def get_connection():
    if 'conn' not in st.session_state:
        st.session_state['conn'] = sqlite3.connect("monketsu.db")
    return st.session_state['conn']
    
#def create_taikai():
#	c.execute('CREATE TABLE IF NOT EXISTS taikai_table(username TEXT,password TEXT)')

def is_taikaiid_exists(taikaiid):
    # データベースに接続
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM taikai_data WHERE taikaiid = ?;", (taikaiid,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def add_new_data(taikaiid, password):
    conn =  get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO taikai_data (taikaiid, password,num_match) VALUES (?, ?);", (taikaiid, password,num_match))
    conn.commit()
    # データベース接続を閉じる
    conn.close()

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
    new_taikaiid = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
    new_password = st.text_input("大会パスワードを入力してください",type='password')
    num_match = st.selectbox("大会の試合数を入力してください", range(1, 15),format_func=lambda x: f'{x} 回')
    num_universities = st.number_input("参加大学数を入力してください", min_value=1, step=1)
    
    universities = []
    for i in range(num_universities):
        university_name = st.text_input(f"参加大学名{i+1}を入力してください")
        universities.append(university_name)

    if st.button('大会作成！', use_container_width=True, help='ページ準備中'):
        if is_taikaiid_exists(new_taikaiid):
            st.error("エラー: このtaikaiidは既に存在します。別のtaikaiidを入力してください。")
        else:
            add_new_data(new_taikaiid, new_password,num_match)
            st.success(f"新しい大会({new_taikai})の作成に成功しました")
            
        #if add_user(new_taikai, make_hashes(new_password),num_match):
        #    st.warning("その大会名は既に使用されています")
        #else:
        #    create_user()
        #    st.success(f"新しい大会({new_taikai})の作成に成功しました")
        #    st.info("参加者にアンケートのURL（https://monketsu-questionnaire.streamlit.app/）を送ってください。")
        #    st.info("アンケートの回答には大会IDと大会パスワードの入力が必要です")
            

if __name__ == '__main__':
    main()
