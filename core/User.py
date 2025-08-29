### 유저 클래스
class User:
    def __init__(self, user_id, name, account_address, account_balance, num_tokens_held, blockchain):
        self.user_id = user_id # 유저 아이디
        self.name = name # 유저명
        self.account_address = account_address # 계좌 주소
        self.account_balance = account_balance # 계좌 잔고
        self.num_tokens_held = num_tokens_held # 보유 토큰 개수
        self.blockchain = blockchain

    # 맵 자료구조로 변환 메서드
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "account_address": self.account_address,
            "account_balance": self.account_balance,
            "num_tokens_held": self.num_tokens_held
        }

    # 유저 등록 메서드
    def user_issue_to_blockchain(self, blockchain):
        user_data = self.to_dict() # 맵 자료구조로 변환
        blockchain.users[self.user_id] = user_data # Key를 UserID를 설정
        blockchain.add_block(user_data)  # 블록체인에 추가

    # 유저 정보 출력 메서드
    def print_user(self):
        print(f"User ID: {self.user_id}")
        print(f"User Name: {self.name}")
        print(f"Account Address: {self.account_address}")
        print(f"Account Balance: {self.account_balance}")
        print(f"Number of Tokens Held: {self.num_tokens_held}")
        print("------------------------")
    # 배당금 전송 메서드
    def receive_dividend(self, amount):
        self.account_balance += amount
        print(f"Received dividend: {amount} won. New account balance: {self.account_balance} won.")