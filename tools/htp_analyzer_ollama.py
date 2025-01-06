import json
import argparse

# Import LLM model
from ollama import Client
from openai import OpenAI

from house_func import analyze_house
from tree_func import analyze_tree
from person_func import analyze_person

class HTPAnalyzer:
    """HTP (House-Tree-Person) 심리 분석을 수행하는 클래스"""
    def __init__(self, host='http://localhost:11434'):
        self.client = Client(host=host)

    def analyze_with_ollama(self, features, drawing_type):
        system_prompt = """You are a professional HTP psychologist and mental health counselor.
        Analyze both current psychological state and developmental influences through drawing features.
        Provide detailed analysis by connecting specific drawing features to psychological interpretations.
        - Use formal Korean (-습니다)
        - Do not use special characters
        - Avoid using personal pronouns or labels (e.g., 'you', 'artist', etc)
        - Only use emojis that are specifically defined in section headers
        """

        user_prompt = f"""
        === HTP Analysis Request ===
        Drawing Type: {drawing_type.upper()}
        Features Detected: {features}

        Using the bounding box coordinates [x,y,w,h], analyze the sketch and provide psychological interpretation in formal Korean.
        Translate all measurements into descriptive terms (e.g., centered, upper right, large, small):

        1. Personality Analysis:
        - Start with "1. 🔅 성격 특징 🔅"
        - Key personality traits
        - Analyze element sizes and placements from coordinates
        - Connect spatial features to personality traits
        - Interpret overall composition

        2. Social Characteristics:
        - Start with "2. 🌤️ 대인 관계 🌤️"
        - Family relationship patterns
        - Communication style
        - Interpret element spacing and relationship boundaries
        - Attachment patterns

        3. Current Mental State:
        - Start with "3. 🧘 현재 심리 상태 🧘"
        - Emotional stability
        - Developmental effects
        - Stress/anxiety levels
        - Coping mechanisms

        4. Mental Health Care:
        - Start with "4. 💪 멘탈 케어 Tips 💪"
        - Understanding past influences
        - Stress management suggestions
        - Provide practical suggestions
        - Growth potential

        Analysis guidelines:
        - Start content immediately after each section title
        - Write clear and concise paragraphs
        - Translate coordinates into descriptive terms
        - Include practical advice
        - Maintain a supportive tone
        """

        try:
            response = self.client.chat(
                model="llama3",  # Ollama에서 사용할 모델
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"분석 중 오류가 발생했습니다: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='HTP Psychological Analysis System')
    # 분석할 그림 타입 지정
    parser.add_argument('type', choices=['house', 'tree', 'person'],
                      help='Drawing type to analyze (house, tree, person)')
    args = parser.parse_args()

    # Ollama 클라이언트 초기화
    analyzer = HTPAnalyzer()

    # 그림 유형별 분석 함수 매핑
    analysis_functions = {
        'house': analyze_house,
        'tree': analyze_tree,
        'person': analyze_person
    }

    # 선택된 그림 유형의 특징 분석
    features = analysis_functions[args.type]()

    # Ollama를 사용한 심리 분석
    analysis = analyzer.analyze_with_ollama(features, args.type)

    # 분석 결과 출력
    print(f"\n=== {args.type.upper()} Drawing Analysis ===")
    print(analysis)

    return analysis

if __name__ == "__main__":
    main()
