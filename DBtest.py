import streamlit as st
def main():
  status_area = st.empty()
  a=3
  st.title('DBテストサイト!')
  st.markdown('requirements.txtをアップロードし編集した。誤字チェック済み')

  for i in range(3):
      st.write('インデント？')
  
   

if __name__ == '__main__':
    main()
