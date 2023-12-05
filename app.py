from flask import Flask, request
# from flask_cors import CORS
from roadmap import RoadmapService
from clustering import ClusteringService
from recommendation import RecommendationService
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
roadmap_service = RoadmapService()
cluster_service = ClusteringService()
recommendation_service = RecommendationService()

@app.route('/ml/get_subject', methods=['POST'])
def get_subject_route():
    return roadmap_service.get_subject()

@app.route('/ml/get_question', methods=['POST'])
def get_question_route():
    return roadmap_service.get_question()

@app.route('/ml/recommend_problems', methods=['POST'])
def recommend_problems_route():
    return cluster_service.recommend_problems()

@app.route('/ml/find_similar_question', methods=['POST'])
def find_similar_question():
    data = request.get_json()
    title = data['title']
    return recommendation_service.find_similar_question(title)

if __name__ == '__main__':
    app.run(debug=True)