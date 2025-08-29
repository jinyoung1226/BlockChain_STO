### 토큰 클래스
class Token:
    def __init__(self, token_id, name, price, issuer, underlying_asset, underlying_price, underlying_location):
        self.token_id = token_id # 토큰 아이디
        self.name = name # 토큰명
        self.price = price # 초기 가격
        self.issuer = issuer # 발행자
        self.underlying_asset = underlying_asset # 기초자산 정보
        self.underlying_price = underlying_price # 기초자산 가격
        self.underlying_location = underlying_location # 기초자산 위치

    # 맵 자료구조 변환 메서드
    def to_dict(self):
        return {
            "token_id": self.token_id,
            "name": self.name,
            "price": self.price,
            "issuer": self.issuer,
            "underlying_asset": self.underlying_asset,
            "underlying_price": self.underlying_price,
            "underlying_location": self.underlying_location
        }

    # 토큰 발행 메서드
    def token_issue_to_blockchain(self, blockchain):
        token_data = self.to_dict() # 맵 자료구조로 변환
        blockchain.tokens[self.token_id] = token_data # Key를 TokenID로 설정
        blockchain.add_block(token_data) # 블록체인에 추가