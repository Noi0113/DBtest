import streamlit as st
import pandas as pd
def main():
    status_area = st.empty()
#タイトル
st.title('アンケート回答') 

st.markdown('フォーム')


#選択肢はフォームの外に作らないとエラーが出るかも
univ_options = ['あ','い']#こんな感じで、データベースから大学名のリストを取ってくればプルダウン作成は可能です！！！
absent_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']#このリストをmonketsu-option.dbから取得するとよい

# フォームを作成します
with st.form(key='my_form'):
    input_taikaiid = st.text_input(label = '大会IDを入力してください')
    #大会IDはフォーム外のほうがいいかもしれない…？大会IDからuniv_optionsを作成するならその処理はフォーム外になるかも？
    input_name = st.text_input(label='名前を入力してください')
    input_univ = st.selectbox('学校名または所属会名を入力してください', options=univ_options)
    input_level = st.selectbox('級を入力してください',options=['A','B','C','D','E'])
    input_kisuu = st.selectbox('奇数の場合一人取りまたは読手を希望しますか',options=['はい','いいえ'])
    input_wantto = st.text_input(label='対戦したい人を記入してください')
    input_wantnotto = st.text_input(label='対戦したくない人を記入してください')
    absent_matches = st.multiselect('欠席する試合(複数選択可)を入力してください', absent_options)
  
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
    st.write(absent_01)
    
    #c.execute('''
    #INSERT INTO user_data (input_name,input_school,input_level,input_kisuu,input_wantto,input_wantnotto,) VALUES (?, ?,　?,　?,　?,　?,　?)
    #''', (name,school,clas,kisuu,wantto,wantnotto,))
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
