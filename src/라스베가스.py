import random
initial_money=50
goal=250
wins=0
for i in range(100):
    cash=initial_money
    while cash>0 and cash<goal:
        number=random.randint(1,2)
        if number==1:
            cash=cash+1
        else:
            cash=cash-1
    if cash==goal:wins=wins+1
    
print("초기 금액 $%d"%initial_money)
print("목표 금액 $%d"%goal)
print("100번 중에서 %d번 성공"%wins)