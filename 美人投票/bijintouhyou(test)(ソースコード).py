import random
import pygame

A=[]
B=[]
C=[]
D=[]
PLAYER=[]
COIN=[]
HAND=[]
turn=1
tokuten=10
a_c=b_c=c_c=d_c=p_c=100

def kubari():
    a=[]
    b=[]
    c=[]
    d=[]
    player=[]
    for i in range(2):
        a.append(random.randrange(0,101))
        b.append(random.randrange(0,101))
        c.append(random.randrange(0,101))
        d.append(random.randrange(0,101))
        player.append(random.randrange(0,101))
    return a,b,c,d,player

def coin_hyouji(r1,r2,r3,r4,r5):
    print("Aのコインは"+str(r1),end="  ")
    print("Bのコインは"+str(r2),end="  ")
    print("Cのコインは"+str(r3),end="  ")
    print("Dのコインは"+str(r4),end="  ")
    print("プレイヤーのコインは"+str(r5))
    print(" ")

def coin_bet_hyouji(r1,r2,r3,r4,r5):
    print("Aの賭けるコインは"+str(r1),end="  ")
    print("Bの賭けるコインは"+str(r2),end="  ")
    print("Cの賭けるコインは"+str(r3),end="  ")
    print("Dの賭けるコインは"+str(r4),end="  ")
    print("プレイヤーの賭けるコインは"+str(r5))
    print(" ")
    
def moti_hyouji(a,b,c,d,player):
    print("Aが現在所有しているカードは",end=" ")
    for i in range(len(a)):
        print(a[i],end=" ")
    print("")
    print("Bが所有しているカードは",end=" ")
    for i in range(len(b)):
        print(b[i],end=" ")
    print("")
    print("Cが所有しているカードは",end=" ")
    for i in range(len(c)):
        print(c[i],end=" ")
    print("")
    print("Dが所有しているカードは",end=" ")
    for i in range(len(d)):
        print(d[i],end=" ")
    print("")
    print("")
    print("あなたが所有しているカードは",end=" ")
    for i in range(len(player)):
        print(player[i],end=" ")
    print("です")

def dasu_hyouji(a,b,c,d,p):
    global a_c,b_c,c_c,d_c,p_c
    da_a=random.randrange(0,len(a))
    da_b=random.randrange(0,len(b))
    da_c=random.randrange(0,len(c))
    da_d=random.randrange(0,len(d))
    print("#"*20)
    print("Aが出したカードは"+str(a[da_a]))
    print("Bが出したカードは"+str(b[da_b]))
    print("Cが出したカードは"+str(c[da_c]))
    print("Dが出したカードは"+str(d[da_d]))
    print("プレイヤーが出したカードは"+str(p))
    print("A～Dの出したカード、そしてプレイヤーの出したカードを元に平均値*0.8を算出します")
    print("#"*20)
    sa=((a[da_a]+b[da_b]+c[da_c]+d[da_d]+p)/5)*0.8
    sa_m=min(abs(a[da_a]-sa),abs(b[da_b]-sa),abs(c[da_c]-sa),abs(d[da_d]-sa),abs(p-sa))
    if sa_m==abs(a[da_a]-sa):
        sa_p="A"
    elif sa_m==abs(b[da_b]-sa):
        sa_p="B"
    elif sa_m==abs(c[da_c]-sa):
        sa_p="C"
    elif sa_m==abs(d[da_d]-sa):
        sa_p="D"
    elif sa_m==abs(p-sa):
        sa_p="PLAYER"
    print("算出した結果は{}です".format(sa))
    print("{}が勝利しました".format(sa_p))
    if sa_p=="A": 
        a_c=a_c+int(COIN[0])*5
        b_c=b_c-int(COIN[1])
        c_c=c_c-int(COIN[2])
        d_c=d_c-int(COIN[3])
        p_c=p_c-int(COIN[4])
    if sa_p=="B":
        a_c=a_c-int(COIN[0])
        b_c=b_c+int(COIN[1])*5
        c_c=c_c-int(COIN[2])
        d_c=d_c-int(COIN[3])
        p_c=p_c-int(COIN[4])
    if sa_p=="C":
        a_c=a_c-int(COIN[0])
        b_c=b_c-int(COIN[1])
        c_c=c_c+int(COIN[2])*5
        d_c=d_c-int(COIN[3])
        p_c=p_c-int(COIN[4])
    if sa_p=="D":
        a_c=a_c-int(COIN[0])
        b_c=b_c-int(COIN[1])
        c_c=c_c-int(COIN[2])
        d_c=d_c+int(COIN[3])*5
        p_c=p_c-int(COIN[4])
    if sa_p=="PLAYER":
        a_c=a_c-int(COIN[0])
        b_c=b_c-int(COIN[1])
        c_c=c_c-int(COIN[2])
        d_c=d_c-int(COIN[3])
        p_c=p_c+int(COIN[4])*5

ka=0

for i in range(10):
    A,B,C,D,PLAYER=kubari()
    coin_hyouji(a_c,b_c,c_c,d_c,p_c)
    print(str(turn)+"ターン目")
    #賭けるコインを選択
    while True:
        bet_coin=int(input("賭けるコインは何枚ですか(1～100枚の中から選んでください)->"))
        if bet_coin>=1 and bet_coin<=100:
            break
        else:
            print("1～100の中で選んでください")
    for i in range(4):
        COIN.append(random.randrange(1,101))
    COIN.append(bet_coin)
    coin_bet_hyouji(COIN[0],COIN[1],COIN[2],COIN[3],COIN[4])
    turn += 1
    print(" ")
    moti_hyouji(A,B,C,D,PLAYER)
    print(" ")
    #手を考える
    for i in range(4):
        HAND.append("セット")
    while True:
        select=input("あなたの手を選択してください。セットはそのまま賭ける、ダブルは賭けを2倍にする、フォールは半分支払う代わりに賭けを降りる")
        if select=="セット" or select=="ダブル" or select=="フォール":
            HAND.append(select)
            break
        else:
            print("もう一度入力してください")
    while True:
        ka=int(input("どのカードを出しますか？->(999を入力すると強制終了)"))
        if ka == 999:
            break
        elif not ka in PLAYER:
            print("そのカードは持っていないよ、もう1度入力してね")
            continue
        else:
            dasu_hyouji(A,B,C,D,ka)
            break
    COIN.clear()
    HAND.clear()
    if ka==999:
        break