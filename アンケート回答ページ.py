import streamlit as st
import pandas as pd
import sqlite3
import hashlib

#def get_connection():
#    if 'conn' not in st.session_state:
#        st.session_state['conn'] = sqlite3.connect('monketsu.db')
#    return st.session_state['conn']

#target_id列の値がtarget_idである行のcolumn_name列の値をリストで出す
def data_retu(table_name, target_name,target_id, column_name):
    conn = sqlite3.connect('monka.db')
    c = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name} WHERE {target_name} = ?;"
    c.execute(query, (target_id,))
    result = c.fetchall()
    conn.close()
    result_list = [item[0] for item in result]
    return result_list

#loginする
def login_user(username,password):
    c = sqlite3.connect('monka.db')
    cursor = c.cursor()
    cursor.execute('SELECT * FROM taikai_data WHERE taikaiid = ? AND password = ?', (username, password))
    data = cursor.fetchall()
    return data
#hash化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

univ_options = ['-']
s_number = ['-']
absent_options = ['-']


def main():
    status_area = st.empty()
    #タイトル
    st.title('アンケート回答') 

 

            # フォームを作成します
    with st.form(key='my_form'):
        input_name = st.text_input(label='名前を入力してください(必須)')
        #input_univ = st.selectbox('学校名または所属会名を入力してください(必須)', options=univ_options)
        input_level = st.selectbox('級を入力してください(必須)',options=['A','B','C','D','E'])
        input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか(必ず希望に添えるわけではありません)',options=['はい','いいえ'])
        input_wantto = st.text_input(label='対戦したい人を記入してください')
        input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
        #absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', absent_options)
    
        submit_button = st.form_submit_button(label='送信',use_container_width = True)
        
                # ユーザーが送信ボタンを押したときに表示されるメッセージ
        if submit_button:
            st.success("aaa")

    ##ログインについて
    #st.link_button()を導入したい


    #######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
