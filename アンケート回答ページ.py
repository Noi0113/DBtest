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
    
def main():
    status_area = st.empty()
    #タイトル
    st.title('アンケート回答') 

    st.markdown('参加する大会の大会名とパスワードを入力してください')

    input_taikaiid = st.text_input(label = '大会名を入力してください')
    input_password = st.text_input(label = "大会パスワードを入力してください",type='password')

    result = login_user(input_taikaiid,input_password)
    #hash化されたpasswordをdbに書き込めるようになったらこれ
    #hashed_pswd = make_hashes(input_password)
    #result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
    
    if st.button(label='確定') and result:
        #hashed_pswd = make_hashes(input_password)
        #result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
        #if result:
        st.success("{}の参加用フォーム".format(input_taikaiid))

        univ_options = data_retu("univ_data","taikaiid",input_taikaiid,"univ")
        st.write(univ_options)
        s_number = data_retu("taikai_data","taikaiid",input_taikaiid,"snum")
        st.write(s_number)
        absent_options = []
        for i in range(int(s_number[0])):
            absent_options.append(f'{i+1}試合目')

            #univ_options = ['あ','い']
            #absent_options = ['1','2','3']

            # フォームを作成します
        with st.form(key='my_form'):
            input_name = st.text_input(label='名前を入力してください(必須)')
            input_univ = st.selectbox('学校名または所属会名を入力してください(必須)', options=univ_options)
            input_level = st.selectbox('級を入力してください(必須)',options=['A','B','C','D','E'])
            input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか(必ず希望に添えるわけではありません)',options=['はい','いいえ'])
            input_wantto = st.text_input(label='対戦したい人を記入してください')
            input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
            absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', absent_options)
    
            submit_button = st.form_submit_button(label='送信',use_container_width = True)

                # ユーザーが送信ボタンを押したときに表示されるメッセージ
            if submit_button:
                if input_name and input_univ and input_level:
                    absent_01 = []
                    for i in absent_options:
                        if i in absent_matches:
                            absent_01.append(0)
                        else:
                            absent_01.append(1)
                    while len(absent_01) < 16:
                        absent_01.append(0)

                    conn = conn.sqlite3.connect('monketsu.db')
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO user_data (name, school, level, kisuu, wantto, wantnotto, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, taikaiid)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        ''', (input_name, input_univ, input_level, input_kisuu, input_wantto, input_wantnotto,absent_01[0], absent_01[1], absent_01[2], absent_01[3], absent_01[4], absent_01[5],absent_01[6], absent_01[7], absent_01[8], absent_01[9], absent_01[10], absent_01[11],absent_01[12], absent_01[13], absent_01[14], input_taikaiid))

                    conn.commit()
                    conn.close()
                    st.success(f"送信が完了しました。ありがとうございます、{input_name}さん！")
                # 全ての欄が埋まっていない場合の処理
                else:
                    st.warning("必須項目を入力してください。")
    elif st.button(label='確定'):
        st.warning("大会IDか大会パスワードが間違っています")


    ##ログインについて
    #st.link_button()を導入したい


    #######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
