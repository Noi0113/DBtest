import streamlit as st
import pandas as pd
import sqlite3

# target_id列の値がtarget_idである行のcolumn_name列の値をリストで出す
def data_retu(table_name, target_name, target_id, column_name):
    conn = sqlite3.connect('monka.db')
    c = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name} WHERE {target_name} = ?;"
    c.execute(query, (target_id,))
    result = c.fetchall()
    conn.close()
    result_list = [item[0] for item in result]
    return result_list

def main():
    status_area = st.empty()
    # タイトル
    st.title('アンケート回答')

    st.markdown('参加者の個人アンケートに回答するため、大会IDとパスワードを入力してください')

    # 選択肢はフォームの外に作らないとエラーが出るかも
    input_taikaiid = st.text_input(label='大会名を入力してください')
    input_password = st.text_input(label="大会パスワードを入力してください", type='password')

    if st.button(label='確定'):
        result = login_user(input_taikaiid, input_password)

        if result:
            st.success("{}の参加用フォーム".format(username))

            univ_options = data_retu('monka.db', 'univ_data', 'taikaiid', input_taikaiid, 'univ')
            s_number = data_retu('monka.db', 'taikai_data', 'taikaiid', input_taikaiid, 'snum')
            absent_options = []
            for i in range(int(s_number[0])):
                absent_options.append(f'{i+1}試合目')

            # フォームを作成します
            with st.form(key='my_form'):
                input_name = st.text_input(label='名前を入力してください(必須)')
                input_univ = st.selectbox('学校名または所属会名を入力してください(必須)', options=univ_options)
                input_level = st.selectbox('級を入力してください(必須)', options=['A', 'B', 'C', 'D', 'E'])
                input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか(必ず希望に添えるわけではありません)',
                                           options=['はい', 'いいえ'])
                input_wantto = st.text_input(label='対戦したい人を記入してください')
                input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
                absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', absent_options)

                # if input_name and input_level and input_univ is not None:

                submit_button = st.form_submit_button(label='送信', use_container_width=True)

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

                        conn = sqlite3.connect('monka.db')
                        c = conn.cursor()
                        c.execute('''
                            INSERT INTO user_data (name, school, level, kisuu, wantto, wantnotto, s1, s2, s3, s4, s5, s6, s7, s
