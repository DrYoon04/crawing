import random

def deal_card():
    """카드를 뽑는 함수"""
    cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]
    card = random.choice(cards)
    return card

def calculate_score(cards):
    """카드 합을 계산하는 함수"""
    # 21을 초과하면 11을 1로 변환
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, dealer_score):
    """점수를 비교하여 승패를 결정하는 함수"""
    if user_score == dealer_score:
        return "비김!"
    elif dealer_score == 0:
        return "딜러 승!"
    elif user_score == 0:
        return "플레이어 승!"
    elif user_score > 21:
        return "플레이어 버스트!"
    elif dealer_score > 21:
        return "딜러 버스트!"
    elif user_score > dealer_score:
        return "플레이어 승!"
    else:
        return "딜러 승!"

def play_game():
    """게임을 실행하는 함수"""
    print("블랙잭 게임을 시작합니다.")

    # 카드를 초기화합니다.
    user_cards = []
    dealer_cards = []

    # 시작 시 카드 2장을 각각 플레이어와 딜러에게 나눠줍니다.
    for _ in range(2):
        user_cards.append(deal_card())
        dealer_cards.append(deal_card())

    is_game_over = False

    while not is_game_over:
        # 플레이어와 딜러의 현재 카드와 점수를 출력합니다.
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(dealer_cards)
        print(f"플레이어 카드: {user_cards}, 점수: {user_score}")
        print(f"딜러 카드: {dealer_cards[0]}")

        # 플레이어가 블랙잭(21점)이거나 딜러가 블랙잭인 경우 게임 종료
        if user_score == 0 or dealer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            # 플레이어에게 카드를 더 받을지 물어봅니다.
            should_continue = input("카드를 더 받으시겠습니까? 'y' or 'n': ")
            if should_continue == 'y':
                user_cards.append(deal_card())
            else:
                is_game_over = True

    # 딜러가 16 이하일 경우 카드를 계속 뽑습니다.
    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)

    # 최종 결과를 출력합니다.
    print(f"플레이어 카드: {user_cards}, 점수: {user_score}")
    print(f"딜러 카드: {dealer_cards}, 점수: {dealer_score}")
    print(compare(user_score, dealer_score))

play_game()
