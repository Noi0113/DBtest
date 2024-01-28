import streamlit as st
#py get-pip.py
#!pip install firebase-admin
import time
def main():
    status_area = st.empty()

    st.title('DBテストサイト')
    st.markdown('firebase adminをインストールできた')


    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db

    #cred = credentials.Certificate("path/to/serviceAccountKey.json")
    #firebase_admin.initialize_app(cred, {
    #    'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com'
    #})

    #ref = db.reference('restricted_access/secret_document')
    #print(ref.get())

    count_down_sec = 5
    for i in range(count_down_sec):
        # プレースホルダーに残り秒数を書き込む
        status_area.write(f'{count_down_sec - i} sec left')
        # スリープ処理を入れる
        time.sleep(1)

    # 完了したときの表示
    status_area.write('Done!')
    # 風船飛ばす
    st.balloons()
if __name__ == '__main__':
    main()
