import streamlit as st
def main():
    status_area = st.empty()
#タイトル
st.title('アンケート回答') 

st.markdown('フォーム')


univ_options = ['あ','い']#こんな感じで、データベースから大学名のリストを取ってくればプルダウン作成は可能です！！！

# フォームを作成します
with st.form(key='my_form'):
    input_taikaiid = st.text_input(label = '大会ID')
    input_name = st.text_input(label='名前')
    input_level = st.selectbox('級',options=['A','B','C','D','E'])
    input_univ = st.selectbox('大学名', options=univ_options)
    #input_feedback = st.text_area(label='フィードバック')
    st.markdown ('個人IDを作成してください。アンケート結果を編集する際に必要となりますので、お手元にお控え下さい。')
    input_kojinid = st.text_input(label = '個人ID')
    if input_taikaiid in not Null:
        submit_button = st.form_submit_button(label='送信',use_container_width = True)

# ユーザーが送信ボタンを押したときに表示されるメッセージ
if submit_button:
    st.write(f"送信が完了しました。ありがとうございます、{input_name}さん！")

##ログインについて
#st.link_button()を導入したい


#######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
