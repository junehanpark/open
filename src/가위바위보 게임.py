import tkinter as tk
from tkinter import simpledialog, messagebox, Checkbutton, IntVar, ttk
import json
import os
import random

class ClothingSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("의류 선택기")
        self.master.geometry("400x800")
        self.master.configure(bg='#F5F5DC')  # 연한 베이지 색상
        self.recommender = ClothingRecommender()
        
        self.create_widgets()

    def create_widgets(self):
        row = 0
        tk.Label(self.master, text="의류 선택기", font=("Arial", 24), bg='#F5F5DC').grid(row=row, columnspan=2, pady=20)
        
        row += 1
        tk.Label(self.master, text="상의 종류 선택:", font=("Arial", 14), bg='#F5F5DC').grid(row=row, sticky=tk.W, padx=20)
        self.top_vars = {"반소매": IntVar(), "긴소매": IntVar()}
        row += 1
        for top_type, var in self.top_vars.items():
            Checkbutton(self.master, text=top_type, variable=var, font=("Arial", 12), bg='#F5F5DC').grid(row=row, sticky=tk.W, padx=40)
            row += 1

        tk.Label(self.master, text="하의 종류 선택:", font=("Arial", 14), bg='#F5F5DC').grid(row=row, sticky=tk.W, padx=20)
        self.bottom_vars = {"긴바지": IntVar(), "반바지": IntVar()}
        row += 1
        for bottom_type, var in self.bottom_vars.items():
            Checkbutton(self.master, text=bottom_type, variable=var, font=("Arial", 12), bg='#F5F5DC').grid(row=row, sticky=tk.W, padx=40)
            row += 1

        row += 1
        style = ttk.Style()
        style.configure('TButton', foreground='#8B4513')  # 버튼 글자 색상 갈색
        ttk.Button(self.master, text="제출", command=self.submit).grid(row=row, sticky=tk.W, padx=20, pady=10)
        ttk.Button(self.master, text="코디 추천 받기", command=self.show_recommendation_button).grid(row=row, column=1, sticky=tk.W, pady=10)
        row += 1
        ttk.Button(self.master, text="데이터 초기화", command=self.reset_data).grid(row=row, sticky=tk.W, padx=20, pady=10)

    def submit(self):
        selected_options = {
            'top': {key: var.get() for key, var in self.top_vars.items() if var.get()},
            'bottom': {key: var.get() for key, var in self.bottom_vars.items() if var.get()}
        }
        self.recommender.collect_data(selected_options)
        messagebox.showinfo("저장 완료", "옷의 세부 사항이 성공적으로 저장되었습니다.")
        self.create_widgets()

    def show_recommendation_button(self):
        total_items = self.recommender.count_items()
        messagebox.showinfo("저장된 옷 개수", f"총 저장된 옷의 수: {total_items}")
        self.get_recommendation_inputs()

    def get_recommendation_inputs(self):
        temperature = simpledialog.askinteger("입력", "온도를 입력하세요:")
        keyword = simpledialog.askstring("입력", "키워드(색상 또는 스타일)를 입력하세요:")
        self.recommender.recommend_clothes(temperature, keyword)

    def reset_data(self):
        self.recommender.reset_data()
        messagebox.showinfo("초기화 완료", "모든 데이터가 초기화되었습니다.")

class ClothingRecommender:
    def __init__(self):
        self.clothes = {'top': {}, 'bottom': {}}
        self.load_data()

    def load_data(self):
        if os.path.exists('clothes_data.json'):
            with open('clothes_data.json', 'r', encoding='utf-8') as file:
                self.clothes = json.load(file)

    def save_data(self):
        with open('clothes_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.clothes, file, ensure_ascii=False, indent=4)

    def reset_data(self):
        self.clothes = {'top': {}, 'bottom': {}}
        self.save_data()

    def collect_data(self, selected_options):
        for category, types in selected_options.items():
            for type, is_selected in types.items():
                if is_selected:
                    item_name, item_details = self.ask_question_gui(category, type)
                    self.clothes[category][item_name] = item_details
        self.save_data()

    def ask_question_gui(self, category, type):
        item_details = {}
        questions = self.get_questions(category, type)
        for question, options in questions:
            answer = simpledialog.askstring("Input", f"{question} ({', '.join(options)}): ")
            item_details[question] = answer
            if question == "니트인가?" and answer == "예":
                item_details["옷 종류"] = "니트"
            elif question == "맨투맨인가?" and answer == "예":
                item_details["옷 종류"] = "맨투맨"
            elif question == "어떤 스타일인가요?" and answer in options:
                item_details["옷 종류"] = answer
        item_name = simpledialog.askstring("입력", f"이 {category} 항목의 이름을 입력하세요 (예: 상의1, 바지1): ")
        item_details['이름'] = item_name
        item_details['종류'] = type
        return item_name, item_details

    def get_questions(self, category, type):
        questions = {
            'top': {
                '반소매': [
                    ("무슨 핏인가요?", ["오버핏", "레귤러핏"]),
                    ("카라가 있나요?", ["예", "아니오"]),
                    ("무늬가 있나요?", ["예", "아니오"]),
                    ("색깔이 무엇인가요?", ["버건디", "네이비", "블루", "화이트", "아이보리", "블랙", "그레이", "퍼플", "그린", "옐로우", "브라운", "베이지", "핑크"])
                ],
                '긴소매': [
                    ("이너인가요 아니면 아우터인가요?", ["이너", "아우터"]),
                ]
            },
            'bottom': {
                '긴바지': [
                    ("바지 종류가 무엇인가요?", ["조거팬츠", "스웨트팬츠", "청바지", "슬랙스", "카고팬츠", "면바지"]),
                    ("무슨 핏인가요?", ["레귤러핏", "와이드핏"]),
                    ("색깔이 무엇인가요?", ["버건디", "네이비", "블루", "화이트", "아이보리", "블랙", "그레이", "퍼플", "그린", "옐로우", "브라운", "베이지", "핑크"])
                ],
                '반바지': [
                    ("바지 종류가 무엇인가요?", ["스웨트팬츠", "면바지", "카고바지", "청바지"]),
                    ("색깔이 무엇인가요?", ["버건디", "네이비", "블루", "화이트", "아이보리", "블랙", "그레이", "퍼플", "그린", "옐로우", "브라운", "베이지", "핑크"])
                ]
            }
        }
        if type == '긴소매':
            inner_or_outer = simpledialog.askstring("Input", "이너인가요 아니면 아우터인가요? (이너/아우터): ")
            if inner_or_outer == "아우터":
                return [
                    ("어떤 스타일인가요?", ["패딩", "자켓", "가죽", "후리스", "코트"]),
                    ("색깔이 무엇인가요?", ["버건디", "네이비", "블루", "화이트", "아이보리", "블랙", "그레이", "퍼플", "그린", "옐로우", "브라운", "베이지", "핑크"])
                ]
            else:
                return [
                    ("니트인가?", ["예", "아니오"]),
                    ("카라가 있나요?", ["예", "아니오"]),
                    ("맨투맨인가?", ["예", "아니오"]),
                    ("무늬가 있는가?", ["예", "아니오"]),
                    ("색깔이 무엇인가요?", ["버건디", "네이비", "블루", "화이트", "아이보리", "블랙", "그레이", "퍼플", "그린", "옐로우", "브라운", "베이지", "핑크"])
                ]
        return questions[category][type] if type in questions[category] else []

    def recommend_clothes(self, temperature, keyword):
        top_recommendations = []
        bottom_recommendations = []
        bottom_colors = {
            '화이트': ['청바지', '베이지', '그레이'],
            '네이비': ['블루', '베이지', '그레이', '버건디'],
            '핑크': ['청바지', '블랙', '그레이'],
            '옐로우': ['네이비', '그레이', '블랙'],
            '블루': ['화이트', '베이지'],
            '그린': ['블루 청바지', '베이지', '아이보리', '화이트'],
            '아이보리': ['청바지', '카키', '버건디', '블랙'],
            '버건디': ['블루 청바지', '블랙', '베이지', '아이보리'],
            '베이지': ['브라운', '네이비', '그레이'],
            '브라운': ['아이보리', '베이지', '블랙', '화이트'],
            '그레이': ['블랙', '네이비', '블루'],
            '블랙': ['그레이', '화이트', '블루']
        }

        # 추천 로직 구현
        for category, items in self.clothes.items():
            if category == 'top':
                for item_name, details in items.items():
                    color = details["색깔이 무엇인가요?"]
                    if keyword in details.get("옷 종류", ""):
                        if temperature < 18 and details['종류'] == '긴소매':
                            if '코트' in keyword and ('아이보리' in keyword or '화이트' in keyword):
                                top_recommendations.append(details)
                            elif '가죽' in keyword and '긴소매' in details['종류']:
                                top_recommendations.append(details)
                            elif '니트' in details.get("옷 종류", ""):
                                top_recommendations.append(details)
                            elif '맨투맨' in details.get("옷 종류", ""):
                                top_recommendations.append(details)
                        elif temperature >= 18 and details['종류'] == '반소매':
                            top_recommendations.append(details)

        # 긴소매 추천 시 하의 색상 결정 로직
        if temperature < 18 and '코트' in keyword and ('아이보리' in keyword or '화이트' in keyword):
            possible_bottoms = ['청바지', '슬랙스', '면바지']
        elif temperature < 18 and '가죽' in keyword:
            possible_bottoms = ['청바지', '면바지']
        else:
            if top_recommendations:
                top_color = top_recommendations[0]["색깔이 무엇인가요?"]
                possible_bottoms = bottom_colors.get(top_color, [])

        if top_recommendations and possible_bottoms:
            selected_bottom_color = random.choice(possible_bottoms)
            matching_bottoms = [details for bottom_name, details in self.clothes['bottom'].items() if details["색깔이 무엇인가요?"] in selected_bottom_color]
            if matching_bottoms:
                bottom_recommendations.append(random.choice(matching_bottoms))

        def format_details(details):
            return ", ".join([f"{key}: {value}" for key, value in details.items()])

        top_recommendation_text = "\n".join([f"{details['이름']} (종류: {details['종류']}), {format_details(details)}" for details in top_recommendations])
        bottom_recommendation_text = "\n".join([f"{details['이름']} (종류: {details['종류']}), {format_details(details)}" for details in bottom_recommendations])
        recommendation_text = f"추천 상의:\n{top_recommendation_text}\n추천 하의:\n{bottom_recommendation_text}"
        messagebox.showinfo("코디 추천", recommendation_text if top_recommendations and bottom_recommendations else "추천할 옷이 없습니다.")

    def count_items(self):
        return sum(len(items) for items in self.clothes.values())

if __name__ == "__main__":
    root = tk.Tk()
    app = ClothingSelector(root)
    root.mainloop()
