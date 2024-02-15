import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# スコープの設定（Google Sheets API および Google Drive API のスコープを追加）
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Google Sheets認証情報の読み込み
credentials = ServiceAccountCredentials.from_json_keyfile_name('monketsu-karuta-a50fe8e854dc.json', scopes)
gc = gspread.authorize(credentials)

##########ここまでスプシ接続設定#######

def main():
    if 'univ_options' not in st.session_state: 
        st.session_state.univ_options = ["-"]
    if 's_number' not in st.session_state: 
        st.session_state.s_number = []
    if 'absent_options' not in st.session_state: 
        st.session_state.absent_options = ["-"]
        
    filtered_univ_num = 0
    filtered_s_num = 0
    univ_options = []
    absent_options = []
    
    new_gene_sheet = gc.open('monketsu-karuta-db').get_worksheet(1)
    new_gene_data = new_gene_sheet.get_all_values()
    headers = new_gene_data.pop(0)
    new_gene_df = pd.DataFrame(new_gene_data, columns=headers)
    
    status_area = st.empty()
    st.title('アンケート回答ページ(コピー)') 

    st.markdown('参加する大会の大会名とパスワードを入力してください')

    input_taikaiid = st.text_input(label='大会名を入力してください')
    input_password = st.text_input(label="大会パスワードを入力してください", type='password')

    id_from_df = new_gene_df.iloc[:, 0]
    pass_from_df = new_gene_df.iloc[:, 1]
    id_list = list(id_from_df)
    pass_list = list(pass_from_df)
    taikai_dict = dict(zip(id_list, pass_list))

    if st.button(label='確定'):
        if input_taikaiid in taikai_dict and taikai_dict[input_taikaiid] == input_password:
            st.success("{}の参加用フォーム".format(input_taikaiid))
            filtered_new_gene_df = new_gene_df[new_gene_df.iloc[:, 0] == input_taikaiid]
            filtered_univ_num = filtered_new_gene_df.iloc[0, 3]
            filtered_s_num = filtered_new_gene_df.iloc[0, 2]

            univ_options = []
            for i in range(int(filtered_univ_num)):
                univ_options.append(filtered_new_gene_df.iloc[0, 4 + i])
                
            absent_options = []
            for i in range(int(filtered_s_num)):
                absent_options.append(f'{i + 1}試合目')

            with st.form(key='my_form'):
                input_name = st.text_input(label='名前を入力してください(必須)')
                input_univ = st.selectbox('学校名または所属会名を入力してください(必須)', options=univ_options)
                input_level = st.selectbox('級を入力してください(必須)', options=['A', 'B', 'C', 'D', 'E'])
                input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか(必ず希望に添えるわけではありません)', options=['はい', 'いいえ'])
                input_wantto = st.text_input(label='対戦したい人を記入してください')
                input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
                absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', options=absent_options)

                submit_button = st.form_submit_button(label='送信', use_container_width=True)

                if submit_button:
                    if input_name and input_univ and input_level:
                        absent_bin_list = []
                        for i in range(len(absent_options)):
                            if absent_options[i] in absent_matches:
                                absent_bin_list.append(1)  # 欠席するなら1を入れる
                            else:
                                absent_bin_list.append(0)  # 出席するなら0を入れる
                
                        sheet = gc.open('monketsu-karuta-db').get_worksheet(0)
                        last_row = len(sheet.col_values(3)) + 1  # 行番号の修正
                        sheet.update_cell(last_row, 1, input_taikaiid)
                        sheet.update_cell(last_row, 2, input_password)
                        sheet.update_cell(last_row, 3, input_name)
                        sheet.update_cell(last_row, 4, input_univ)
                        sheet.update_cell(last_row, 5, input_level)
                        sheet.update_cell(last_row, 6, input_kisuu)
                        sheet.update_cell(last_row, 7, input_wantto)
                        sheet.update_cell(last_row, 8, input_wantnotto)
                        for i in range(len(absent_bin_list)):
                            sheet.update_cell(last_row, 9 + i, absent_bin_list[i])
        
                        st.success(f"送信が完了しました。ありがとうございます、{input_name}さん！")
                    else:
                        st.warning("必須項目を入力してください。")
        else:
            st.warning("大会名か大会パスワードが間違っています")


    ##ログインについて
    # st.link_button()を導入したい


    #######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
