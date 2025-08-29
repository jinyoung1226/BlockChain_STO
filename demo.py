from core.Blockchain import Blockchain
from core.Token import Token
from core.User import User
from core.Exchange import Exchange
from core.Dividend import Dividend, token_price_map


# #### 1. 제네시스 블록 생성 / 토큰 발행 / 유저 등록

# 블록체인 객체 및 genesis block 생성
blockchain = Blockchain()
blockchain.create_genesis_block()

# 토큰 정보 입력
token_id = "T001" #토큰 ID
token_name = "쏭토큰" #토큰 이름
token_price = 10 #토큰 가격
token_issuer = "박성우"  # 발행자명
underlying_asset = "쏭건물"  # 기초자산명
underlying_price = 20  # 기초자산 가격
underlying_location = "아주대학교 일신관"  # 기초자산위치

# Song_token라는 토큰 객체 생성 
Song_token = Token(token_id, token_name, token_price, token_issuer, 
                   underlying_asset, underlying_price, underlying_location)

# Song_token 발행
Song_token.token_issue_to_blockchain(blockchain)

# 토큰 정보 입력
token_id = "T002" #토큰 ID
token_name = "히지토큰" #토큰 이름
token_price = 15 #토큰 가격
token_issuer = "정희지"  # 발행자명
underlying_asset = "히지건물"  # 기초자산명
underlying_price = 25  # 기초자산 가격
underlying_location = "아주대 다산관"  # 기초자산위치

# Heeji_token라는 토큰 객체 생성
Heeji_token = Token(token_id, token_name, token_price, token_issuer, underlying_asset,
                    underlying_price, underlying_location)

# Heeji_token 발행
Heeji_token.token_issue_to_blockchain(blockchain)


# 유저 정보 입력
user_id = "U001" # 유저 ID
user_name = "박성우" # 유저 이름 
account_address = "0x123456789" # 유저 주소
account_balance = 10000 # 유저 계좌 잔고
num_tokens_held = {'T001': 20} # 유저 보유 토큰 and 토큰 수량

# Song_user라는 유저 객체 생성
Song_user = User(user_id, user_name, account_address, account_balance, num_tokens_held, blockchain = blockchain)

# Song_user 유저 등록
Song_user.user_issue_to_blockchain(blockchain)

# 유저 정보 입력
user_id = "U002" # 유저 ID
user_name = "임진영" # 유저 이름
account_address = "0x123456798" # 유저 주소
account_balance = 15000 # 유저 계좌 잔고
num_tokens_held = {'T001': 12, 'T002' : 10} # 유저 보유 토큰 and 토큰 수량

# Young_user라는 유저 객체 생성
Young_user = User(user_id, user_name, account_address, account_balance, num_tokens_held, blockchain = blockchain)

# Young_user 유저 등록
Young_user.user_issue_to_blockchain(blockchain)

# 블록체인 정보 출력
blockchain.print_blocks()


# #### 2. 토큰 매매

# 거래소 초기화
exchange = Exchange(blockchain)

# 계좌 및 토큰 확인 가능
Young_user.print_user()

Song_user.print_user()

# 매수 및 매도 주문 생성 및 처리
for i in range(10):
    exchange.create_and_place_orders(Young_user, Song_token, 'buy', 100, 2)  # 100원에 매수 주문 20개
    exchange.create_and_place_orders(Young_user, Song_token, 'buy', 50, 2) # 50원에 매수 주문 20개
    
for i in range(10):
    exchange.create_and_place_orders(Song_user, Song_token, 'sell', 70, 2) # 70원에 매도 주문 20개


# 10개의 체결 거래 블록체인에 블록 생성
exchange.create_block()

# 10개 거래 블록 생성 확인
blockchain.print_blocks()

# 계좌 및 토큰 변경 확인 
Young_user.print_user()

Song_user.print_user()


# #### 3. 배당 지급

# 베딩
# 토큰 별 배당 금액 할당
token_price_map['T001'] = 100
token_price_map['T002'] = 150

Dividend.issue_to_blockchain(blockchain, Song_user)
Dividend.issue_to_blockchain(blockchain, Young_user)

blockchain.print_blocks()