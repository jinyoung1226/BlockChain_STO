### 블록 클래스 생성
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index # 블록 인덱스
        self.previous_hash = previous_hash # 이전 해시 저장
        self.timestamp = timestamp # 타임스탬프
        self.data = data # 블록 내에 들어가는 데이터
        self.hash = hash # 현재 해시 저장