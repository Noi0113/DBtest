import streamlit as st
import hashlib
import sqlite3

st.title('ログインページ!(アンケ前)')
#loginする
def login_user(id,pas):
    conn = sqlite3.connect('monka.db')
    c = conn.cursor()
    c.execute('SELECT * FROM taikai_data WHERE taikaiid =? AND password = ?',(id,pas))
    data = c.fetchall()
    conn.close()
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
  st.title('ログイン機能(アンケ前)')
  #st.markdown('この辺にログイン機能(適当にアンケート回答ページに飛べるボタンを設置しておきました)')
  st.markdown('参加する大会の大会名とパスワードを入力してください')

  input_taikaiid = st.text_input(label = '大会名を入力してください')
  input_password = st.text_input(label = "大会パスワードを入力してください",type='password')

  if st.button(label='確定'):
      hashed_pswd = make_hashes(input_password)
      result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
      if result:
        st.success("{}の参加用フォーム".format(input_taikaiid))

        
#st.link_button('アンケート回答',"https://monketsu-questionnaire.streamlit.app/",use_container_width=True)
if __name__ == '__main__':
    main()
