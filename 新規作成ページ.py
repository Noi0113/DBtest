import streamlit as st
import hashlib
import sqlite3

# sqliteに接続
def get_connection():
    if 'conn' not in st.session_state:
        st.session_state['conn'] = sqlite3.connect("monketsu.db")
    return st.session_state['conn']

def is_taikaiid_exists(taikaiid):
    # データベースに接続
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM taikai_data WHERE taikaiid = ?;", (taikaiid,))
    count = c.fetchone()

    # データベース接続を閉じる
    conn.close()

    return count[0] > 0 if count else False

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    status_area = st.empty()
    
    # タイトル
    st.title('新規作成') 

    # ここから本作成
    new_taikaiid = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
    new_password = st.text_input("大会パスワードを入力してください", type='password')
    num_match = st.selectbox("大会の試合数を入力してください", range(1, 15), format_func=lambda x: f'{x} 回')
    num_universities = st.number_input("参加大学数を入力してください", min_value=1, step=1)

    universities = []
    for i in range(num_universities):
        university_name = st.text_input(f"参加大学名{i+1}を入力してください")
        universities.append(university_name)

    if st.button('大会作成！', use_container_width=True, help='ページ準備中'):
        if is_taikaiid_exists(new_taikaiid):
            st.error("エラー: このtaikaiidは既に存在します。別のtaikaiidを入力してください。")
        else:
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO taikai_data (taikaiid, password, snum) VALUES (?, ?, ?);", (new_taikaiid, new_password, num_match))
            conn.commit()

    # データベース接続を閉じる
    conn.close()
            st.success(f"新しい大会({new_taikaiid})の作成に成功しました")

if __name__ == '__main__':
    main()
