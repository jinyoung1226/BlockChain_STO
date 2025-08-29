### 주문 클래스
class Order:
    def __init__(self, user, token_id, category, price, quantity):
        self.user = user # 주문자명
        self.token_id = token_id # 주문 토큰
        self.category = category # 매수 or 매도
        self.price = price # 주문 가격
        self.quantity = quantity # 주문량
    
    # 가격 비교 메서드
    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.price == other.price