import hashlib
import time
from core.Block import Block

### 블록체인 클래스
class Blockchain:
    def __init__(self):
        self.chain = [] # 블록을 연결할 단순 연결 리스트(이는 해시로 연결됨)
        self.users = {}  # 유저를 맵 형태로 저장 (key : UserID, value : User data)
        self.tokens = {} # 유저를 맵 형태로 저장 (key : TokenID, value : Token data)
        
    # 제네시스 블록을 생성하는 메서드
    def create_genesis_block(self):
        genesis_block = Block(0, "0", int(time.time()), "Genesis Block", self.hash_block("0")) # 제네시스 블록 생성
        self.chain.append(genesis_block) # 제네시스 블록을 블록체인에 추가

    # transaction(유저 등록, 토큰 발행, 매매, 배당)이 일어나면 블록에 추가하는 메서드
    def add_block(self, transactions):
        # 데이터 생성
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = int(time.time())
        previous_hash = previous_block.hash
        data = str(transactions)

        # 블록체인에 추가
        hash_value = self.hash_block(previous_hash + str(index) + str(timestamp) + data)
        new_block = Block(index, previous_hash, timestamp, data, hash_value)
        self.chain.append(new_block)

    # 해시 변환하는 매서드
    def hash_block(self, data): 
        return hashlib.sha256(data.encode()).hexdigest()
        
    # 블록체인 내의 전체 내용을 출력하는 함수
    def print_blocks(self): 
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print("------------------------")    
    # 블록체인 내에 발행된 토큰 정보를 출력하는 함수
    def print_tokens(self):
        for token_id, token_info in self.tokens.items():
            print(f"토큰 ID: {token_id}")
            print(token_info)
            print("------------------------")

    # Token ID를 입력하여 개별 토큰 정보를 출력하는 함수
    def search_token(self, token_id): 
        return self.tokens.get(token_id, None)