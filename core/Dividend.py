# 토큰당 배당금을 저장하는 맵 자료구조
token_price_map = {}

### 배당금 클래스
class Dividend:
    @staticmethod
    # 배당금 계산을 위해 토큰 보유량을 추출
    def calculate_dividend(num_tokens_held):
        sum = 0
        tokens = list(num_tokens_held.keys())
        print(tokens)
        print(num_tokens_held[tokens[0]])
        
        # 각 토큰에 대한 배당금 계산 (토큰 수량 * 토큰 가격)
        for i in range(len(tokens)):
            
            token_price = token_price_map[tokens[i]]
            quantity = num_tokens_held[tokens[i]]
            
            sum += quantity * token_price
            
        return sum

    @staticmethod
    def issue_to_blockchain(blockchain, user):
    
        # 사용자가 보유한 토큰에 대한 배당금 계산
        dividend_price = Dividend.calculate_dividend(user.num_tokens_held)
        
        # 배당금 정보를 거래 목록에 추가
        transactions = {"dividend": dividend_price}
        blockchain.add_block(transactions)
        # 계산된 배당금
        dividend_amount = dividend_price

        # 계좌에 배당금 전송
        user.receive_dividend(dividend_amount)
        
        # 사용자 정보를 블록체인에 업데이트
        user.user_issue_to_blockchain(blockchain)