import streamlit as st
def main():
    status_area = st.empty()

    st.title('DBテストサイト')

    #py get-pip.py
    #!pip install firebase-admin
    import pandas as pd
    import firebase_admin as fa
    #from firebase_admin import credentials
    #from firebase_admin import db
    #cred = credentials.Certificate("path/to/serviceAccountKey.json")
    #firebase_admin.initialize_app(cred, {
    #    'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com'
    #})

    #ref = db.reference('restricted_access/secret_document')
    #print(ref.get())

if __name__ == '__main__':
    main()
