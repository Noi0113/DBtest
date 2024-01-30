import streamlit as st
def main():
    status_area = st.empty()

    st.title('DBテストサイト')
    st.markdown('requirements.txtをアップロードした。各モジュールは使えるか？')
    import pyrebase4
    import pandas as pd
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
    #cred = credentials.Certificate("path/to/serviceAccountKey.json")
    #firebase_admin.initialize_app(cred, {
    #    'databaseURL': 'https://console.firebase.google.com/u/0/project/monketsu-choicedb/database/monketsu-choicedb-default-rtdb/data?hl=ja'
    #})

    #ref = db.reference('restricted_access/secret_document')
    #print(ref.get())

if __name__ == '__main__':
    main()
