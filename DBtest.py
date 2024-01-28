#py get-pip.py
#!pip install firebase-admin

#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
import streamlit as st
def main():
    status_area = st.empty()

    st.title('DBテストサイト')
    #st.markdown('firebase adminをインストールできた')
    #cred = credentials.Certificate("path/to/serviceAccountKey.json")
    #firebase_admin.initialize_app(cred, {
    #    'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com'
    #})

    #ref = db.reference('restricted_access/secret_document')
    #print(ref.get())

if __name__ == '__main__':
    main()
