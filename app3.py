from flask import Flask, request, jsonify
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings(action='ignore')
app3 = Flask(__name__)

def problem_recommendation(df, idx, name):
    test = df[df['name'] == name]

    # 조건에 맞는 행 추출
    level = []
    ran = 2
    k = int(test['level'].iloc[0])

    for i in range(k - ran, k + ran + 1):
        level.append(i)

    # test['레벨']에 level이 포함된 행 추출
    filtered_rows = df[df['level'].isin(level)]

    # 최적의 군집 수 찾기
    kmeans = KMeans(random_state=42)
    KEV = KElbowVisualizer(kmeans, k=20, n_init="auto")
    KEV.fit(filtered_rows[['level', 'unrated', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby']])
    plt.close()

    n_clusters = KEV.elbow_value_

    # 찾은 최적의 군집 수로 군집화
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(filtered_rows[['level', 'unrated', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby']])

    # 군집화 결과를 Cluster 컬럼에 넣음
    filtered_rows['Cluster'] = kmeans.labels_

    # test 사용자와 같은 군집에 속한 사용자 추출
    total = filtered_rows[filtered_rows['Cluster'] == filtered_rows.iloc[idx]['Cluster']].drop(index=idx)

    total['problem_number'] = total['problem_number'].str.replace('[', '')
    total['problem_number'] = total['problem_number'].str.replace(']', '')

    test['problem_number'] = test['problem_number'].str.replace('[', '')
    test['problem_number'] = test['problem_number'].str.replace(']', '')

    # 문제 번호를 쉼표로 구분하여 나누고, 빈도수를 계산하기
    test_counts = test['problem_number'].str.split(',').explode().apply(int).to_list()

    # test 사용자가 풀지 않은 문제 추출
    problem_counts = total[~total['problem_number'].isin(test_counts)]

    # 문제 번호를 쉼표로 구분하여 나누고, 빈도수를 계산하기
    problem_counts = total['problem_number'].str.split(',').explode().apply(int).value_counts()

    return problem_counts[:5].index.to_list()


# 사용자 데이터 불러오기
df = pd.read_csv('fake_user.csv')
df.columns = ['name', 'level', 'problem_number', 'problem_level', 'unrated', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby']

# 문제 데이터 불러오기
q = pd.read_csv('df_problems.csv')
q.columns = ['content_link', 'title', 'problem', 'rate', 'number', 'korean', 'level', 'classification', '별칭']

@app3.route('/ml/recommend_problems', methods=['POST'])
def recommend_problems():
    data = request.get_json()
    name = data['name']

    # Get user index
    idx = df[df['name'] == name].index[0]

    # Get recommended problems
    question = problem_recommendation(df, idx, name)

    # Get problem details
    result = q[q['number'].isin(question)][['number', 'title']].to_dict(orient='records')

    return jsonify({'recommended_problems': result})

if __name__ == '__main__':
    app3.run()