import streamlit as st
import hashlib
import sqlite3


# sqliteに接続
conn = sqlite3.connect('monketsu.db')
c = conn.cursor()

    
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    status_area = st.empty()

    # sqliteに接続
    conn = sqlite3.connect('monketsu.db')
    c = conn.cursor()

    
    # タイトル
    st.title('新規作成') 
    with st.form(key='my_form2'):
        # ここから本作成
        new_taikaiid = st.text_input("大会名を入力してください")
        new_password = st.text_input("大会パスワードを入力してください", type='password')
        num_match = st.selectbox("大会の試合数を入力してください", range(1, 15), format_func=lambda x: f'{x} 回')
        num_universities = st.number_input("参加学校・かるた会数を入力してください", min_value=1, step=1)

        universities = []
        for i in range(num_universities):
            university_name = st.text_input(f"参加学校・かるた会名{i+1}を入力してください")
            universities.append(university_name)

        submit_button = st.form_submit_button(label='送信',use_container_width = True)

        if submit_button:
            if new_taikaiid and new_password and num_match and num_universities and universities.count("")==0:
                c.execute(f"SELECT COUNT(*) FROM taikai_data WHERE taikaiid = ?;", (new_taikaiid,))
                count = c.fetchone()
                a = count[0] > 0 if count else False
                if a:
                    st.error("エラー: この大会名は既に使用されています。別の大会名を入力してください。")
                else:
                    c.execute("INSERT INTO taikai_data (taikaiid, password, snum) VALUES (?, ?, ?);", (new_taikaiid, new_password, num_match))
                    for u in universities:
                        c.execute("INSERT INTO univ_data (taikaiid, univ) VALUES (?, ?);", (new_taikaiid, u))
                    conn.commit()
                    st.success(f"新しい大会({new_taikaiid})の作成に成功しました")
                    import os

                    # データベースファイルのパス
                    db_path = "monketsu.db"
                    py_path = "新規作成ページ.py"
                    # パスを表示
                    st.write(f"データベースへのパス: {os.path.abspath(py_path)}")
                    st.write(f"データベースへのパス: {os.path.abspath(db_path)}")
            else:
                # 全ての欄が埋まっていない場合の処理
                st.warning("全ての項目を入力してください。")
            
    conn.close()
if __name__ == '__main__':
    main()


