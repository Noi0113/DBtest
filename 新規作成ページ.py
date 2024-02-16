import streamlit as st
import hashlib
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


##########ここからスプシ接続設定#######
# スコープの設定（Google Sheets API および Google Drive API のスコープを追加）
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Google Sheets認証情報の読み込み
credentials = ServiceAccountCredentials.from_json_keyfile_name('monketsu-karuta-a50fe8e854dc.json', scopes)
gc = gspread.authorize(credentials)
##########ここまでスプシ接続設定#######
    
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    status_area = st.empty()

    # タイトル
    st.title('新規作成ページ') 
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
                hashed_pswd = make_hashes(new_password)
                
                #c.execute(f"SELECT COUNT(*) FROM taikai_data WHERE taikaiid = ?;", (new_taikaiid,))
                #count = c.fetchone()
                #a = count[0] > 0 if count else False
                #if a:

                # まずGoogle Sheetsのシート2を開き、それをデータフレーム化する
                new_gene_sheet = gc.open('monketsu-karuta-db').get_worksheet(1)
                new_gene_data = new_gene_sheet.get_all_values()
                headers = new_gene_data.pop(0)
                new_gene_df = pd.DataFrame(new_gene_data, columns = headers)
                
                # 以前使用された大会名がないか、検索して確かめる
                col1 = new_gene_df.iloc[:, 0]
                taikaiid_list =list(col1)
                if new_taikaiid in taikaiid_list:                
                    st.error("エラー: この大会名は既に使用されています。別の大会名を入力してください。")
                    
                else: 
                    last_row = len(new_gene_sheet.col_values(1)) + 1
                    new_gene_sheet.update_cell(last_row, 1, new_taikaiid)
                    new_gene_sheet.update_cell(last_row, 2, hashed_pswd)
                    new_gene_sheet.update_cell(last_row, 3, num_match)
                    new_gene_sheet.update_cell(last_row, 4, num_universities)
                    for i in range(num_universities): # 出席・欠席を0,1で格納(試合数の違いにも対応)
                        new_gene_sheet.update_cell(last_row, 5+i, universities[i])
                    #c.execute("INSERT INTO taikai_data (taikaiid, password, snum) VALUES (?, ?, ?);", (new_taikaiid, new_password, num_match))
                    #for u in universities:
                    #    c.execute("INSERT INTO univ_data (taikaiid, univ) VALUES (?, ?);", (new_taikaiid, u))
                    #conn.commit()
                    st.success(f"新しい大会({new_taikaiid})の作成に成功しました")
                    st.subheader("以下の情報を大会参加者に共有してください。")
                    st.write(f"大会名：{new_taikaiid}")
                    st.write(f"大会パスワード：{new_password}")
                    st.write("大会参加者アンケートURL：https://monketsu-questionnaire.streamlit.app/")

            
                    
            else:
                # 全ての欄が埋まっていない場合の処理
                st.warning("全ての項目を入力してください。")
            
    # conn.close()
if __name__ == '__main__':
    main()


