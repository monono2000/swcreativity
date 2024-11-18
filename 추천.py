# 패션 추천 알고리즘
class FashionRecommender:
    def __init__(self, items):
        self.items = items

    def recommend(self, user):
        # 사용자의 스타일, 색상 선호도, 착장감에 맞는 아이템 필터링
        filtered_items = [item for item in self.items
                          if user.style in item.style_tags
                          and item.color in user.color_preferences]
        
        # 필터링된 아이템 중 상위 3개 추천
        return filtered_items[:3] if filtered_items else [random.choice(self.items)]

    def recommend_outfit(self, user):
        # 사용자의 스타일에 맞는 코디 조합 추천
        outfit = []
        categories = ["상의", "하의", "신발"]

        for category in categories:
            category_items = [item for item in self.items
                              if item.category == category and user.style in item.style_tags]
            if category_items:
                outfit.append(random.choice(category_items))

        return outfit
