import streamlit as st
import pandas as pd
import sqlite3

def main():
    status_area = st.empty()
#タイトル
st.title('アンケート回答') 

st.markdown('フォーム')

#target_id列の値がtarget_idである行のcolumn_name列の値をリストで出す
def data_retu(database_path, table_name, target_name,target_id, column_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name} WHERE {target_name} = ?;"
    cursor.execute(query, (target_id,))
    result = cursor.fetchall()
    conn.close()
    result_list = [item[0] for item in result]
    return result_list

#loginする
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

#選択肢はフォームの外に作らないとエラーが出るかも
input_taikaiid = st.text_input(label = '大会IDを入力してください')
input_password = st.sidebar.text_input("大会パスワードを入力してください",type='password')

hashed_pswd = make_hashes(input_password)
result = login_user(username,check_hashes(input_password,hashed_pswd))
if st.sidebar.checkbox("ログイン"):
    if result:
        st.success("{}の参加用フォーム".format(username))
    else:
		st.warning("大会IDか大会パスワードが間違っています")

if st.button(label='確定'):
    univ_options = data_retu('monketsu.db', 'univ_data', 'taikaiid',input_taikaiid, 'univ'):#こんな感じで、データベースから大学名のリストを取ってくればプルダウン作成は可能です！！！
    s_number = data_retu('monketsu.db', 'taikai_data', 'taikaiid',input_taikaiid, 'snum')
    absent_options = []
    for i in range(int(s_number[0])):
        absent_options.append(f'{i+1}試合目')

    #univ_options = ['あ','い']
    #absent_options = ['1','2','3']

    # フォームを作成します
    with st.form(key='my_form'):
        input_name = st.text_input(label='名前を入力してください')
        input_univ = st.selectbox('学校名または所属会名を入力してください', options=univ_options)
        input_level = st.selectbox('級を入力してください',options=['A','B','C','D','E'])
        input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか',options=['はい','いいえ'])
        input_wantto = st.text_input(label='対戦したい人を記入してください')
        input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
        absent_matches = st.multiselect('欠席する試合を入力してください(複数選択可)', absent_options)
  
        #st.markdown ('個人IDを作成してください。アンケート結果を編集する際に必要となりますので、お手元にお控え下さい。')
        #input_kojinid = st.text_input(label = '個人IDを作成してください。アンケート結果を編集する際に必要となりますので、お手元にお控え下さい。')
        #すべての欄を埋めたら送信できるようにもしたい
        #if input_name and input_level and input_univ is not None:
    
        submit_button = st.form_submit_button(label='送信',use_container_width = True)

    # ユーザーが送信ボタンを押したときに表示されるメッセージ
    if submit_button:
        absent_01 = []
        for i in absent_options:
            if i in absent_matches:
                absent_01.append(0)
            else:
                absent_01.append(1)
        while len(absent_01) < 15:
            absent_01.append(0)
    
        #c.execute('''
        #INSERT INTO user_data (name,school,level,kisuu,wantto,wantnotto,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15) VALUES ((?,?,?,?,?,?,?,?,?,?,?,?,,?,?,?,?,?,?,?,?)
        #''', (input_name,input_school,input_level,input_kisuu,input_wantto,input_wantnotto,absent_01[0],absent_01[1],absent_01[2],absent_01[3],absent_01[4],absent_01[5],absent_01[6],absent_01[7],absent_01[8],absent_01[9],absent_01[10],absent_01[11],absent_01[12],absent_01[13],absent_01[14]))
        #    conn.commit()
        #st.success(f"送信が完了しました。ありがとうございます、{input_name}さん！")
        #st.write(f"送信が完了しました。ありがとうございます、{input_name}さん！")

    ##ログインについて
    #st.link_button()を導入したい


    #######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
