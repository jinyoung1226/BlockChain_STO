from queue import Queue
import heapq
from core.Order import Order


### 매매 클래스
class Exchange:
    def __init__(self, blockchain):
        self.orders = {}  # 각 토큰별 주문 저장 딕셔너리
        self.completed_transactions = Queue()  # 완료된 거래 저장 큐
        self.blockchain = blockchain  # 블록체인 객체
        self.buy_orders_heap = []  # 매수 주문을 위한 최대 힙
        self.sell_orders_heap = []  # 매도 주문을 위한 최소 힙
        
    # 주문 유형에 따라 계정 잔액 또는 토큰 수량 갱신
    def place_order(self, order, token_id):
        if order.category == 'buy':
            order.user.account_balance -= order.price * order.quantity  # 매수 주문 시 잔액 감소
        elif order.category == 'sell':
            # 매도 주문 시 토큰 수량 감소
            if token_id in order.user.num_tokens_held:
                order.user.num_tokens_held[token_id] -= order.quantity
            else:
                print("Error: Not enough tokens to sell")
                return
        # 매수 주문을 최대힙, 매도 주문을 최소 힙에 추가
        if order.category == 'buy':
            heapq.heappush(self.buy_orders_heap, (-order.price, order))
        elif order.category == 'sell':
            heapq.heappush(self.sell_orders_heap, (order.price, order))

        self.match_orders(token_id)

    
    # 매수 및 매도 주문을 생성하고 처리하는 함수
    def create_and_place_orders(self, user, token, category, price, quantity):
        order = Order(user, token.token_id, category, price, quantity)
        self.place_order(order, token.token_id)  

    # 주문 일치 처리하는 함수
    def match_orders(self, token):
        while self.buy_orders_heap and self.sell_orders_heap:
            if -self.buy_orders_heap[0][0] >= self.sell_orders_heap[0][0]:
                buy_order = heapq.heappop(self.buy_orders_heap)[1]
                sell_order = heapq.heappop(self.sell_orders_heap)[1]
                quantity = min(buy_order.quantity, sell_order.quantity)

                # 체결된 거래 처리
                completed_trade = self.execute_trade(buy_order, sell_order, quantity)
                if completed_trade:
                    self.completed_transactions.put(completed_trade)


    def execute_trade(self, buy_order, sell_order, quantity):
        # 체결된 거래 정보 생성 및 저장
        completed_trade = {
            'buy_order': [{'user': buy_order.user.user_id},{'token_id':buy_order.token_id},{'category':buy_order.category},
                         {'price': buy_order.price}, {'quantity':buy_order.quantity}], 
            'sell_order': [{'user': sell_order.user.user_id},{'token_id':sell_order.token_id},{'category':sell_order.category},
                         {'price': sell_order.price}, {'quantity':sell_order.quantity}],
            'price': sell_order.price, 
            'quantity': quantity
        }

        # 매수 주문을 한 사용자의 토큰 수량 증가
        if buy_order.category == 'buy':
            if buy_order.token_id in buy_order.user.num_tokens_held:
                buy_order.user.num_tokens_held[buy_order.token_id] += quantity
            else:
                buy_order.user.num_tokens_held[buy_order.token_id] = quantity

        # 매도 주문을 한 사용자의 계좌에서 체결된 금액만큼 감소
        if sell_order.category == 'sell':
            sell_order.user.account_balance += sell_order.price * quantity

        
        return completed_trade
    # 최저 매도 주문 가격 반환
    def get_lowest_sell_order_price(self):
        return self.sell_orders_heap[0][0] if self.sell_orders_heap else None
        
    # 최고 매수 주문 가격 반환
    def get_highest_buy_order_price(self):
        return -self.buy_orders_heap[0][0] if self.buy_orders_heap else None
    
    # 완료된 거래 목록 반환
    def create_block(self):
        transactions = []
        while not self.completed_transactions.empty() and len(transactions) < 10:
            transactions.append(self.completed_transactions.get())
        if transactions:
            self.blockchain.add_block(transactions)
    
    def get_buy_orders(self):
        """매수 주문 목록을 반환합니다."""
        return [(order[1].user.user_id, -order[0], order[1].quantity) for order in self.buy_orders_heap]

    def get_sell_orders(self):
        """매도 주문 목록을 반환합니다."""
        return [(order[1].user.user_id, order[0], order[1].quantity) for order in self.sell_orders_heap]
    
    def get_completed_transactions(self):
        """체결된 거래 목록을 반환합니다."""
        completed_transactions_list = []
        while not self.completed_transactions.empty():
            transaction = self.completed_transactions.get()
            completed_transactions_list.append(transaction)
            self.completed_transactions.put(transaction)  # 거래 정보를 다시 큐에 추가
        return completed_transactions_list
    
    def update_balance_and_tokens(self, token_id, token_amount, balance_change):
        """계좌 잔액과 토큰 수량을 업데이트합니다."""
        self.account_balance += balance_change
        self.num_tokens_held = self.num_tokens_held + token_amount