import streamlit as st
import hashlib
import sqlite3

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
  st.title('ログイン機能(アンケ前)')
  st.markdown('参加する大会の大会名とパスワードを入力してください')

  input_taikaiid = st.text_input(label = '大会名を入力してください')
  input_password = st.text_input(label = "大会パスワードを入力してください",type='password')

  if st.button(label='確定'):
      #hash化されたpasswordをdbに書き込めるようになったらこれ
      #hashed_pswd = make_hashes(input_password)
      #result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
      
      result = login_user(input_taikaiid,input_password)
      
      if result:
        st.write("ログインしました")
        st.success("{}の参加用フォーム".format(input_taikaiid))

        
#st.link_button('アンケート回答',"https://monketsu-questionnaire.streamlit.app/",use_container_width=True)
if __name__ == '__main__':
    main()
