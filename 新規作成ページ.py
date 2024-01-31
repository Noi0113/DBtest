import streamlit as st

def main():
    status_area = st.empty()
#タイトル
st.title('新規作成') 

st.markdown('大会名・大学名など入力する欄がこの辺に来る')

#ボタン
#st.button('ID発行',use_container_width=True,help='ページ準備中')
#st.markdown('ID発行されたらそのIDと「完了しました」的な何か出力させたい。ページも変えられたら〇')

# ページの選択と表示
menu = ["大会ログイン", "新規大会登録" ]
choice = st.selectbox("選択してください",menu)
st.write("{}ページです".format(choice))

if choice == "大会ログイン":
	username = st.text_input("大会名を入力")
	password = st.text_input("大会パスワードを入力してください",type='password')
	if st.button('ログイン'):
		hashed_pswd = make_hashes(password)
		result = login_user(username,check_hashes(password,hashed_pswd))
		if result:
			st.success("大会名：{}でログインしました".format(username))
		else:
			st.warning("大会名か大会パスワードが間違っています")

elif choice == "新規大会登録":
	new_user = st.text_input("大会名を入力してください（被りがあると注意されて新規作成できない予定）")
	new_password = st.text_input("大会パスワードを入力してください",type='password')
	if st.button("登録"):
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
