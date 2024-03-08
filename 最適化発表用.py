import streamlit as st
import time
import pandas as pd
def main():
    #status_area = st.empty()
    #ここから上は編集しない

    #タイトル
    st.title('対戦表の作成')
    #install coin-or-cbc

    st.markdown('対戦表を作成したい大会の大会名・大会パスワードを入力してください')
    input_taikaiid = st.text_input(label = '大会名')
    input_password = st.text_input(label = 'パスワード',type = 'password')
    if st.button('対戦表の作成',use_container_width=True):
        st.success("対戦表を作成します")
        with st.spinner("対戦表を作成中..."):
            time.sleep(10)
        
        # CSVファイルを読み込む
        try:
            df = pd.read_csv(csv_file_path)
            st.dataframe(df)
        except FileNotFoundError:
            st.error("CSVファイルが見つかりませんでした。")

 #   hashed_pswd = make_hashes(input_password)
 #   result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
 #   if result:
