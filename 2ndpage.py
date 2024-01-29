import streamlit as st
def main():
    status_area = st.empty()
 #ここから上は編集しない

#タイトル
st.title('新規作成ページ遷移成功')

#install coin-or-cbc
#pip install pulp
#pip install pulp

import subprocess
# subprocessモジュールを使用してpipを呼び出し、モジュールをインストールする
subprocess.check_call(["pip", "install", "pulp"])
#pip! install pulp

import pulp
import random
import numpy as np
import csv

#CSVファイルをアップロード(とりあえず)
import pandas as pd
uploaded_file = st.file_uploader("CSVファイルを選択してください。(CSVファイルを読み込み表示させられます。今後最適化を実験するときのために使えるかも)", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if st.button('CSV表示',use_container_width=True):

    ####ここに最適化をいれる####


        ##csvファイルの出力##
        st.write(data)
        #if st.button('学校名の抽出',use_container_width=True):

#ここから下は編集しない
if __name__ == '__main__':
    main()
