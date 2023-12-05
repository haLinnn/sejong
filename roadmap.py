from flask import Flask, request, jsonify
# from flask_cors import CORS
import pandas as pd
from konlpy.tag import Okt


class RoadmapService:
    def __init__(self):
        self.load_data()

    def load_data(self):
        self.df_if = pd.read_csv('recommend/ifelse.csv', encoding='utf-8')
        self.df_for = pd.read_csv('recommend/for.csv', encoding='utf-8')
        self.df_arr = pd.read_csv('recommend/array.csv', encoding='utf-8')
        self.df_string = pd.read_csv('recommend/string.csv', encoding='utf-8')
        self.df_function = pd.read_csv('recommend/function.csv', encoding='utf-8')
        self.df_recursion = pd.read_csv('recommend/recursion.csv', encoding='utf-8')
        self.df_stack = pd.read_csv('recommend/stack.csv', encoding='utf-8')
        self.df_queue = pd.read_csv('recommend/queue.csv', encoding='utf-8')
        self.df_tree = pd.read_csv('recommend/tree.csv', encoding='utf-8')
        self.df_heap = pd.read_csv('recommend/priorityqueue.csv', encoding='utf-8')
        self.df_sort = pd.read_csv('recommend/sort.csv', encoding='utf-8')
        self.df_binary = pd.read_csv('recommend/binarysearch.csv', encoding='utf-8')
        self.df_graph = pd.read_csv('recommend/graph.csv', encoding='utf-8')


    def get_question(self):
        question = input("배운 내용을 입력하세요: ")
        return question


    def find_question(self, question):
        okt = Okt()
        li = okt.phrases(question)
        if question == '큐':
            li.append('큐')

        for item in li:
            if "조건" in item or "if" in item:
                return self.df_if[['number', 'title', 'problem', 'level']]

            if "반복" in item or "for" in item or "while" in item:
                return self.df_for[['number', 'title', 'problem', 'level']]

            if "배열" in item:
                return self.df_arr[['number', 'title', 'problem', 'level']]

            if "문자열" in item:
                return self.df_string[['number', 'title', 'problem', 'level']]

            if "함수" in item:
                return self.df_function[['number', 'title', 'problem', 'level']]

            if "재귀" in item or "재귀함수" in item or "재귀 함수" in item:
                return self.df_recursion[['number', 'title', 'problem', 'level']]

            if "스택" in item:
                return self.df_stack[['number', 'title', 'problem', 'level']]

            if "큐" in item:
                return self.df_queue[['number', 'title', 'problem', 'level']]

            if "트리" in item:
                return self.df_tree[['number', 'title', 'problem', 'level']]

            if "정렬" in item:
                return self.df_sort[['number', 'title', 'problem', 'level']]

            if "이진탐색" in item or "이진 탐색" in item:
                return self.df_binary[['number', 'title', 'problem', 'level']]

            if "그래프" in item:
                return self.df_graph[['number', 'title', 'problem', 'level']]


    def get_subject_name(self):
        subject_name = input("과목명을 입력하세요: ")
        return subject_name


    def find_subject(self, subject_name):
        subject_name = subject_name.lower()

        # c프로그래밍및실습
        if subject_name == 'c프로그래밍및실습' or subject_name == 'c프' or subject_name == 'c프로그래밍' or subject_name == '씨프' or subject_name == '씨프로그래밍':
            return 'c프로그래밍및실습'

        # 고급c프로그래밍및실습
        elif subject_name == '고급c프로그래밍및실습' or subject_name == '고c' or subject_name == '고급c' or subject_name == '고급c프로그래밍' or subject_name == '고씨' or subject_name == '고급씨':
            return '고급c프로그래밍및실습'

        # 자료구조및실습
        elif subject_name == '자료구조및실습' or subject_name == '자료구조' or subject_name == '자구' or subject_name == '자료구조실습':
            return '자료구조및실습'

        # 알고리즘및실습
        elif subject_name == '알고리즘및실습' or subject_name == '알고리즘' or subject_name == '알고리즘실습':
            return '알고리즘및실습'

        # 프로그래밍활용C
        elif subject_name == '프로그래밍활용C' or subject_name == '프활c':
            return '프로그래밍활용C'

        # 컴퓨터사고기반기초코딩
        elif subject_name == '컴퓨터사고기반기초코딩' or subject_name == '컴기코':
            return '컴퓨터사고기반기초코딩'

        # SW기초코딩
        elif subject_name == 'SW기초코딩':
            return 'SW기초코딩'

        # 프로그래밍활용P
        elif subject_name == '프로그래밍활용P' or subject_name == '프활P':
            return '프로그래밍활용P'

        # 고급프로그래밍활용
        elif subject_name == '고급프로그래밍활용' or subject_name == '고프활':
            return '고급프로그래밍활용'

        else:
            return None

    def get_subject(self):
        data = request.get_json()
        subject_name = data['subject_name']
        result = self.find_subject(subject_name)

        if result is not None:
            return jsonify({'subject_name': result})
        else:
            return jsonify({'error': '해당하는 과목명을 찾을 수 없습니다.'})

    def get_question(self):
        data = request.get_json()
        question = data['question']
        result_q = self.find_question(question)

        if result_q is not None:
            result_q = result_q.sort_values('level').to_dict(orient='records')
            return jsonify({'questions': result_q})
        else:
            return jsonify({'error': '해당하는 알고리즘을 찾을 수 없습니다.'})
