import streamlit as st
import hashlib
import sqlite3

def main():
	status_area = st.empty()
#タイトル
st.title('新規作成') 
st.markdown('新規大会IDとパスワードの作成をする')
#st.markdown('大会名・大学名など入力する欄がこの辺に来る')
st.markdown('ID発行されたらそのIDと「完了しました」的な何か出力させたい。ページも変えられたら〇')




	
#sqliteに接続
conn = sqlite3.connect('user_database.db') 
#ここのデータベース名を「monketsu-option.db」に変更？
c=conn.cursor()

def create_user():
    c.execute('CREATE TABLE IF NOT EXISTS userstable (username TEXT PRIMARY KEY, password TEXT)')

def add_user(username, password):
    # ユーザーが既に存在するかを確認
    c.execute('SELECT * FROM userstable WHERE username = ?', (username))
    existing_user = c.fetchone()
    if existing_user:
        return True
    else:
	    c.execute('INSERT INTO userstable (username, password) VALUES (?, ?)', (username, password))
	    conn.commit()
	    return False

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

#パスワードのハッシュ化
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False




#ここから本作成
new_user = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
new_password = st.text_input("大会パスワードを入力してください",type='password')
#new_check = st.markdown('大会名とパスワードを記録しておいてください')

if st.button('ID発行',use_container_width=True,help='ページ準備中'):
	if add_user(new_user,make_hashes(new_password)):
		st.warning("その大会名は既にしようされています")
	else:
		create_user()
		st.success("新しい大会の作成に成功しました")
		st.info("大会ログイン画面からログインしてください")

##ログインについて
#st.link_button()を導入したい


#######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
