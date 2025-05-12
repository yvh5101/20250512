from flask import Flask, render_template, request, jsonify
import requests
import json
import random

app = Flask(__name__)

# 외부 API를 통해 단어 어원 정보를 가져오는 함수
def get_etymology(word):
    # 실제 API가 있다면 여기서 호출하여 사용
    # 예시 데이터로 대체
    etymologies = {
        "hello": {
            "origin": "고대 영어 'hāl' (건강한, 온전한)에서 유래",
            "history": "고대 영어 'hāl'에서 중세 영어 'hail'로 변화했으며, 이후 'hello'로 발전했습니다.",
            "related_words": ["hail", "health", "whole"]
        },
        "apple": {
            "origin": "고대 영어 'æppel'에서 유래",
            "history": "인도유럽어 'ab(e)l' (과일)에서 파생되었으며, 고대 색슨어, 고대 노르드어를 거쳐 현대 영어로 발전했습니다.",
            "related_words": ["applesauce", "pineapple", "crabapple"]
        },
        "computer": {
            "origin": "라틴어 'computare' (계산하다)에서 유래",
            "history": "라틴어 'com' (함께) + 'putare' (생각하다)에서 파생되어 '계산하다'라는 의미의 동사가 되었고, 이후 계산 기계를 의미하는 명사로 발전했습니다.",
            "related_words": ["compute", "computation", "computerize"]
        },
        "book": {
            "origin": "고대 영어 'bōc'에서 유래",
            "history": "게르만어 'bokiz'에서 파생되었으며, 처음에는 '너도밤나무'를 의미했다가 나무 껍질에 글자를 새기는 관습에서 '책'의 의미로 발전했습니다.",
            "related_words": ["booklet", "bookish", "bookend"]
        },
        "garden": {
            "origin": "앵글로-노르만어 'gardin'에서 유래",
            "history": "고대 프랑크어 '*gardo' (울타리, 정원)에서 발전했으며, 이는 인도유럽어 'ghor-dho' (울타리 친 장소)에서 파생되었습니다.",
            "related_words": ["yard", "kindergarten", "orchard"]
        },
        "school": {
            "origin": "그리스어 'scholē' (여가, 토론, 강의)에서 유래",
            "history": "원래 '여가 시간' 또는 '휴식'을 의미했으나 점차 '학문적 토론이나 강의를 위한 시간'으로 의미가 바뀌었고, 이후 교육 기관을 가리키게 되었습니다.",
            "related_words": ["scholar", "scholastic", "preschool"]
        },
        "paper": {
            "origin": "고대 이집트의 파피루스(papyrus)에서 유래",
            "history": "파피루스 식물로 만든 고대 필기 재료에서 이름이 파생되었으며, 라틴어 'papyrus'를 거쳐 중세 영어 'papir'로, 그리고 현대 영어 'paper'로 발전했습니다.",
            "related_words": ["paperback", "newspaper", "paperwork"]
        },
        "window": {
            "origin": "고대 노르드어 'vindauga' (바람의 눈)에서 유래",
            "history": "'바람(wind)'과 '눈(eye)'의 합성어로, 초기 건물에서 바람이 들어오는 구멍을 의미했습니다. 이후 현대적인 창문의 개념으로 발전했습니다.",
            "related_words": ["windowed", "windowsill", "windowpane"]
        },
        "salary": {
            "origin": "라틴어 'salarium' (소금값)에서 유래",
            "history": "고대 로마 시대에 군인들에게 소금을 사기 위한 수당으로 지급된 돈에서 유래했습니다. 소금은 당시 매우 중요한 보존제였습니다.",
            "related_words": ["sale", "saline", "salad"]
        },
        "panic": {
            "origin": "그리스 신화의 판(Pan) 신에서 유래",
            "history": "산과 숲의 신인 판(Pan)이 갑작스럽게 나타나 공포를 일으킨다는 그리스 신화에서 유래했습니다. 판은 종종 사람들을 놀라게 해 공포에 질리게 했다고 합니다.",
            "related_words": ["pandemonium", "pandemic", "panicky"]
        }
    }
    
    if word.lower() in etymologies:
        return etymologies[word.lower()]
    else:
        return None

# 퀴즈 문제 생성 함수
def generate_quiz():
    etymologies = {
        "hello": {
            "origin": "고대 영어 'hāl' (건강한, 온전한)에서 유래",
            "history": "고대 영어 'hāl'에서 중세 영어 'hail'로 변화했으며, 이후 'hello'로 발전했습니다.",
        },
        "apple": {
            "origin": "고대 영어 'æppel'에서 유래",
            "history": "인도유럽어 'ab(e)l' (과일)에서 파생되었으며, 고대 색슨어, 고대 노르드어를 거쳐 현대 영어로 발전했습니다.",
        },
        "computer": {
            "origin": "라틴어 'computare' (계산하다)에서 유래",
            "history": "라틴어 'com' (함께) + 'putare' (생각하다)에서 파생되어 '계산하다'라는 의미의 동사가 되었고, 이후 계산 기계를 의미하는 명사로 발전했습니다.",
        },
        "book": {
            "origin": "고대 영어 'bōc'에서 유래",
            "history": "게르만어 'bokiz'에서 파생되었으며, 처음에는 '너도밤나무'를 의미했다가 나무 껍질에 글자를 새기는 관습에서 '책'의 의미로 발전했습니다.",
        },
        "garden": {
            "origin": "앵글로-노르만어 'gardin'에서 유래",
            "history": "고대 프랑크어 '*gardo' (울타리, 정원)에서 발전했으며, 이는 인도유럽어 'ghor-dho' (울타리 친 장소)에서 파생되었습니다.",
        },
        "school": {
            "origin": "그리스어 'scholē' (여가, 토론, 강의)에서 유래",
            "history": "원래 '여가 시간' 또는 '휴식'을 의미했으나 점차 '학문적 토론이나 강의를 위한 시간'으로 의미가 바뀌었고, 이후 교육 기관을 가리키게 되었습니다.",
        },
        "paper": {
            "origin": "고대 이집트의 파피루스(papyrus)에서 유래",
            "history": "파피루스 식물로 만든 고대 필기 재료에서 이름이 파생되었으며, 라틴어 'papyrus'를 거쳐 중세 영어 'papir'로, 그리고 현대 영어 'paper'로 발전했습니다.",
        },
        "window": {
            "origin": "고대 노르드어 'vindauga' (바람의 눈)에서 유래",
            "history": "'바람(wind)'과 '눈(eye)'의 합성어로, 초기 건물에서 바람이 들어오는 구멍을 의미했습니다. 이후 현대적인 창문의 개념으로 발전했습니다.",
        },
        "salary": {
            "origin": "라틴어 'salarium' (소금값)에서 유래", 
            "history": "고대 로마 시대에 군인들에게 소금을 사기 위한 수당으로 지급된 돈에서 유래했습니다. 소금은 당시 매우 중요한 보존제였습니다.",
        },
        "panic": {
            "origin": "그리스 신화의 판(Pan) 신에서 유래",
            "history": "산과 숲의 신인 판(Pan)이 갑작스럽게 나타나 공포를 일으킨다는 그리스 신화에서 유래했습니다. 판은 종종 사람들을 놀라게 해 공포에 질리게 했다고 합니다.",
        }
    }
    
    # 무작위로 단어 선택
    word_list = list(etymologies.keys())
    correct_word = random.choice(word_list)
    
    # 오답 선택지 생성 (3개)
    wrong_words = random.sample([w for w in word_list if w != correct_word], 3)
    
    # 선택지 섞기
    options = [correct_word] + wrong_words
    random.shuffle(options)
    
    # 정답 인덱스 찾기
    correct_index = options.index(correct_word)
    
    return {
        "question": f"다음 어원 설명에 해당하는 단어는 무엇일까요?\n\n{etymologies[correct_word]['origin']}\n{etymologies[correct_word]['history']}", 
        "options": options,
        "correct_answer": correct_word,
        "correct_index": correct_index
    }

@app.route('/')
def index():
    return render_template('etymology_index.html')

@app.route('/search')
def search():
    word = request.args.get('word', '')
    etymology_data = get_etymology(word)
    
    if etymology_data:
        return jsonify({
            "success": True,
            "word": word,
            "data": etymology_data
        })
    else:
        return jsonify({
            "success": False,
            "message": "해당 단어의 어원 정보를 찾을 수 없습니다."
        })

@app.route('/quiz')
def quiz():
    return render_template('etymology_quiz.html')

@app.route('/get_quiz')
def get_quiz():
    quiz_data = generate_quiz()
    return jsonify(quiz_data)

if __name__ == '__main__':
    app.run(debug=True) 