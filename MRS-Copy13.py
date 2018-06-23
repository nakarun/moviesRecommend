import time
start = time.time()

#パンダスの準備
import pandas as pd
from pandas import Series,DataFrame

#SQLの準備
import sqlite3
con = sqlite3.connect("movies_c.db")

# 関数を作って、SQL文の実行結果をDataFrameにして返します。
def sql_to_df(sql_query):

    # read_sqlの引数に、SQL文とデータベースへのConnectionを渡します。
    df = pd.read_sql(sql_query, con)

    # 結果のDataFrameを返します。
    return df

import MeCab
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

#保存するようのDF
want_df = pd.DataFrame(columns=['id', 'word', 'num'])

watch = '''
コメディ映画。めちゃくちゃ笑いたい。イギリスっぽいアイロニーを含んだ映画がみたい。
知的な笑いで、パティントンとかそういう映画。
テッドとか下品な映画ではなくて、上品な笑いがいい。
'''

#字句解析して、pandasに保存
text = watch
mecab.parse('')#文字列がGCされるのを防ぐ
node = mecab.parseToNode(text)
i_id=0
while node:
    #単語を取得
    word = node.surface
    #品詞を取得
    pos = node.feature.split(",")[1]
    #print('{}'.format(word))
    #print('{0} , {1}'.format(word, pos))
        
    #次の単語に進める
    node = node.next

    s = pd.DataFrame([[i_id, word, 1]], columns=['id', 'word', 'num'])
    want_df = want_df.append(s)
    #want.append(pd.DataFrame([i_id, word, 1]))
    
i_id += 1

#先に保存しておいたモデルのワードとIDの対応表をpandasで作成しておく
sql_query='''
SELECT * FROM num_words
'''
num_words = sql_to_df(sql_query)

#その対応表と字句解析したワードの表をマージ
m = pd.merge(want_df, num_words, on='word')

#頻出回数を計算
mm = m.groupby("id_y")["num"].sum()

mmm = pd.DataFrame(mm)
want_df = mmm.T

l = []
for num in range(0,30400):
    literal = num
    l.append(literal)
    
all_df = pd.DataFrame(columns = l)
all_df = all_df.T
all_df.index.names = ["id_y"]

want_df = want_df.T
last_df = all_df.join(want_df)
last_df = last_df.fillna(0)
all_df = last_df.T

con.close

import numpy as np
import pandas as pd
from pandas import Series,DataFrame

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

#%matplotlib inline

from sklearn import linear_model

from sklearn.externals import joblib
#モデルの読み込み
logreg = joblib.load("model_dir/model")

all_numpyMatrix_data = all_df.as_matrix()
X_test = all_numpyMatrix_data
_test_data = DataFrame(X_test)

# テストデータを予測します。
Y_pred = logreg.predict(X_test)

print(Y_pred[0])

elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time))