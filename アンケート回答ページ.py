import streamlit as st
def main():
    status_area = st.empty()
#タイトル
st.title('アンケート回答') 

st.markdown('大会ID、氏名、大学名など入力する欄がこの辺に来る')

#ボタン
st.markdown('回答が送信されたら「完了しました」的な何か出力させたい。ページも変えられたら〇')

st.markdown('フォーム')
optionsA = ['あ','い']
# フォームを作成します
with st.form(key='my_form'):
    input_name = st.text_input(label='名前')
    input_level = st.selectbox('級',options=['A','B','C','D','E'])
    input_univ = st.selectbox('大学名', options=optionsA)
    #input_feedback = st.text_area(label='フィードバック')
    submit_button = st.form_submit_button(label='送信')

# ユーザーが送信ボタンを押したときに表示されるメッセージ
if submit_button:
    st.write(f"ありがとうございます、{input_name}さん！")

##ログインについて
#st.link_button()を導入したい


#######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
