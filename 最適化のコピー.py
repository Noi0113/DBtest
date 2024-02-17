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
import hashlib

# スコープの設定（Google Sheets API および Google Drive API のスコープを追加）
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Google Sheets認証情報の読み込み
credentials = ServiceAccountCredentials.from_json_keyfile_name('monketsu-karuta-a50fe8e854dc.json', scopes)
gc = gspread.authorize(credentials)

##########ここまでスプシ接続設定#######

# まずGoogle Sheetsのシート2を開き、それをデータフレーム化する(大会名・パスワードの確認のため。またこれについてはシート2で十分と判断した。(アンケページにてシート2で確認→シート1に記載されるため)) 
new_gene_sheet = gc.open('monketsu-karuta-db').get_worksheet(1)
new_gene_data = new_gene_sheet.get_all_values()
headers = new_gene_data.pop(0)
new_gene_df = pd.DataFrame(new_gene_data, columns = headers)

# まずGoogle Sheetsのシート1を開き、それをデータフレーム化する
sheet1 = gc.open('monketsu-karuta-db').get_worksheet(0)
sheet1_data = sheet1.get_all_values()
headers = sheet1_data.pop(0)
raw_df = pd.DataFrame(sheet1_data, columns = headers)

# 新規作成ページで作成された大会IDとパスワードを辞書化
id_from_df = new_gene_df.iloc[:,0]
pass_from_df = new_gene_df.iloc[:,1]
id_list = list(id_from_df)
pass_list = list(pass_from_df)
taikai_dict = dict(zip(id_list,pass_list))

#hash化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
   
def main():
    status_area = st.empty()
    #ここから上は編集しない
    
    #タイトル
    st.title('対戦表の作成ページです(スプシ版)')
    #install coin-or-cbc

    st.markdown('対戦表を作成したい大会の大会名・大会パスワードを入力してください')
    input_taikaiid = st.text_input(label = '大会名')
    input_password = st.text_input(label = 'パスワード',type = 'password')

  #  hashed_pswd = make_hashes(input_password)
  #  checked_password = check_hashes(input_password,hashed_pswd)

    if st.button('対戦表の作成',use_container_width=True):
     #   if input_taikaiid in taikai_dict and taikai_dict[input_taikaiid] == checked_password:
            st.success("対戦表を作成します")

        
#↓以降最適化の実行
          #######スプシversion#######
            #大会名が入力内容と一致した行を抜き出し必要な情報を取り出す(今回は試合数が知りたい)
            filtered_new_gene_df = new_gene_df[new_gene_df.iloc[:,0] == input_taikaiid]
            s_num = int(filtered_new_gene_df.iloc[0,2])

            #スプレッドシートのシート1から、大会名が一致する行のみ取り出し一旦DF化(filtered_df)
            filtered_df = raw_df[raw_df.iloc[:,0] == input_taikaiid]
            #filtered_dfから必要な列のみ取り出す(これにより大会名・大会パス・不要な試合分の欠席が除かれる)
            df = filtered_df.iloc[:,2:s_num+8]
            #列数に番号を付け、それを個人IDとする
            df.insert(0, '個人ID', range(1, len(df) + 1))

            # いろいろ確認したいから、一応スプシから取得して形成したDFを表示させておく
            st.table(df)
            #######スプシversion#######


            #######以下最適化
            q_num = len(df.columns)-7
            
            Q = []
            for n in range(1,q_num+1):
                Q.append(f'q{str(n)}')
           
            S = []
            for row in df.itertuples():
                if row.所属 not in S:
                    S.append(row.所属)
           
            K = []
            for row in df.itertuples():
                if row.級 not in K:
                    K.append(row.級)

            Iall_old = df['個人ID'].tolist()
            I_all = df['個人ID'].tolist()
            I_all.append('ダミー')
            st.success(Iall_old)
            st.success(I_all)

            I_rest = []
            I_sanka_old = []
            I_sanka = []
           
            for qnum in range(q_num):
              I_rest.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == '1'].itertuples()])
              I_sanka_old.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == '0'].itertuples()])
              I_sanka.append([row.個人ID for row in df.loc[df['第{}試合休み'.format(qnum+1)] == '0'].itertuples()])

            I_d = []
            for qnum in range(q_num):
              I_d.append([row.奇数の時にダミーさんとやりたいですか for row in df.itertuples()])
              if len(I_sanka[qnum]) % 2 != 0:
                I_sanka[qnum].append('ダミー')
                I_d[qnum].append(100)
              else:
                I_rest[qnum].append('ダミー')


            P = []
            for qnum in range(q_num):
              P.append([f'p{str(k)}' for k in range(1,int(len(I_sanka[qnum])/2)+1)])

            I_wanttorest = [row.個人ID for row in df.itertuples() if row.奇数の時にダミーさんとやりたいですか == 1]

            Wantto = []
            wantto1 = [row.個人ID for row in df.itertuples() if row.対戦希望 != 'なし' and row.対戦希望!='']
            wantto2 = [row.対戦希望 for row in df.itertuples() if row.対戦希望 != 'なし' and row.対戦希望!='']
            for i in range(len(wantto1)):
              Wantto.append([wantto1[i],wantto2[i]])

            Dontwantto = []
            dontwantto1 = [row.個人ID for row in df.itertuples() if row.対戦したくない希望 != 'なし' and row.対戦したくない希望!='']
            dontwantto2 = [row.対戦したくない希望 for row in df.itertuples() if row.対戦したくない希望 != 'なし' and row.対戦したくない希望!='']
            for i in range(len(dontwantto1)):
              Dontwantto.append([dontwantto1[i],dontwantto2[i]])

            w1 = 3.78
      
            S_dict = {}
            for s in S:
              S_dict[s] = [row.個人ID for row in df.itertuples() if row.所属 == s]

            K_dict = {}
            for k in K:
              K_dict[k] = [row.個人ID for row in df.itertuples() if row.級 == k]

            K1K2 = []

            K1K2_0 = {}
            for k in K:
              K1K2_0[k] = [k,k]
            K1K2.append(K1K2_0)

            K1K2_1 = {}
            if 'A' and 'B' in K:
              K1K2_1['AB'] = ['A','B']
            if 'B' and 'C' in K:
              K1K2_1['BC'] = ['B','C']
            if 'C' and 'D' in K:
              K1K2_1['CD'] = ['C','D']
            if 'D' and 'E' in K:
              K1K2_1['DE'] = ['D','E']
            K1K2.append(K1K2_1)

            K1K2_2 = {}
            if 'A' and 'C' in K:
              K1K2_2['AC'] = ['A','C']
            if 'B' and 'D' in K:
              K1K2_2['BD'] = ['B','D']
            if 'C' and 'E' in K:
              K1K2_2['CE'] = ['C','E']
            K1K2.append(K1K2_2)

            K1K2_3 = {}
            if 'A' and 'D' in K:
              K1K2_3['AD'] = ['A','D']
            if 'B' and 'E' in K:
              K1K2_3['BE'] = ['B','E']
            K1K2.append(K1K2_3)

            K1K2_4 = {}
            if 'A' and 'E' in K:
              K1K2_4['AE'] = ['A','E']
            K1K2.append(K1K2_4)


            prob = pulp.LpProblem('Taisen1Problem', pulp.LpMaximize)


            QII = [(q,i1,i2) for q in Q for i1 in I_all for i2 in I_all]
            x = pulp.LpVariable.dicts('x', QII, cat = 'Binary')

            #変数score1(全試合の所属のスコア)
            score1 = pulp.LpVariable('score1', cat = 'LpInteger')


            #変数sc1(全試合の所属が異なるペア数)
            sc1 = pulp.LpVariable('sc1', cat = 'LpInteger')


            #変数sc1q(第q試合目の所属が異なるペア数)
            sc1q = pulp.LpVariable.dicts('sc1q', Q, cat = 'LpInteger')

            qnum = 0
            for q in Q:
              qnum += 1
              for i1 in I_sanka[qnum-1]:
                prob += pulp.lpSum(x[q,i1,i2] for i2 in I_all)  == 1
              for i1 in I_rest[qnum-1]:
                prob += pulp.lpSum(x[q,i1,i2] for i2 in I_all)  == 0

              for i1 in I_all:
                for i2 in I_all:
                  prob += x[q,i1,i2] == x[q,i2,i1]

                  if i1 == i2:
                    prob += x[q,i1,i2] == 0

            qnum = 0
            for q in Q:
              qnum += 1
              sc1q_sub = []
              for s in S:
                ss_num = pulp.lpSum(x[q,i1,i2] for i1 in S_dict[s] for i2 in S_dict[s])/2
                sc1q_sub.append(ss_num)
              sum = pulp.lpSum(sc1q_sub)

             
              if len(I_sanka_old[qnum-1]) % 2 == 0:
                prob += sc1q[q] == len(P[qnum-1]) -sum
              else:
                prob += sc1q[q] == len(P[qnum-1]) - sum -1


            prob += sc1 == pulp.lpSum(sc1q[q] for q in Q)
            prob += score1 == w1 * sc1


            totalscore = score1
    
            prob += totalscore
            
            status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=240 ))

                     
            kekkalistx = []
            restlist = []
            rest2list =[]
            kekkanew = []

     
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

     #   else:
      #    st.warning("大会名か大会パスワードが間違っています")  
#ここから下は編集しない
if __name__ == '__main__':
    main()
