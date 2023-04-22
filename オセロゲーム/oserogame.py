import tkinter
import tkinter.messagebox
import random

board=[["None" for i in range(8)] for i in range(8)]
back=[[0 for i in range(8)] for i in range(8)]
point=[[6,2,5,4,4,5,2,6],
       [2,1,3,3,3,3,1,2],
       [5,3,3,3,3,3,3,5],
       [4,3,3,0,0,3,3,4],
       [4,3,3,0,0,3,3,4],
       [5,3,3,3,3,3,3,5],
       [2,1,3,3,3,3,1,2],
       [6,2,5,4,4,5,2,6]]
kaihou=[[0 for i in range(8)] for i in range(8)]
kaihou_kiroku=[[0 for i in range(8)] for i in range(8)]
kakutei=[]
board[3][3]="white"
board[3][4]="black"
board[4][3]="black"
board[4][4]="white"
kaihou[3][3]=5
kaihou[3][4]=5
kaihou[4][3]=5
kaihou[4][4]=5
stage="title"
turn=""
f_s=0
masu_k=4
kiroku=[]
kiroku2=[]
kati_kiroku=[]
MONTE=[100,180,180,240,240,300,300]
ban_switch=0
assist=0
level=-1
    
def kaku_hyouka(ux,uy,color):
    kaku=0
    if board[uy][ux] == color:
        if not [uy,ux] in kakutei:
            kaku+=1
            kakutei.append([uy,ux])
        plus_x=0
        plus_y=0
        for i in range(-1,2):
            for i2 in range(-1,2):
                if (i == 0 and i2 != 0) or (i2 == 0 and i != 0):
                    plus_x=0
                    plus_y=0
                    while True:
                        plus_x += i2
                        plus_y += i
                        if (ux+plus_x) < 0 or (uy+plus_y) < 0 or (ux+plus_x) >= 8 or (uy+plus_y) >= 8:
                            break
                        else:
                            if [uy+plus_y,ux+plus_x] in kakutei:
                                break
                            elif board[uy+plus_y][ux+plus_x] == color:
                                kaku += 1
                                kakutei.append([uy+plus_y,ux+plus_x])
                            else:
                                break
    return kaku

def wing(ux,uy,color):
    if board[uy][ux]=="None":
        return 0
    elif board[uy][ux]==color:
        return 2
    else:
        return 1  

def isiuti(x,y,iro,flag):
    if flag=="try" and board[y][x] != "None":
        return None
    for dy in range(-1,2):
        for dx in range(-1,2):
            sx=x
            sy=y
            count=0 
            while True:
                sx+=dx
                sy+=dy
                if sy<0 or sy>7 or sx<0 or sx>7:
                    break
                elif board[sy][sx]=="None":
                    break
                elif (iro=="black" and board[sy][sx]=="white") or (iro=="white" and board[sy][sx]=="black"):
                    count = count + 1
                elif board[sy][sx]==iro:
                    if flag=="uti":
                        for i in range(1,count+1):
                            board[sy-(i*dy)][sx-(i*dx)]=iro
                    elif flag=="try" and count != 0:
                        return "clear"
                    break

def tyu_hyouka(ux,uy,color,flag):
    """
    盤面の評価値を表示する関数
    """
    global ban_switch
    if color=="black": te_color="white"
    elif color=="white": te_color="black"
    tya=0
    tya_color=0
    tya_te_color=0
    #着手可能手数の評価
    for y in range(8):
        for x in range(8):
            if isiuti(x,y,color,"try") != None:
                tya+=1
                tya_color+=1
            if isiuti(x,y,te_color,"try") != None:
                tya-=1
                tya_te_color+=1

    #開放度の評価
    ka=0
    if ux != -1 and uy != -1:
        for i in range(-1,2):
            for i2 in range(-1,2):
                if i == 0 and i2 == 0:
                #打ったマスの開放度を算出する
                    for i3 in range(-1,2):
                        for i4 in range(-1,2):
                            if 0 <= (uy+i3) < 8 and 0 <= (ux+i4) < 8 and board[uy+i3][ux+i4] == "None" and (i3 != 0 or i4 != 0):
                                ka += 1
                    kaihou[uy][ux]=ka
                    ka=0
                #打ったマスの周囲の開放度を-1する
                else:
                    if (uy+i) < 8 and (ux+i2) < 8 and board[uy+i][ux+i2] != "None" and kaihou[uy+i][ux+i2] != 0:
                        kaihou[uy+i][ux+i2] -= 1
    kai=0
    kai_color=0
    kai_te_color=0
    for i in range(8):
        for i2 in range(8):
            if board[i][i2] == color:
                kai += kaihou[i][i2]
                kai_color += kaihou[i][i2]
            elif board[i][i2] == te_color:
                kai -= kaihou[i][i2]
                kai_te_color += kaihou[i][i2]

    #確定石の評価
    kak_color=kaku_hyouka(0,0,color)+kaku_hyouka(0,7,color)+kaku_hyouka(7,0,color)+kaku_hyouka(7,7,color)
    kak_te_color=kaku_hyouka(0,0,te_color)+kaku_hyouka(0,7,te_color)+kaku_hyouka(7,0,te_color)+kaku_hyouka(7,7,te_color)
    kak=kak_color-kak_te_color
    kakutei.clear()
    
    #ウィングの評価
    win=0
    win_color=0
    win_te_color=0
    index_1=3*(3*(3*(3*(3*(3*(3*(wing(0,0,color))+wing(0,1,color))+wing(0,2,color))+wing(0,3,color))+wing(0,4,color))+wing(0,5,color))+wing(0,6,color))+wing(0,7,color)
    index_2=3*(3*(3*(3*(3*(3*(3*(wing(0,0,color))+wing(1,0,color))+wing(2,0,color))+wing(3,0,color))+wing(4,0,color))+wing(5,0,color))+wing(6,0,color))+wing(7,0,color)
    index_3=3*(3*(3*(3*(3*(3*(3*(wing(7,0,color))+wing(7,1,color))+wing(7,2,color))+wing(7,3,color))+wing(7,4,color))+wing(7,5,color))+wing(7,6,color))+wing(7,7,color)
    index_4=3*(3*(3*(3*(3*(3*(3*(wing(0,7,color))+wing(1,7,color))+wing(2,7,color))+wing(3,7,color))+wing(4,7,color))+wing(5,7,color))+wing(6,7,color))+wing(7,7,color)
    if (index_1==2178 or index_1==726): 
        win += 1
        win_color += 1
    if (index_2==2178 or index_2==726): 
        win += 1
        win_color += 1
    if (index_3==2178 or index_3==726): 
        win += 1
        win_color += 1
    if (index_4==2178 or index_4==726): 
        win += 1
        win_color += 1
    if (index_1==1089 or index_1==363): 
        win -= 1
        win_te_color += 1
    if (index_2==1089 or index_2==363): 
        win -= 1
        win_te_color += 1
    if (index_3==1089 or index_3==363): 
        win -= 1
        win_te_color += 1
    if (index_4==1089 or index_4==363): 
        win -= 1
        win_te_color += 1
    
    #X打ちの評価
    xuti=0
    xuti_color = 0
    xuti_te_color = 0
    if board[0][0]=="None" and board[1][1]==color:
        xuti += 1
        xuti_color += 1
    if board[7][7]=="None" and board[6][6]==color:
        xuti += 1
        xuti_color += 1
    if board[0][7]=="None" and board[1][6]==color:
        xuti += 1
        xuti_color += 1
    if board[7][0]=="None" and board[6][1]==color:
        xuti += 1
        xuti_color += 1
    if board[0][0]=="None" and board[1][1]==te_color:
        xuti -= 1
        xuti_te_color += 1
    if board[7][7]=="None" and board[6][6]==te_color:
        xuti -= 1
        xuti_te_color += 1
    if board[0][7]=="None" and board[1][6]==te_color:
        xuti -= 1
        xuti_te_color += 1
    if board[7][0]=="None" and board[6][1]==te_color:
        xuti -= 1
        xuti_te_color += 1
    
    #C打ちの評価
    cuti=0
    cuti_color=0
    cuti_te_color=0
    if board[0][0]=="None" and board[0][1]==color:
        cuti += 1
        cuti_color += 1
    if board[0][0]=="None" and board[1][0]==color:
        cuti += 1
        cuti_color += 1
    if board[7][7]=="None" and board[6][7]==color:
        cuti += 1
        cuti_color += 1
    if board[7][7]=="None" and board[7][6]==color:
        cuti += 1
        cuti_color += 1
    if board[0][7]=="None" and board[1][7]==color:
        cuti += 1
        cuti_color += 1
    if board[0][7]=="None" and board[0][6]==color:
        cuti += 1
        cuti_color += 1
    if board[7][0]=="None" and board[7][1]==color:
        cuti += 1
        cuti_color += 1
    if board[7][0]=="None" and board[6][0]==color:
        cuti += 1
        cuti_color += 1
    
    if board[0][0]=="None" and board[0][1]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[0][0]=="None" and board[1][0]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[7][7]=="None" and board[6][7]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[7][7]=="None" and board[7][6]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[0][7]=="None" and board[1][7]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[0][7]=="None" and board[0][6]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[7][0]=="None" and board[7][1]==te_color:
        cuti -= 1
        cuti_te_color += 1
    if board[7][0]=="None" and board[6][0]==te_color:
        cuti -= 1
        cuti_te_color += 1

    #総合評価
    total_hyouka=(67*tya)+(-13*kai)+(101*kak)+(-308*win)+(-449*xuti)+(-552*cuti)
    if ban_switch==1:
        hyouka_lavel["text"]="盤面評価(係数)                黒　白　  黒-白　　合計点数 "
        tyakusyu_hyouka["text"]="着手可能手数の評価(67)      "+str(tya_color) +"     "+ str(tya_te_color) + "        " + str(tya) + "      "+str(67*tya)
        kaihoudo_hyouka["text"]="開放度の評価(-13)   　　   "+str(kai_color) +"   "+ str(kai_te_color) + "      " + str(kai)+"       "+str(-13*kai)
        kakutei_hyouka["text"]="確定石の評価(101)   　       "+str(kak_color) +"     "+ str(kak_te_color) + "        " + str(kak)+"      "+str(101*kak)
        wing_hyouka["text"]="ウィングの評価(-308)        "+str(win_color) +"     "+ str(win_te_color) + "        " + str(win)+"      "+str(-308*win)
        cuti_hyouka["text"]="危険なC打ちの評価(-449)   "+str(cuti_color) +"     "+ str(cuti_te_color) + "        " + str(cuti)+"      "+str(-448*cuti)
        xuti_hyouka["text"]="危険なX打ちの評価(-552)   "+str(xuti_color) +"     "+ str(xuti_te_color) + "        " + str(xuti)+"      "+str(-552*xuti)
        sougou_hyouka["text"]="総合評価    "+"                                               "+str(total_hyouka)
    else:
        hyouka_lavel["text"]=""
        tyakusyu_hyouka["text"]=""
        kaihoudo_hyouka["text"]=""
        kakutei_hyouka["text"]=""
        wing_hyouka["text"]=""
        cuti_hyouka["text"]=""
        xuti_hyouka["text"]=""
        sougou_hyouka["text"]=""
    
    if flag == "gage":
        if -2000<total_hyouka<2000:
            total_gage=(total_hyouka//200)+10
        elif total_hyouka<-2000:
            total_gage=0
        else:
            total_gage=20
        return total_gage
    
    elif flag == "hyouka":
        return total_hyouka
        
        

class hyouka_button(object):
    """
    評価関数の具体的な説明をまとめたクラス
    """
    def __init__(self):
        print("Button Press")
    def button_tya(self):
        hyouka_exp["text"] = "着手可能手数は主に、自分や相手が打てる場所を指す。\n中盤は、着手可能手数が多い程、\nその人の方が有利だと言えるよ"
    def button_kai(self):
        hyouka_exp["text"] = "開放度は石が他の石にどれくらい囲まれているかを表す。\n開放度が少ない程、その石は取られにくいから、\nなるべく開放度が少ない石を取ろう"
    def button_kak(self):
        hyouka_exp["text"] = "確定石はもう取られる事のない石を指す。\nこの石を増やしていく事で一気に勝利に近づけるよ"
    def button_win(self):
        hyouka_exp["text"] = "ウィングは辺に同じ色が5色並んだ形の事を言う\nこの形は最終的に全部取られちゃう可能性が高いから\n作らない方が良いよ"
    def button_xuti(self):
        hyouka_exp["text"] = "X打ちとは、隅の1つ斜め内側のマスに打つ事を言う\n一部例外を除いて、基本的には打たない方が良いよ"
    def button_cuti(self):
        hyouka_exp["text"] = "C打ちとは、隅の1つ隣のマスに打つ事を言う\n何も考えずにうっかり打つと、端を取られかねないよ"

def button_haijyo():
    global stage,turn
    """
    画面移動した時の処理(ステージセレクト→ゲーム画面)
    """
    if stage=="title":
        stage="teban"
        turn="PLAYER"
        start_try.place_forget()
        titlecole.place_forget()
        stage1_button.place_forget()
        stage2_button.place_forget()
        stage3_button.place_forget()
        stage4_button.place_forget()
        stage5_button.place_forget()
        banmen(10)
        senkyou_lavel = tkinter.Label(root, text="戦況ゲージ",font=("HGS創英角ﾎﾟｯﾌﾟ体",10),bg="green",fg="white")
        senkyou_lavel.place(x=770,y=120)
        jibun_lavel = tkinter.Label(root, text="自分",font=("HGS創英角ﾎﾟｯﾌﾟ体",10),bg="green",fg="white")
        jibun_lavel.place(x=770,y=200)
        teki_lavel = tkinter.Label(root, text="敵",font=("HGS創英角ﾎﾟｯﾌﾟ体",10),bg="green",fg="white")
        teki_lavel.place(x=1270,y=200)
        hyouka_switch.place(x=350, y=650)
        assist_switch.place(x=100, y=650)
        
class stage_button(object):
    """
    ステージ選択のボタンを押した時の処理をまとめたクラス
    """
    def __init__(self):
        print("stage select")
    def stage_1():
        global level
        button_haijyo()
        level=1
    def stage_2():
        global level
        button_haijyo()
        level=2
    def stage_3():
        global level
        button_haijyo()
        level=3
    def stage_4():
        global level
        button_haijyo()
        level=4
    def stage_5():
        global level
        button_haijyo()
        level=5

def button_switch():
    """
    盤面評価詳細を表示する/しないを選択する
    """
    global ban_switch
    if hyouka_switch["text"] == "盤面評価詳細表示機能ON":
        hyouka_switch["text"] = "盤面評価詳細表示機能OFF"
        hyouka_switch["bg"] = "red"
        ban_switch = 1
        tyakusyu_button.place(x=720, y=325)
        kaihou_button.place(x=720, y=350)
        kakutei_button.place(x=720, y=375)
        wing_button.place(x=720, y=400)
        cuti_button.place(x=720, y=425)
        xuti_button.place(x=720, y=450)
    elif hyouka_switch["text"] == "盤面評価詳細表示機能OFF":
        hyouka_switch["text"] = "盤面評価詳細表示機能ON"
        hyouka_switch["bg"] = "blue"
        ban_switch = 0
        tyakusyu_button.place_forget()
        kaihou_button.place_forget()
        kakutei_button.place_forget()
        wing_button.place_forget()
        cuti_button.place_forget()
        xuti_button.place_forget()

def button_assist():
    """
    アシストを表示する/しないを選択する
    """
    global assist
    if assist_switch["text"] == "アシスト表示ON":
        assist_switch["text"] = "アシスト表示OFF"
        assist_switch["bg"] = "red"
        assist = 1
    elif assist_switch["text"] == "アシスト表示OFF":
        assist_switch["text"] = "アシスト表示ON"
        assist_switch["bg"] = "blue"
        assist = 0
        
def click(e):
    """
    自分のターン時にオセロの駒を置く関数
    """
    global stage,turn,masu_k
    if stage=="teban" and 70<int(e.x)<630 and 70<int(e.y)<630:
        mx=int(e.x)//70-1
        my=int(e.y)//70-1
        if board[my][mx] == "None" and isiuti(mx,my,"black","try") != None and turn=="PLAYER":
            board[my][mx] = "black"
            masu_k += 1
            isiuti(mx,my,"black","uti")
            hyo_gage=tyu_hyouka(mx,my,"black","gage")
            turn="COMPUTER"
            banmen(hyo_gage)
            cvs.coords("P_O",70+mx*70,70+my*70,140+mx*70,140+my*70)
            root.after(500,computer_teban)
        
def banmen(hyo_gage):
    """
    オセロの盤面のUIを表示する関数
    """
    global turn,gazou_character,gazou_fukidasi,assist
    cvs.delete("all")
    cvs.create_rectangle(0,0,0,0,fill="yellow",tag="P_O")
    cvs.create_rectangle(0,0,0,0,fill="red",tag="U_O")
    for y in range(8):
        for x in range(8):
            X=70+x*70
            Y=70+y*70
            cvs.create_rectangle(X,Y,X+70,Y+70,outline="black")
    for y in range(8):
        for x in range(8):
            if board[y][x]=="black":
                cvs.create_oval(70*x+80,70*y+80,70*x+130,70*y+130,fill="black",width=0)
            elif board[y][x]=="white":
                cvs.create_oval(70*x+80,70*y+80,70*x+130,70*y+130,fill="white",width=0)
            if assist==1 and turn=="PLAYER" and isiuti(x,y,"black","try") != None:
                cvs.create_oval(70*x+80,70*y+80,70*x+130,70*y+130,outline="cyan",width=3)
            if assist==1 and turn=="COMPUTER" and isiuti(x,y,"white","try") != None:
                cvs.create_oval(70*x+80,70*y+80,70*x+130,70*y+130,outline="red",width=3)
    gazou_character=tkinter.PhotoImage(file="animai_buta.png")
    cvs.create_image(1300,650, image=gazou_character, tag="CHARA")
    gazou_fukidasi=tkinter.PhotoImage(file="fukidasi.png")
    cvs.create_image(1000,620, image=gazou_fukidasi, tag="FUKI")
    if hyo_gage != -1:
        gage=hyo_gage
        for p in range(gage):
             cvs.create_rectangle(770+25*p,150,770+25*(p+1),180,fill="blue",outline="white")
        for p in range(gage,20,1):
             cvs.create_rectangle(770+25*p,150,770+25*(p+1),180,fill="red",outline="white")

def uchiau(color):
    """
    交互に打てるマスをランダムで置く
    """
    flag=0
    while True:
        for y in range(8):
            for x in range(8):
                if isiuti(x,y,color,"try")!= None:
                    kiroku2.append([x,y])
        if len(kiroku2) != 0:
                flag=0
                a=random.randint(0,len(kiroku2)-1)
                board[kiroku2[a][1]][kiroku2[a][0]] = color
                isiuti(kiroku2[a][0],kiroku2[a][1],color,"uti")
                kiroku2.clear()
        elif len(kiroku2) == 0:
                flag += 1

        if flag == 2:
            kiroku2.clear()
            break
        
        if color=="black": 
            color="white"
        elif color=="white": 
            color="black"

def save_road(syu):
    """ 
    盤面の状況をセーブ・ロードする
    """
    for y in range(8):
        for x in range(8):
            if syu=="save":
                back[y][x] = board[y][x]
            elif syu=="road":
                board[y][x] = back[y][x]

def computer_teban():
    """
    コンピューターがどこにオセロを置くかを決める関数
    """
    global turn,masu_k,level
    kiroku.clear()
    cy=-1
    cx=-1
    flag=0
    p=0
    if level==1:
        for y in range(8):
            for x in range(8):
                if isiuti(x,y,"white","try") != None:
                    kiroku.append([y,x])
        if len(kiroku) != 0:
            u=random.randint(0,len(kiroku)-1)
            cy=kiroku[u][0]
            cx=kiroku[u][1]
            board[cy][cx] = "white"
            masu_k += 1
            isiuti(cx,cy,"white","uti")
            hyo_gage=tyu_hyouka(cx,cy,"black","gage")
            banmen(hyo_gage)
            
    elif level==2:
        for y in range(8):
            for x in range(8):
                if isiuti(x,y,"white","try") != None and point[y][x] > p:
                    cy=y
                    cx=x
                    p=point[y][x]
        if cy != -1 and cx != -1:
            board[cy][cx] = "white"
            masu_k += 1
            isiuti(cx,cy,"white","uti")
            hyo_gage=tyu_hyouka(cx,cy,"black","gage")
            banmen(hyo_gage)
            
    
    elif level==3:
        for y in range(8):
            for x in range(8):
                if isiuti(x,y,"white","try") != None:
                    kiroku.append([x,y])
        if len(kiroku) != 0:
            for i in range(len(kiroku)):
                kati_kiroku.append(0)
            for ka in range(MONTE[masu_k//10]):
                for i in range(len(kiroku)):
                    wh_c=0
                    bl_c=0
                    save_road("save")
                    cy=kiroku[i][1]
                    cx=kiroku[i][0]
                    board[cy][cx] = "white"
                    uchiau("black")
                    for i2 in range(8):
                        wh_c+=board[i2].count("white")
                        bl_c+=board[i2].count("black")
                    if wh_c > bl_c:
                        kati_kiroku[i] = int(kati_kiroku[i])+1
                    save_road("road")
        print(MONTE[masu_k//10])
        print(kati_kiroku)
        dec=kati_kiroku.index(max(kati_kiroku))
        kati_kiroku.clear()        
        masu_k+=1
        cy=kiroku[dec][1]
        cx=kiroku[dec][0]
        board[cy][cx]="white"
        isiuti(cx,cy,"white","uti")
        hyo_gage=tyu_hyouka(cx,cy,"black","gage")
        banmen(hyo_gage)
        kiroku.clear()
    
    elif level==4:
        for y in range(8):
            for x in range(8):
                if isiuti(x,y,"white","try") != None:
                    kiroku.append([y,x])
                    if (y==0 and x==0) or (y==0 and x==7) or (y==7 and x==0) or (y==7 and x==7):
                        cy=y
                        cx=x
        if cy == -1 and cx == -1 and len(kiroku) != 0:
            for i in range(len(kiroku)):
                save_road("save")
                for i2 in range(8):
                    for i3 in range(8):
                        kaihou_kiroku[i2][i3]=kaihou[i2][i3]
                board[kiroku[i][0]][kiroku[i][1]] = "white"
                isiuti(kiroku[i][1],kiroku[i][0],"white","uti")
                hyo_gage=tyu_hyouka(kiroku[i][1],kiroku[i][0],"black","hyouka")
                kati_kiroku.append(hyo_gage)
                save_road("road")
                for i2 in range(8):
                    for i3 in range(8):
                        kaihou[i2][i3]=kaihou_kiroku[i2][i3]
            dec=kati_kiroku.index(min(kati_kiroku))
            kati_kiroku.clear()
            cy=kiroku[dec][0]
            cx=kiroku[dec][1]
        masu_k+= 1
        board[cy][cx]="white"
        isiuti(cx,cy,"white","uti")
        hyo_gage=tyu_hyouka(cx,cy,"black","gage")
        banmen(hyo_gage)
        kiroku.clear()
        
    for y in range(8):
        for x in range(8):
            if isiuti(x,y,"black","try") != None:
                flag += 1
    if flag>=1:
        turn="PLAYER"
        hyo_gage=tyu_hyouka(-1,-1,"black","gage")
        banmen(hyo_gage)
        cvs.coords("U_O",70+cx*70,70+cy*70,140+cx*70,140+cy*70)
    else:
        if masu_k < 64:
            root.after(500,computer_teban)
    
    if masu_k >= 64:
        wh_c=0
        br_c=0
        for i in range(8):
            wh_c+=board[i].count("white")
        for i in range(8):
            br_c+=board[i].count("black")
        syuryou = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",24),bg="black",fg="lime")
        if wh_c > br_c:
            syuryou["text"]="白が"+str(wh_c)+"個"+",黒が"+str(br_c)+"個\n","白の勝利です"
        elif br_c > wh_c:
            syuryou["text"]="黒が"+str(br_c)+"個"+",白が"+str(wh_c)+"個\n","黒の勝利です"
        elif br_c == wh_c:
            syuryou["text"]="黒が"+str(br_c)+"個"+",白が"+str(wh_c)+"個\n","引き分けです"
        syuryou.place(x=770, y=230)
        tkinter.messagebox.showinfo("ゲーム終了","ゲームが終了しました")


if __name__=="__main__":
    root=tkinter.Tk()
    root.title("リバーシ")
    root.resizable(False,False)
    root.bind("<Button>",click)
    cvs=tkinter.Canvas(root,width=1400,height=700,bg="green")
    cvs.pack()
    titlecole = tkinter.Label(root, text="リバーシ",font=("HGS創英角ﾎﾟｯﾌﾟ体",36),bg="green",fg="black")
    titlecole.place(x=240, y=500)
    hyouka_lavel = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="black")
    hyouka_lavel.place(x=770, y=300)
    tyakusyu_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="white")
    tyakusyu_hyouka.place(x=770, y=325)
    kaihoudo_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="sky blue")
    kaihoudo_hyouka.place(x=770, y=350)
    kakutei_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="orange")
    kakutei_hyouka.place(x=770, y=375)
    wing_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="pink")
    wing_hyouka.place(x=770, y=400)
    xuti_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="gold")
    xuti_hyouka.place(x=770, y=425)
    cuti_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="green",fg="chocolate")
    cuti_hyouka.place(x=770, y=450)
    sougou_hyouka = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="white",fg="red")
    sougou_hyouka.place(x=770, y=475)
    hyouka_exp = tkinter.Label(root, text="",font=("HGS創英角ﾎﾟｯﾌﾟ体",12),bg="white",fg="black")
    hyouka_exp.place(x=800, y=580)
    start_try = tkinter.Label(root, text="ステージを選択して下さい",font=("HGS創英角ﾎﾟｯﾌﾟ体",24),bg="black",fg="lime")
    start_try.place(x=770,y=150)
    stage_btn=stage_button()
    stage1_button = tkinter.Button(root, text="STAGE1",font=("Times New Roman",16),bg="black",fg="white",command=stage_button.stage_1)
    stage2_button = tkinter.Button(root, text="STAGE2",font=("Times New Roman",16),bg="black",fg="white",command=stage_button.stage_2)
    stage3_button = tkinter.Button(root, text="STAGE3",font=("Times New Roman",16),bg="black",fg="white",command=stage_button.stage_3)
    stage4_button = tkinter.Button(root, text="STAGE4",font=("Times New Roman",16),bg="black",fg="white",command=stage_button.stage_4)
    stage5_button = tkinter.Button(root, text="STAGE5(作成予定)",font=("Times New Roman",16),bg="black",fg="white",command=stage_button.stage_5)
    stage1_button.place(x=770,y=250)
    stage2_button.place(x=770,y=325)
    stage3_button.place(x=770,y=400)
    stage4_button.place(x=770,y=475)
    stage5_button.place(x=770,y=550)
    hyouka_btn=hyouka_button()
    tyakusyu_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_tya)
    kaihou_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_kai)
    kakutei_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_kak)
    wing_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_win)
    cuti_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_xuti)
    xuti_button = tkinter.Button(root, text="解説",font=("Times New Roman",7),bg="black",fg="white",command=hyouka_btn.button_cuti)
    hyouka_switch = tkinter.Button(root, text="盤面評価詳細表示機能ON",font=("Times New Roman",15),bg="blue",fg="white",command=button_switch)
    assist_switch = tkinter.Button(root, text="アシスト表示ON",font=("Times New Roman",15),bg="blue",fg="white",command=button_assist)
    
    #タイトルロゴの作成
    for i in range(3):
        for i2 in range(3):
            if i==1 and i2 == 1:
                cvs.create_rectangle(240+i2*70,270+i*70,300+i2*70,330+i*70,fill="white",tag="T_L_W1")
            else:
                cvs.create_rectangle(240+i2*70,270+i*70,300+i2*70,330+i*70,fill="black",tag="T_L_B1")
                
    for i in range(3):
         for i2 in range(3):
             if i==1 and i2 == 1:
                 cvs.create_oval(245+i2*70,275+i*70,295+i2*70,325+i*70,fill="black",tag="T_L_W2")
             else:
                 cvs.create_oval(245+i2*70,275+i*70,295+i2*70,325+i*70,fill="white",tag="T_L_B2")
    
    oukan_logo=tkinter.PhotoImage(file="oukan.png")
    cvs.create_image(340,210, image=oukan_logo, tag="OUKAN")
    root.mainloop()
    