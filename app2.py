from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

app2 = Flask(__name__)

# 문제 데이터프레임 불러오기
df = pd.read_csv('df_problems.csv')
df.columns = ['content_link', 'title', 'problem', 'rate', 'number', 'korean', 'level', 'classification', '별칭']

# null값 처리
df.loc[df['classification'].isnull(), 'classification'] = '0'

# 문장 리스트
sentences = df['classification'].tolist()

# TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

# 코사인 유사도 계산
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# sentence-bert 문장 유사도 행렬 불러오기
with open('similarities_sb.pkl', 'rb') as f:
    similarities_sb = pickle.load(f)

# 최종 유사도, sentence-bert 문장 유사도 행렬과 분류 코사인 유사도 행렬을 더함
combined_matrix = similarities_sb + cosine_sim


def find_similar_sentences(title, top_n=20):
    title_data = df[df['title'] == title]
    title_index = title_data.index.values[0]

    # 해당 작품과 다른 작품 간의 유사도
    title_similarity_scores = combined_matrix[title_index]

    # 유사도가 높은 상위 N개 인덱스를 찾음
    similar_indexes = np.argsort(title_similarity_scores)[::-1][:top_n]

    # 유사도 값 가져오기
    similar_cosine_values = [title_similarity_scores[i] for i in similar_indexes]

    # 유사한 작품 데이터 프레임 생성
    similar_titles = df.iloc[similar_indexes]

    # "유사도" 열 추가
    similar_titles['similar'] = similar_cosine_values

    # 현재 선택한 제목(title)의 인덱스(title_index)가 유사한 제목들의 리스트(similar_indexes) 안에 있는지 확인
    if title_index in similar_indexes:
        # 현재 선택한 제목을 유사한 제목들의 데이터프레임(similar_titles)에서 제외
        similar_titles = similar_titles[similar_titles.index != title_index]
        # 현재 선택한 제목의 데이터를 원본 데이터프레임(df)에서 가져와 title_row에 저장
        # title_row = df.loc[title_index]
        # title_row['유사도'] = '기준'
        # similar_titles = pd.concat([pd.DataFrame([title_row]), similar_titles])

    # 현재 선택한 제목(title)의 레벨(level)을 가져옴
    title_level = title_data['level'].values[0]

    # 레벨이 현재 선택한 제목(title)의 레벨과 3 이내로 차이나는 항목만 필터링
    similar_titles = similar_titles[abs(similar_titles['level'] - title_level) <= 3]

    return similar_titles[['number', 'content_link', 'title', 'problem', 'level', 'classification', 'similar']]

@app2.route('/ml/find_similar_question', methods=['POST'])
def find_similar_question():
    data = request.get_json()
    title = data['title']

    similar_titles = find_similar_sentences(title, 20)

    # Convert DataFrame to JSON
    result_json = similar_titles.to_dict(orient='records')

    return jsonify({'result': result_json})

if __name__ == '__main__':
    app2.run()