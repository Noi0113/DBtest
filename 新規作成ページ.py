def main():
    status_area = st.empty()
#タイトル
st.title('新規作成') 

st.markdown('大会名・大学名など入力する欄がこの辺に来る')

#ボタン
st.button('ID発行',use_container_width=True,help='ページ準備中')
st.markdown('ID発行されたらそのIDと「完了しました」的な何か出力させたい。ページも変えられたら〇')


##ログインについて
#st.link_button()を導入したい


#######トップページ終わり

#######新規作成クリック後のページ
def new():
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

if __name__ == '__main__':
    main()
