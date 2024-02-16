import streamlit as st
import pandas as pd
import sqlite3
import hashlib

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# スコープの設定（Google Sheets API および Google Drive API のスコープを追加）
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Google Sheets認証情報の読み込み
credentials = ServiceAccountCredentials.from_json_keyfile_name('monketsu-karuta-a50fe8e854dc.json', scopes)
gc = gspread.authorize(credentials)

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
    # まずGoogle Sheetsのシート2を開き、それをデータフレーム化する
    new_gene_sheet = gc.open('monketsu-karuta-db').get_worksheet(1)
    new_gene_data = new_gene_sheet.get_all_values()
    headers = new_gene_data.pop(0)
    new_gene_df = pd.DataFrame(new_gene_data, columns = headers)

        # 新規作成ページで作成された大会IDとパスワードを辞書化
    id_from_df = new_gene_df.iloc[:,0]
    pass_from_df = new_gene_df.iloc[:,1]
    id_list = list(id_from_df)
    pass_list = list(pass_from_df)
    taikai_dict = dict(zip(id_list,pass_list))

    if 'univ_options' not in st.session_state: 
        st.session_state.univ_options = ["-"]
    if 's_number' not in st.session_state: 
        st.session_state.s_number = []
    if 'absent_options' not in st.session_state: 
        st.session_state.absent_options = ["-"]
    
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
    
    if st.button(label='確定'):
      if input_taikaiid in taikai_dict and taikai_dict[input_taikaiid] == input_password:
        
        #hashed_pswd = make_hashes(input_password)
        #result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
        #if result:
        st.success("{}の参加用フォーム".format(input_taikaiid))

        #大会名が入力内容と一致した行を抜き出す必要な情報を取り出す
        filtered_new_gene_df = new_gene_df[new_gene_df.iloc[:,0] == input_taikaiid]
        #以下は指定された大会の参加大学数、試合数
        filtered_univ_num = filtered_new_gene_df.iloc[0,3]
        filtered_s_num = filtered_new_gene_df.iloc[0,2]

        # 大学の選択肢を作成
        st.session_state.univ_options = []
        for i in range(int(filtered_univ_num)):
            st.session_state.univ_options.append(filtered_new_gene_df.iloc[0,4+i])
            
        # 欠席試合を入力するために、ここで試合のリストを作る
        st.session_state.absent_options = []
        for i in range(int(filtered_s_num)):
            st.session_state.absent_options.append(f'{i+1}試合目')
        st.write(st.session_state.univ_options)
        st.write(st.session_state.absent_options)
        
      else:
        st.warning("大会名か大会パスワードが間違っています")

            # フォームを作成します
    with st.form(key='my_form'):
            input_name = st.text_input(label='名前を入力してください(必須)')
            input_univ = st.selectbox('学校名または所属会名を入力してください(必須)', options=st.session_state.univ_options)
            input_level = st.selectbox('級を入力してください(必須)',options=['A','B','C','D','E'])
            input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか(必ず希望に添えるわけではありません)',options=['はい','いいえ'])
            input_wantto = st.text_input(label='対戦したい人を記入してください')
            input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
            absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', st.session_state.absent_options)
    
            submit_button = st.form_submit_button(label='送信',use_container_width = True)
        
                # ユーザーが送信ボタンを押したときに表示されるメッセージ
            if submit_button:
                if input_name and input_univ and input_level:
                    absent_01 = []
                    for i in st.session_state.absent_options:
                        if i in absent_matches:
                            absent_01.append(0)
                        else:
                            absent_01.append(1)
                    while len(absent_01) < 16:
                        absent_01.append(0)
                    conn = sqlite3.connect('monketsu.db')
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
      #else:
       # st.warning("大会名か大会パスワードが間違っています")



    ##ログインについて
    #st.link_button()を導入したい
    #######トップページ終わり
#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")
if __name__ == '__main__':
    main()
