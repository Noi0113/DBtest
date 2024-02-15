import streamlit as st
import subprocess
import pulp
import random
import numpy as np
import csv
import pandas as pd
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# スコープの設定（Google Sheets API および Google Drive API のスコープを追加）
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Google Sheets認証情報の読み込み
credentials = ServiceAccountCredentials.from_json_keyfile_name('monketsu-karuta-a50fe8e854dc.json', scopes)
gc = gspread.authorize(credentials)

##########ここまでスプシ接続設定#######


#def data_retu(table_name, target_name,target_id, column_name):
#    conn = sqlite3.connect('monka.db')
#    c = conn.cursor()
#    query = f"SELECT {column_name} FROM {table_name} WHERE {target_name} = ?;"
#    c.execute(query, (target_id,))
#    result = c.fetchall()
#    conn.close()
#    result_list = [item[0] for item in result]
#    return result_list

#def get_data_by_taikaiid(n, id):
    # データベースファイルのパスを正確に指定
    #conn = sqlite3.connect('monka.db')

    # s1, s2, ..., s{n} を結合した文字列を生成
    #S = ", ".join([f"s{i}" for i in range(1, n+1)])

    # user_dataテーブルから特定のtaikaiidに一致する行を取得
    #query = f"SELECT name, school, level, kisuu, wantto, wantnotto, {S} FROM user_data WHERE taikaiid=?"
    #df = pd.read_sql_query(query, conn, params=(id,))

    #conn.close()
    #return df


#login
def login_user(id,pas):
    conn = sqlite3.connect('monka.db')
    c = conn.cursor()
    c.execute('SELECT * FROM taikai_data WHERE taikaiid =? AND password = ?',(id,pas))
    data = c.fetchall()
    conn.close()
    return data
#hash化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
    
# まずGoogle Sheetsのシート2を開き、それをデータフレーム化する(大会名・パスワードの確認のため。またこれについてはシート2で十分と判断(アンケページにてシート2で確認→シート1に記載されるため)) 
new_gene_sheet = gc.open('monketsu-karuta-db').get_worksheet(1)
new_gene_data = new_gene_sheet.get_all_values()
headers = new_gene_data.pop(0)
new_gene_df = pd.DataFrame(new_gene_data, columns = headers)

# 新規作成ページで作成された大会IDとパスワードを辞書化
id_from_df = new_gene_df.iloc[:,0]
pass_from_df = new_gene_df.iloc[:,1]
id_list = list(id_from_df)
pass_list = list(pass_from_df)
taikai_dict = dict(zip(id_list,pass_list))
   
def main():
    status_area = st.empty()
    #ここから上は編集しない
    
    #タイトル
    st.title('対戦表の作成')
    #install coin-or-cbc

    st.markdown('対戦表を作成したい大会の大会名・大会パスワードを入力してください')
    input_taikaiid = st.text_input(label = '大会名')
    input_password = st.text_input(label = 'パスワード',type = 'password')
    if st.button('対戦表の作成',use_container_width=True):
 #   hashed_pswd = make_hashes(input_password)
 #   result = login_user(input_taikaiid,check_hashes(input_password,hashed_pswd))
 #   if result:
        if input_taikaiid in taikai_dict and taikai_dict[input_taikaiid] == input_password:        
            st.success("対戦表を作成します")
    else:
      st.warning("大会名か大会パスワードが間違っています")  


        
#↓以降最適化の実行

        
  #  uploaded_file = st.file_uploader("CSVファイルを選択してください。(CSVファイルを読み込み表示させられます。今後最適化を実験するときのために使えるかも)", type="csv")
  #  if uploaded_file is not None:
  #      df = pd.read_csv(uploaded_file)
        df = pd.DataFrame()
        conn = sqlite3.connect('monka.db')
        c = conn.cursor()
        num = int(data_retu("taikai_data","taikaiid","zenkoku","snum")[0])
        df = get_data_by_taikaiid(num,input_taikaiid)
        df.insert(0, '個人ID', range(1, len(df) + 1))
        df = df.rename(columns={'name': '名前', 'school': '所属', 'level': '級', 'kisuu': '奇数の時にダミーさんとやりたいですか', 'wantto': '対戦希望', 'wantnotto': '対戦したくない希望', 's1': '第1試合休み', 's2': '第2試合休み', 's3': '第3試合休み', 's4': '第4試合休み', 's5': '第5試合休み', 's6': '第6試合休み', 's7': '第7試合休み', 's8': '第8試合休み', 's9': '第9試合休み', 's10': '第10試合休み', 's11': '第11試合休み', 's12': '第12試合休み', 's13': '第13試合休み', 's14': '第14試合休み', 's15': '第15試合休み'})
        st.table(df)
        conn.close()

        #スプレッドシートのシート1から、大会名が一致
        raw_df = 

        #集合定義
        #試合数
        q_num = len(df.columns)-7
        #試合の集合
        Q = []
        for n in range(1,q_num+1):
            Q.append(f'q{str(n)}')

        #所属の集合
        S = []
        for row in df.itertuples():
            if row.所属 not in S:
                S.append(row.所属)

        #級の集合
        K = []
        for row in df.itertuples():
            if row.級 not in K:
                K.append(row.級)

        #試合参加者の集合
        Iall_old = df['個人ID'].tolist()
        I_all = df['個人ID'].tolist()
        I_all.append('ダミー')

        #試合qを休む人と参加する人の集合
        I_rest = []
        I_sanka_old = []
        I_sanka = []
        for qnum in range(q_num):
          I_rest.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == 1].itertuples()])
          I_sanka_old.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == 0].itertuples()])
          I_sanka.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == 0].itertuples()])

        #I_sankaまたはI_restにダミーを加える
        I_d = []
        for qnum in range(q_num):
          I_d.append([row.奇数の時にダミーさんとやりたいですか for row in df.itertuples()])
          if len(I_sanka[qnum]) % 2 != 0: #試合参加者が奇数の時はダミーさんをI_sankaに入れる
            I_sanka[qnum].append('ダミー')
            I_d[qnum].append(100)
          else: #試合参加者が偶数の時はダミーさんをI_restに入れる
            I_rest[qnum].append('ダミー')

        #対戦ペアの集合
        P = []
        for qnum in range(q_num):
          P.append([f'p{str(k)}' for k in range(1,int(len(I_sanka[qnum])/2)+1)])

        #奇数のときに休みたい人
        I_wanttorest = [row.個人ID for row in df.itertuples() if row.奇数の時にダミーさんとやりたいですか == 1]

        #Wantto(対戦したい人リスト)
        Wantto = []
        wantto1 = [row.個人ID for row in df.itertuples() if row.対戦希望 != 'なし']
        wantto2 = [row.対戦希望 for row in df.itertuples() if row.対戦希望 != 'なし']
        for i in range(len(wantto1)):
          Wantto.append([wantto1[i],wantto2[i]])

        #Dontwantto(対戦したくない人リスト)
        Dontwantto = []
        dontwantto1 = [row.個人ID for row in df.itertuples() if row.対戦したくない希望 != 'なし']
        dontwantto2 = [row.対戦したくない希望 for row in df.itertuples() if row.対戦したくない希望 != 'なし']
        for i in range(len(dontwantto1)):
          Dontwantto.append([dontwantto1[i],dontwantto2[i]])

        #定数

        #重み
        w1 = 3.78  #所属違う
        w2_0 = 4.75  #同級
        w2_1 = 4.66  #1級違い
        w2_2 = 3.63  #2級違い
        w2_3 = 2.81  #3級違い
        w2_4 = 2.21  #4級違い
        w3 = -1000  #同じ対戦相手のペア
        w4_0 = 4.74  #対戦希望
        w4_1 = -4.74  #対戦したくない希望
        w5 = 4.74  #奇数人のとき休みたい人
        w6 = -round((len(I_all)-1)*q_num/5,2) #個人スコアの重み

        #準備①所属

        #所属ごとの辞書
        S_dict = {}
        for s in S:
          S_dict[s] = [row.個人ID for row in df.itertuples() if row.所属 == s]

        #準備②級

        #級ごとの辞書
        K_dict = {}
        for k in K:
          K_dict[k] = [row.個人ID for row in df.itertuples() if row.級 == k]

        #級の組み合わせリスト ←アンケートに基づき分け方変える
        K1K2 = []

        K1K2_0 = {}  #同級の組み合わせ
        for k in K:
          K1K2_0[k] = [k,k]
        K1K2.append(K1K2_0)

        K1K2_1 = {}  #1級違いの組み合わせ
        if 'A' and 'B' in K:
          K1K2_1['AB'] = ['A','B']
        if 'B' and 'C' in K:
          K1K2_1['BC'] = ['B','C']
        if 'C' and 'D' in K:
          K1K2_1['CD'] = ['C','D']
        if 'D' and 'E' in K:
          K1K2_1['DE'] = ['D','E']
        K1K2.append(K1K2_1)

        K1K2_2 = {}  #2級違いの組み合わせ
        if 'A' and 'C' in K:
          K1K2_2['AC'] = ['A','C']
        if 'B' and 'D' in K:
          K1K2_2['BD'] = ['B','D']
        if 'C' and 'E' in K:
          K1K2_2['CE'] = ['C','E']
        K1K2.append(K1K2_2)

        K1K2_3 = {} #3級違いの組み合わせ
        if 'A' and 'D' in K:
          K1K2_3['AD'] = ['A','D']
        if 'B' and 'E' in K:
          K1K2_3['BE'] = ['B','E']
        K1K2.append(K1K2_3)

        K1K2_4 = {} #4級違いの組み合わせ
        if 'A' and 'E' in K:
          K1K2_4['AE'] = ['A','E']
        K1K2.append(K1K2_4)

        #問題定義
        prob = pulp.LpProblem('Taisen1Problem', pulp.LpMaximize)


        #変数定義  ←sc2はアンケートに基づき変える
        #変数x(対戦表)
        QII = [(q,i1,i2) for q in Q for i1 in I_all for i2 in I_all]
        x = pulp.LpVariable.dicts('x', QII, cat = 'Binary')

        #変数score1(全試合の所属のスコア)
        score1 = pulp.LpVariable('score1', cat = 'LpInteger')
        #変数score2_0(全試合の同級のスコア)
        score2_0 = pulp.LpVariable('score2_0', cat = 'LpInteger')
        #変数score2_1(全試合の1級違いのスコア)
        score2_1 = pulp.LpVariable('score2_1', cat = 'LpInteger')
        #変数score2_2(全試合の2級違いのスコア)
        score2_2 = pulp.LpVariable('score2_2', cat = 'LpInteger')
        #変数score2_3(全試合の3級違いのスコア)
        score2_3 = pulp.LpVariable('score2_3', cat = 'LpInteger')
        #変数score2_4(全試合の4級違いのスコア)
        score2_4 = pulp.LpVariable('score2_4', cat = 'LpInteger')
        #変数score3(全試合の同じ対戦相手のスコア)
        score3 = pulp.LpVariable('score3', cat = 'LpInteger')
        #変数score4_0(全試合の対戦希望のスコア)
        score4_0 = pulp.LpVariable('score4_0', cat = 'LpInteger')
        #変数score4_1(全試合の対戦したくない希望のスコア)
        score4_1 = pulp.LpVariable('score4_1', cat = 'LpInteger')
        #変数score5(全試合の休みたい人が休めたときのスコア)
        score5 = pulp.LpVariable('score5', cat = 'LpInteger')
        #変数score6
        score6 = pulp.LpVariable('score6', cat = 'LpInteger')


        #変数sc1(全試合の所属が異なるペア数)
        sc1 = pulp.LpVariable('sc1', cat = 'LpInteger')
        #変数sc2_0(全試合の同級のペア数)
        sc2_0 = pulp.LpVariable('sc2_0', cat = 'LpInteger')
        #変数sc2_1(全試合の1級違いのペア数)
        sc2_1 = pulp.LpVariable('sc2_1', cat = 'LpInteger')
        #変数sc2_2(全試合の2級違いのペア数)
        sc2_2 = pulp.LpVariable('sc2_2', cat = 'LpInteger')
        #変数sc2_3(全試合の3級違いのペア数)
        sc2_3 = pulp.LpVariable('sc2_3', cat = 'LpInteger')
        #変数sc2_4(全試合の4級違いのペア数)
        sc2_4= pulp.LpVariable('sc2_4', cat = 'LpInteger')
        #変数sc3(全試合における同じペアのペア数)
        sc3 = pulp.LpVariable('sc3', cat = 'LpInteger')
        #変数sc4_0(全試合における対戦希望が通った人数)
        sc4_0 = pulp.LpVariable('sc4_0', cat = 'LpInteger')
        #変数sc4_1(全試合における対戦したくない希望が通った人数)
        sc4_1 = pulp.LpVariable('sc4_1', cat = 'LpInteger')
        #変数sc5(全試合における休みたい人が休めた人数)
        sc5 = pulp.LpVariable('sc5', cat = 'LpInteger')
        #変数sc6
        sc6 = pulp.LpVariable('sc6', cat = 'LpInteger')



        #変数sc1q(第q試合目の所属が異なるペア数)
        sc1q = pulp.LpVariable.dicts('sc1q', Q, cat = 'LpInteger')
        #変数sc2q_0(第q試合目の同級のペア数)
        sc2q_0 = pulp.LpVariable.dicts('sc2q_0', Q, cat = 'LpInteger')
        #変数sc2q_1(第q試合目の1級違いのペア数)
        sc2q_1 = pulp.LpVariable.dicts('sc2q_1', Q, cat = 'LpInteger')
        #変数sc2q_2(第q試合目の2級違いのペア数)
        sc2q_2 = pulp.LpVariable.dicts('sc2q_2',Q, cat = 'LpInteger')
        #変数sc2q_3(第q試合目の3級違いのペア数)
        sc2q_3 = pulp.LpVariable.dicts('sc2q_3',Q, cat = 'LpInteger')
        #変数sc2q_4(第q試合目の4級違いのペア数)
        sc2q_4 = pulp.LpVariable.dicts('sc2q_4',Q, cat = 'LpInteger')
        #変数sc4q_0(第q試合目で対戦希望が通った人数)
        sc4q_0 = pulp.LpVariable.dicts('sc4q_0', Q, cat = 'LpInteger')
        #変数sc4q_1(第q試合目で対戦したくない希望が通った人数)
        sc4q_1 = pulp.LpVariable.dicts('sc4q_1', Q, cat = 'LpInteger')
        #変数sc5(第q試合目で対戦希望が通った人数)
        sc5q = pulp.LpVariable.dicts('sc5', Q, cat = 'LpInteger')

        #変数y(参加者i1とi2の対戦回数が1以下⇒0、2以上⇒1)
        II = [(i1,i2) for i1 in I_all for i2 in I_all]
        y = pulp.LpVariable.dicts('y', II, cat = 'Binary')

        #変数z
        IQ = [(i,q) for i in Iall_old for q in Q]
        z = pulp.LpVariable.dicts('z', Iall_old, cat = 'LpInteger')
        z_0 = pulp.LpVariable.dicts('z_0', Iall_old, cat = 'LpInteger')
        z_1 = pulp.LpVariable.dicts('z_1', Iall_old, cat = 'LpInteger')
        z_2 = pulp.LpVariable.dicts('z_2', Iall_old, cat = 'LpInteger')
        z_3 = pulp.LpVariable.dicts('z_3', Iall_old, cat = 'LpInteger')
        zq_0 = pulp.LpVariable.dicts('zq_0', IQ, cat = 'LpInteger')
        zq_1 = pulp.LpVariable.dicts('zq_1', IQ, cat = 'LpInteger')
        zq_2 = pulp.LpVariable.dicts('zq_2', IQ, cat = 'LpInteger')
        zq_3 = pulp.LpVariable.dicts('zq_3', IQ, cat = 'LpInteger')
        zmax = pulp.LpVariable('zmax', cat = 'LpInteger')
        zmin = pulp.LpVariable('zmin', cat = 'LpInteger')

        #制約条件
        #(1)xの条件
        ##(1-1)第q試合に参加する人は対戦表の行の和が1/参加しない人は行の和が0
        qnum = 0
        for q in Q:
          qnum += 1
          for i1 in I_sanka[qnum-1]:
            prob += pulp.lpSum(x[q,i1,i2] for i2 in I_all)  == 1
          for i1 in I_rest[qnum-1]:
            prob += pulp.lpSum(x[q,i1,i2] for i2 in I_all)  == 0

        ##(1-2)対戦表は左右対称
          for i1 in I_all:
            for i2 in I_all:
              prob += x[q,i1,i2] == x[q,i2,i1]

        ##(1-3)対戦表の対角成分は0(同じ人同士は対戦しない)
              if i1 == i2:
                prob += x[q,i1,i2] == 0


        #スコアに反映
        #(2)所属が異なるほうが良い
        qnum = 0
        for q in Q:
          qnum += 1
          sc1q_sub = []    #第q試合における学校s同士のペア数のリスト
          for s in S:
            ss_num = pulp.lpSum(x[q,i1,i2] for i1 in S_dict[s] for i2 in S_dict[s])/2 #学校s同士のペア数
            sc1q_sub.append(ss_num)
          sum = pulp.lpSum(sc1q_sub)

          #sc1q:所属が異なるペア数
          if len(I_sanka_old[qnum-1]) % 2 == 0:
            prob += sc1q[q] == len(P[qnum-1]) -sum
          else:
            prob += sc1q[q] == len(P[qnum-1]) - sum -1  #奇数の場合はダミーを含むペアを引く


          ##スコア定義
          prob += sc1 == pulp.lpSum(sc1q[q] for q in Q)
          prob += score1 == w1 * sc1

          #(3)級が近いほうが良い ←アンケートに基づいて変更する
          for q in Q:
          ##同級
            sc2q_0_list = []
            for k1k2 in K1K2_0:
              k1 = K1K2_0[k1k2][0]
              k2 = K1K2_0[k1k2][1]
              num = pulp.lpSum([x[q,i1,i2] for i1 in K_dict[k1] for i2 in K_dict[k2]])/2 #級k同士のペア数
              sc2q_0_list.append(num)
            prob += sc2q_0[q] == pulp.lpSum(sc2q_0_list)

          ##1級違い
            sc2q_1_list = []
            for k1k2 in K1K2_1:
              k1 = K1K2_1[k1k2][0]
              k2 = K1K2_1[k1k2][1]
              num = pulp.lpSum([x[q,i1,i2] for i1 in K_dict[k1] for i2 in K_dict[k2]]) #級k1k2同士のペア数
              sc2q_1_list.append(num)
            prob += sc2q_1[q] == pulp.lpSum(sc2q_1_list)

          ##2級違い
            sc2q_2_list = []
            for k1k2 in K1K2_2:
              k1 = K1K2_2[k1k2][0]
              k2 = K1K2_2[k1k2][1]
              num = pulp.lpSum([x[q,i1,i2] for i1 in K_dict[k1] for i2 in K_dict[k2]]) #級k1k2同士のペア数
              sc2q_2_list.append(num)
            prob += sc2q_2[q] == pulp.lpSum(sc2q_2_list)

          ##3級違い
            sc2q_3_list = []
            for k1k2 in K1K2_3:
              k1 = K1K2_3[k1k2][0]
              k2 = K1K2_3[k1k2][1]
              num = pulp.lpSum([x[q,i1,i2] for i1 in K_dict[k1] for i2 in K_dict[k2]]) #級k1k2同士のペア数
              sc2q_3_list.append(num)
            prob += sc2q_3[q] == pulp.lpSum(sc2q_3_list)

          ##4級違い
            sc2q_4_list = []
            for k1k2 in K1K2_4:
              k1 = K1K2_4[k1k2][0]
              k2 = K1K2_4[k1k2][1]
              num = pulp.lpSum([x[q,i1,i2] for i1 in K_dict[k1] for i2 in K_dict[k2]]) #級k1k2同士のペア数
              sc2q_4_list.append(num)
            prob += sc2q_4[q] == pulp.lpSum(sc2q_4_list)

        ##スコア定義
        prob += sc2_0 == pulp.lpSum(sc2q_0[q] for q in Q)
        prob += sc2_1 == pulp.lpSum(sc2q_1[q] for q in Q)
        prob += sc2_2 == pulp.lpSum(sc2q_2[q] for q in Q)
        prob += sc2_3 == pulp.lpSum(sc2q_3[q] for q in Q)
        prob += sc2_4 == pulp.lpSum(sc2q_4[q] for q in Q)
        prob += score2_0 == w2_0 * sc2_0
        prob += score2_1 == w2_1 * sc2_1
        prob += score2_2 == w2_2 * sc2_2
        prob += score2_3 == w2_3 * sc2_3
        prob += score2_4 == w2_4 * sc2_4

        #(4)なるべく同じ人と対戦しないようにする
        #変数y...参加者i1とi2の対戦回数が1以下⇒0、2以上⇒1
        for i1 in I_all:
          for i2 in I_all:
            sum = pulp.lpSum(x[q,i1,i2] for q in Q)
            prob += y[i1,i2] <= 0.5 * sum
            prob += y[i1,i2] >= 0.000001 * sum - 0.000001

        ##スコア定義
        #sc3...全試合における同じペアのペア数
        prob += sc3 == pulp.lpSum(y[i1,i2] for i1 in I_all for i2 in I_all)/2
        prob += score3 == w3 * sc3

        #(5)なるべく対戦希望、したくない希望が通るようにする
        for q in Q:
          sc4q_0_list = []
          for wantto in Wantto:
            wantto1 = wantto[0]
            wantto2 = wantto[1]
            num = pulp.lpSum([x[q,wantto1,wantto2]])
            sc4q_0_list.append(num)
          prob += sc4q_0[q] == pulp.lpSum(sc4q_0_list)

          sc4q_1_list = []
          for dontwantto in Dontwantto:
            dontwantto1 = dontwantto[0]
            dontwantto2 = dontwantto[1]
            num = pulp.lpSum([x[q,dontwantto1,dontwantto2]])
            sc4q_1_list.append(num)
          prob += sc4q_1[q] == pulp.lpSum(sc4q_1_list)

        ##スコア定義
        #sc4_0...対戦希望が通った人数 #sc4_1...対戦したくない希望が通らなかった人数
        prob += sc4_0 == pulp.lpSum(sc4q_0[q] for q in Q)
        prob += sc4_1 == pulp.lpSum(sc4q_1[q] for q in Q)
        prob += score4_0 == w4_0 * sc4_0
        prob += score4_1 == w4_1 * sc4_1

        #(6)奇数のとき休みたい人がいれば優先的に休ませる
        for q in Q:
          sc5q_list = []
          for i in I_wanttorest:
            num = pulp.lpSum([x[q,i,'ダミー']])
            sc5q_list.append(num)
          prob += sc5q[q] == pulp.lpSum(sc5q_list)

        ##スコア定義
        #sc4_0...対戦希望が通った人数 #sc4_1...対戦したくない希望が通らなかった人数
        prob += sc5 == pulp.lpSum(sc5q[q] for q in Q)
        prob += score5 == w5 * sc5

        #(7)個人のスコアの範囲をできるだけ小さくする
        #所属
        for i1 in Iall_old:
          qnum = 0
          for q in Q:
            qnum += 1
            zq_0[i1,q] = 0
            if i1 in I_rest[qnum-1]:
              zq_0[i1,q] += pulp.lpSum([z_0[i] for i in Iall_old])/len(Iall_old)/q_num
            for i2 in Iall_old:
              for s in S:
                if i1 in S_dict[s] and i2 not in S_dict[s]:
                  zq_0[i1,q] += w1 * x[q,i1,i2]
          prob += z_0[i1] == pulp.lpSum([zq_0[i1,q] for q in Q])

        #級
        for i1 in Iall_old:
          qnum = 0
          for q in Q:
            qnum += 1
            zq_1[i1,q] = 0
            if i1 in I_rest[qnum-1]:
              zq_1[i1,q] += pulp.lpSum([z_1[i] for i in Iall_old])/len(Iall_old)/q_num
            for i2 in Iall_old:
              if 'A' in K:
                if i1 in K_dict['A'] and i2 in K_dict['A']:
                  zq_1[i1,q] += w2_0 * x[q,i1,i2]
              if 'B' in K:
                if i1 in K_dict['B'] and i2 in K_dict['B']:
                  zq_1[i1,q] += w2_0 * x[q,i1,i2]
              if 'C' in K:
                if i1 in K_dict['C'] and i2 in K_dict['C']:
                  zq_1[i1,q] += w2_0 * x[q,i1,i2]
              if 'D' in K:
                if i1 in K_dict['D'] and i2 in K_dict['D']:
                  zq_1[i1,q] += w2_0 * x[q,i1,i2]
              if 'E' in K:
                if i1 in K_dict['E'] and i2 in K_dict['E']:
                  zq_1[i1,q] += w2_0 * x[q,i1,i2]
              if 'A' in K and 'B' in K:
                if i1 in K_dict['A'] and i2 in K_dict['B']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
                if i1 in K_dict['B'] and i2 in K_dict['A']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
              if 'B' in K and 'C' in K:
                if i1 in K_dict['B'] and i2 in K_dict['C']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
                if i1 in K_dict['C'] and i2 in K_dict['B']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
              if 'C' in K and 'D' in K:
                if i1 in K_dict['C'] and i2 in K_dict['D']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
                if i1 in K_dict['D'] and i2 in K_dict['C']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
              if 'D' in K and 'E' in K:
                if i1 in K_dict['D'] and i2 in K_dict['E']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
                if i1 in K_dict['E'] and i2 in K_dict['D']:
                  zq_1[i1,q] += w2_1 * x[q,i1,i2]
              if 'A' in K and 'C' in K:
                if i1 in K_dict['A'] and i2 in K_dict['C']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]
                if i1 in K_dict['C'] and i2 in K_dict['A']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]
              if 'B' in K and 'D' in K:
                if i1 in K_dict['B'] and i2 in K_dict['D']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]
                if i1 in K_dict['D'] and i2 in K_dict['B']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]
              if 'C' in K and 'E' in K:
                if i1 in K_dict['C'] and i2 in K_dict['E']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]
                if i1 in K_dict['E'] and i2 in K_dict['C']:
                  zq_1[i1,q] += w2_2 * x[q,i1,i2]

              if 'A' in K and 'D' in K:
                if i1 in K_dict['A'] and i2 in K_dict['D']:
                  zq_1[i1,q] += w2_3 * x[q,i1,i2]
                if i1 in K_dict['D'] and i2 in K_dict['A']:
                  zq_1[i1,q] += w2_3 * x[q,i1,i2]
              if 'B' in K and 'E' in K:
                if i1 in K_dict['B'] and i2 in K_dict['E']:
                  zq_1[i1,q] += w2_3 * x[q,i1,i2]
                if i1 in K_dict['E'] and i2 in K_dict['B']:
                  zq_1[i1,q] += w2_3 * x[q,i1,i2]

              if 'A' in K and 'E' in K:
                if i1 in K_dict['A'] and i2 in K_dict['E']:
                  zq_1[i1,q] += w2_4 * x[q,i1,i2]
                if i1 in K_dict['E'] and i2 in K_dict['A']:
                  zq_1[i1,q] += w2_4 * x[q,i1,i2]


          prob += z_1[i1] == pulp.lpSum([zq_1[i1,q] for q in Q])

        #休みたい希望
        for i1 in Iall_old:
          qnum = 0
          for q in Q:
            qnum += 1
            zq_2[i1,q] = 0
            if i1 in I_rest[qnum-1]:
              zq_2[i1,q] += pulp.lpSum([z_2[i] for i in Iall_old])/len(Iall_old)/q_num
            if i1 in I_wanttorest:
              zq_2[i1,q] += w5 * x[q,i1,'ダミー']
          prob += z_2[i1] == pulp.lpSum([zq_2[i1,q] for q in Q])

        #対戦希望、対戦したくない希望
        for i1 in Iall_old:
          qnum = 0
          for q in Q:
            qnum += 1
            zq_3[i1,q] = 0
            if i1 in I_rest[qnum-1]:
              zq_3[i1,q] += pulp.lpSum([z_3[i] for i in Iall_old])/len(Iall_old)/q_num
            for i2 in Iall_old:
              for pair in Wantto:
                if (i1 == pair[0] and i2 == pair[1]) or (i1 == pair[1] and i2 == pair[0]):
                  zq_3[i1,q] += w4_0 * x[q,i1,i2]
              for pair in Dontwantto:
                if (i1 == pair[0] and i2 == pair[1]) or (i1 == pair[1] and i2 == pair[0]):
                  zq_3[i1,q] += w4_1 * x[q,i1,i2]
          prob += z_3[i1] == pulp.lpSum([zq_3[i1,q] for q in Q])



        for i in Iall_old:
          prob += z[i] == z_0[i] + z_1[i] + z_2[i] + z_3[i]
          prob += z[i] <= zmax
          prob += z[i] >= zmin
        prob += sc6 == (zmax - zmin)/q_num

        prob += score6 == w6 * sc6

        #totalscore定義
        totalscore = score1 + score2_0 + score2_1 + score2_2 + score2_3 + score2_4 + score3 + score4_0 + score4_1 + score5 + score6

        #目的関数定義
        prob += totalscore
        #求解
        status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=240 ))

        kekkalistx = []
        restlist = []
        rest2list =[]
        kekkanew = []

        # 各クラスに割り当てられている生徒のリストを辞書に格納
        qnum = 0
        for q in Q:
          qnum += 1
          kekka = {}
          rest2 = []
          pair = 0
          for i1 in I_all:
            for i2 in I_all:
              if x[q,i1,i2].value() == 1 and [i2,i1] not in kekka.values() and i1 != 'ダミー' and i2 != 'ダミー':
                pair += 1
                kekka[P[qnum-1][pair-1]] = [i1,i2]
              elif x[q,i1,i2].value() == 1 and [i2,i1] not in kekka.values() and i1 not in rest2 and i1 != 'ダミー':
                rest2.append(i1)

          #出力のため
          kekkax = []
          for p,i1i2 in kekka.items():
            kekkax.append([i1i2[0],i1i2[1]])
          kekkalistx.append(kekkax)

          restlist.append(I_rest[qnum-1])
          rest2list.append(rest2)

        namex = [row.名前 for row in df.itertuples()]
        idx = [row.個人ID for row in df.itertuples()]
        name_kekkalistx = []
        for q in range(len(Q)):
          name_kekkalistx.append([])
          for p in range(len(kekkalistx[q])):
            name1=namex[idx.index(kekkalistx[q][p][0])]
            name2=namex[idx.index(kekkalistx[q][p][1])]
            name_kekkalistx[q].append([name1,name2])

        #出力準備
        restlistindex = -1
        for list in restlist:
          restlistindex += 1
          if 'ダミー' in list:
            list.remove('ダミー')
          if list == []:
            restlist[restlistindex] = 'なし'
          if list != []:
            namelist = []
            for i in list:
              name = namex[idx.index(i)]
              namelist.append(name)
            restlist[restlistindex] = namelist

        rest2listindex = -1
        for list2 in rest2list:
          rest2listindex += 1
          if list2 == []:
            rest2list[rest2listindex] = 'なし'
          if list2 != []:
            for i in list2:
              name = namex[idx.index(i)]
              rest2list[rest2listindex] = name

        pairnumlist = []
        qnum = 0
        for q in Q:
          qnum += 1
          pairnumlist.append(len(kekkalistx[qnum-1]))
        maxpairnum = max(pairnumlist)

        kekkalist_new = []
        pnum = 0
        for p in range(maxpairnum):
          qnum = 0
          pnum += 1
          plist = []
          plist.append('p{}'.format(pnum))
          for q in Q:
            qnum += 1
            if pairnumlist[qnum-1] >= pnum:
              plist.append('{}vs{}'.format(name_kekkalistx[qnum-1][pnum-1][0],name_kekkalistx[qnum-1][pnum-1][1]))
            else:
              plist.append('')
          kekkalist_new.append(plist)

        Qnew = []
        Qnew.append('')
        for q in Q:
          Qnew.append(q)

        qindex = -1
        for list in restlist:
          qindex += 1
          if list == 'なし':
            restlist[qindex] = 'なし'
          else:
            restlist[qindex] = ', '.join(list)
          restlist.insert(0,'休み')
          rest2list.insert(0,'奇数人のため休み')

        ##csvファイルの出力##
        data = {}
        data[0]=Qnew
        for i in range(maxpairnum):
            data[i+1] = kekkalist_new[i]
        data[maxpairnum+1] = restlist
        data[maxpairnum+2] = rest2list
        new_df = pd.DataFrame(data)
        new_df_trans = new_df.transpose()
        new_df_trans.to_csv("outputcsv", index =False)
        st.write(new_df_trans)

        st.success("新しいCSVファイルが出力されました。")


#ここから下は編集しない
if __name__ == '__main__':
    main()
