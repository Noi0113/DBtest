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
    
    filtered_univ_num = 0
    filtered_s_num = 0
    if 'univ_options' not in st.session_state: 
        st.session_state.univ_options = ["-"]
    if 'absent_options' not in st.session_state: 
        st.session_state.absent_options = ["-"]
    
    status_area = st.empty()
    #タイトル
    st.title('アンケート回答') 
    st.markdown('参加する大会の大会名とパスワードを入力してください')
    input_taikaiid = st.text_input(label = '大会名を入力してください')
    input_password = st.text_input(label = "大会パスワードを入力してください",type='password')
    #hash化されたpasswordをdbに書き込めるようになったらこれ
    hashed_pswd = make_hashes(input_password)
    checked_password = check_hashes(input_password,hashed_pswd)
    
    if st.button(label='確定'):
      if input_taikaiid in taikai_dict and taikai_dict[input_taikaiid] == checked_password:
        
        st.success("{}の参加用フォーム".format(input_taikaiid))
        user_sheet = gc.open('monketsu-karuta-db').get_worksheet(0)
        user_data = user_sheet.get_all_values()
        user_headers = user_data.pop(0)
        user_df = pd.DataFrame(user_data, columns = user_headers)
        filtered_user_df = user_df[user_df.iloc[:,0] == input_taikaiid]
        #大会名が入力内容と一致した行を抜き出す必要な情報を取り出す
        filtered_new_gene_df = new_gene_df[new_gene_df.iloc[:,0] == input_taikaiid]
        #以下は指定された大会の参加大学数、試合数
        filtered_univ_num = filtered_new_gene_df.iloc[0,3]
        filtered_s_num = filtered_new_gene_df.iloc[0,2]
        st.session_state.name_list = filtered_user_df['名前'].tolist()
        st.write(st.session_state.name_list)

        # 大学の選択肢を作成
        st.session_state.univ_options = []
        for i in range(int(filtered_univ_num)):
            st.session_state.univ_options.append(filtered_new_gene_df.iloc[0,4+i])
            
        # 欠席試合を入力するために、ここで試合のリストを作る
        st.session_state.absent_options = []
        for i in range(int(filtered_s_num)):
            st.session_state.absent_options.append(f'{i+1}試合目')
        
      else:
        st.warning("大会名か大会パスワードが間違っています")
    else:
        st.warning('正しい大会名と大会パスワードを入力し、確定を押してください')
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
        
                # ユーザーが送信ボタンを押したとき
            if submit_button:
                if input_name and input_univ and input_level:
                    matching_rows = user_sheet.findall(input_name, in_column="名前")
                    if matching_rows:
                        try:

                            absent_bin_list = [1 if option in absent_matches else 0 for option in st.session_state.absent_options]
                            user_sheet.update_row([input_taikaiid, input_password, input_name, input_univ, input_level, input_kisuu, input_wantto, input_wantnotto] + absent_bin_list)
                            
                            st.success(f"送信が完了しました。ありがとうございます、{input_name}さん！")
                        except Exception as e:
                            st.error("データの送信中にエラーが発生しました。もう一度試してね。")
                    else:
                        try:
                            
                            last_row = len(user_sheet.col_values(3)) + 1
                            absent_bin_list = [1 if option in absent_matches else 0 for option in st.session_state.absent_options]
                            user_sheet.append_row([input_taikaiid, input_password, input_name, input_univ, input_level, input_kisuu, input_wantto, input_wantnotto] + absent_bin_list)
                            
                            st.success(f"送信が完了しました。ありがとうございます、{input_name}さん！")
                        except Exception as e:
                            st.error("データの送信中にエラーが発生しました。もう一度試してください。")
                else:
                    st.warning("必須項目を入力してください。")
if __name__ == '__main__':
    main()
