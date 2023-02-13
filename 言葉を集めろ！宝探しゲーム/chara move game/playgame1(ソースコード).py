#謎解きゲーム

import tkinter
import tkinter.messagebox
import random
import math
import time



px=0 #キャラクターの位置
py=0 #キャラクターの位置
tx=0 #タイトル画面に出てくる猫のx座標
ty=0 #タイトル画面に出てくる猫のy座標
e=0 #ヒントの値
hi=5 #ヒントの数
hi2=0 #ヒントを入手すると増える
ji=3 #爆弾の数
flag=flag2=flag3=flag4=0 #フラグ
hinto_x=0 #ヒントのx座標
hinto_y=0 #ヒントのy座標
jirai_x=0 #爆弾のx座標
jirai_y=0 #爆弾のy座標
index=0 #画面を切り替える際、使用する関数(0:タイトル画面　1:プレイ画面)

key="" #押したキーの変数
mouse_x="" #マウスのx座標
mouse_y="" #マウスのy座標
iti=[] #猫、ヒント、爆弾の位置をそれぞれ記録
hinto=[] #ヒントの位置
jirai=[] #爆弾の位置
hinto_k=[] #ヒントまでの距離
jirai_k=[] #爆弾までの距離
hinto2=[] #ヒントの文字の記録
hinto3=[] #ヒントの文字の記録
#単語集
tango=["でんちゅう","ちきゅうぎ","はるやすみ","ほうちょう","ゆうえんち","なつやすみ","しょうぐん","のうぎょう","かみしばい"
       ,"おべんとう","あまのがわ","いとでんわ","おとしだま","おこづかい","おとうさん","かんこうち","きのこがり","さがしもの"
       ,"こんちゅう","すべりだい","ちゅうごく","ひるごはん","べんきょう","れんきゅう","みせいねん","ゆでたまご","しんごうき"
       ,"しょうかき","ゆうじょう","ほととぎす"]
#単語集からランダムに1つ抽出し、それを正解とする
kotae=tango[random.randrange(0,30)]
print("正解:"+kotae)
kiroku=[]

def place():
    #x座標、y座標をランダムに抽出し、被らないようにする
    while True:
        x=random.randrange(0,10)
        y=random.randrange(0,7)
        #もしx座標とy座標がどちらも被った場合、再びランダムで座標を作る
        if [x,y] in iti:
            continue
        else:
            iti.append([x,y])
            break
    return x,y

def rand():
    #単語から文字をランダムに抽出する
    while True:
        x2=random.randrange(0,5)
        #もし文字が被った場合、再びランダムで文字を抽出する
        if x2 in kiroku:
            continue
        else:
            kiroku.append(x2)
            break
    return x2

def calc_distance(x1, y1, x2, y2):
    # ２点間(猫の座標から爆弾、もしくはヒントまで)の距離を求める
    diff_x = x1 - x2
    diff_y = y1 - y2
    
    return math.sqrt(diff_x**2 + diff_y**2)

def calc_saitan_distance():
    #2点間の距離から最小のものを取得する(ヒントの紙がなくなった場合、×を取得する)
    global px,py
    for i in range(hi):
        hinto_d=calc_distance(px,py,hinto[i][0],hinto[i][1])
        hinto_k.append(hinto_d)
    for i in range(3): 
        jirai_d=calc_distance(px,py,jirai[i][0],jirai[i][1])
        jirai_k.append(jirai_d)
    if len(hinto_k) == 0:
        hinto_k_h="×"
    else:
        hinto_k_h=min(hinto_k)
    jirai_k_h=min(jirai_k)
    hinto_k.clear()
    jirai_k.clear()
    return hinto_k_h,jirai_k_h

def saitan_distance_hyouji():
    #取得した最小の距離を画面に表示(×を取得した場合は、ヒントはもうないと表示する)
    #最短距離に応じてメッセージボックスの中身の文章を変える(例：爆弾が近くにある場合など)
    hinto_distance,jirai_distance=calc_saitan_distance()
    if hinto_distance == "×":
        result1 = "ヒントはもうありません"
        tak_d_game["text"]=str(result1)
    else:
        result1 = math.floor(hinto_distance * 100) / 100
        tak_d_game["text"]="ヒントまでの最短距離:"+str(result1)
            
    result2 = math.floor(jirai_distance * 100) / 100
    jir_d_game["text"]="爆弾までの最短距離:"+str(result2)
    if jirai_distance == 0:
        sup_d_game["text"]="あちゃちゃ.....爆弾に当たっちゃった......\nもう1回挑戦してみてね"
        sup_d_game["fg"]="red"
    elif hinto_distance == "×":
        sup_d_game["text"]="　　ヒントが全部集まったよ、\n　　並び替えて言葉を入力してね"
        sup_d_game["fg"]="deep skyblue"
    elif 0<hinto_distance <= 1.1 and 0<jirai_distance <= 1.1:
        sup_d_game["text"]="　　ヒントも爆弾も近くにあるよ  "
        sup_d_game["fg"]="red"
    elif 0<hinto_distance <= 1.1:
        sup_d_game["text"]="　　ヒントがすぐ近くにあるよ  "
        sup_d_game["fg"]="deep skyblue"
    elif 0<jirai_distance <= 1.1:
        sup_d_game["text"]="   　爆弾がすぐ近くにあるよ   "
        sup_d_game["fg"]="red"
    elif hinto_distance == 0:
        sup_d_game["text"]="　　ヒント発見!　いい調子だよ　"
        sup_d_game["fg"]="deep skyblue"
    else:
        sup_d_game["text"]="矢印キーで動かしてヒントを集めてね\n  (爆弾は避けて!) "
        sup_d_game["fg"]="salmon"

def key_down(e):
    #何かキーを押した際、押したキーが何なのかを取得し、変数keyに代入する
    global key
    key=e.keysym
    
def key_up(e):
    #キーを離した際、変数keyを離す
    global key
    time.sleep(0.05)
    key=""

def button_press(e):
    #マウスをクリックした際、マウスの座標を取得し、その座標に従って処理する条件を変える
    #ただし、タイトル画面とルール画面のみこの関数は処理される
    global index,mouse_x,mouse_y
    if index == 0:
        if 400 <= e.x <= 800:
            if 330 < e.y <= 410:
                mouse_y = 1
            if 410 < e.y <= 490:
                mouse_y = 2
            if 490 < e.y <= 570:
                mouse_y = 3

def button_release(e):
    #マウスを離した際、マウスの座標を空にする
    global mouse_x,mouse_y
    time.sleep(0.05)
    mouse_x,mouse_y="",""

def click_btn():
    #「答える」ボタンを押した際、正解の単語と等しい場合、クリアの処理を行う
    #違った場合は、メッセージボックスが変更される
    global gazou_gameclear1,flag2,flag3
    txt=entry.get()
    if txt == kotae:
        time.sleep(1)
        canvas.delete("MAP")
        if flag3 == 1:
            for i in range(len(hinto2)):
                hinto2[i].place_forget()
                hinto3[i].place_forget()
        canvas.delete("MYCHR")
        gazou_gameclear1=tkinter.PhotoImage(file="text_gameclear_e.png")
        canvas.create_image(400,250, image=gazou_gameclear1, tag="CLEAR")
        sup_d_game["text"]="  プレイしてくれてありがとう！"
        sup_d_game["fg"]="deep skyblue"
        flag2 += 1
        tkinter.messagebox.showinfo("おめでとう","言葉が当たりました！ゲームクリアです！")
    else:
        if not sup_d_game["text"] == "  プレイしてくれてありがとう！":
            sup_d_game["text"]="   答えが違うみたいだよ...."
            sup_d_game["fg"]="salmon"

def yarinaosi():
    #やり直しの処理(ゲームオーバーでリスタートした時の処理)
    #答え、猫の座標、ヒントと地雷の位置を全てリセットする
    global gazou_chara,map,key,px,py,flag2,kotae,hi
    fl=0
    if key == "Return" and fl == 0:
        for y in range(7):
            for x in range(10):
                if map[y][x] == 1:
                    canvas.create_rectangle(150+x*50,100+y*50,150+x*50+39,100+y*50+39, fill="snow", tag="MAP")
        kotae=tango[random.randrange(0,30)]
        print("正解:"+kotae)
        px,py=place()
        canvas.create_image(170+px*50,120+py*50, image=gazou_chara, tag="MYCHR")
        for i in range(5):
            hinto_x,hinto_y=place()
            hinto.append([hinto_x,hinto_y])
        for i in range(3):
            jirai_x,jirai_y=place()
            jirai.append([jirai_x,jirai_y])
        saitan_distance_hyouji()
        canvas.delete("OVER")
        canvas.delete("BAKUDAN")
        yari_annnnai.place_forget()
        fl=1
        flag2=0
        hi=5
        tak_k_game["text"]="ヒントの残りの数:"+str(hi)
        saitan_distance_hyouji()
        key=""
        main_proc()
    elif fl == 0:
        root.after(100,yarinaosi)
    

def main_proc():
    #スタートを押した際に動く関数　
    global px,py,flag,flag2,hi,hi2,ji,gazou_bak,hinto_distance,jirai_distance,hinto2,hinto3,flag3,gazou_gameover1,sup_d_game
    #矢印キーを押した際、猫が移動し、最短距離も算出、表示される
    if key == "Up" and py != 0:
        py=py-1
        saitan_distance_hyouji()
        flag=0
        flag2=0
    elif key == "Down" and py != 6:
        py=py+1
        saitan_distance_hyouji()
        flag=0
        flag2=0
    elif key == "Left" and px != 0:
        px=px-1
        saitan_distance_hyouji()
        flag=0
        flag2=0
    elif key == "Right" and px != 9:
        px=px+1
        saitan_distance_hyouji()
        flag=0
        flag2=0
    #ヒントの座標と猫の座標が一致した際、ヒントの文字をランダムで画面に表示　
    if [px,py] in hinto and flag == 0:
        e=rand()
        hi -= 1
        hinto2.append(tkinter.Label(root, text=kotae[e],font=("HGS創英角ﾎﾟｯﾌﾟ体",18),bg="snow",fg="skyblue"))
        hinto2[hi2].place(x=155+px*50,y=105+py*50)
        hinto3.append(tkinter.Label(root, text=kotae[e],font=("HGS創英角ﾎﾟｯﾌﾟ体",18),bg="snow",fg="salmon"))
        hinto3[hi2].place(x=1100+hi*-40,y=250)
        ba=hinto.index([px,py])
        hinto.pop(ba)
        tak_k_game["text"]="ヒントの残りの数:"+str(hi)
        flag += 1
        flag3 = 1
        hi2 += 1
        
    canvas.coords("MYCHR", 170+px*50,120+py*50)
    
    #爆弾の座標と猫の座標が一致した際、ゲームオーバー処理を行う(Enterキーを押すと、やり直し処理をスタートさせる)
    if [px,py] in jirai and flag2 == 0:
        gazou_bak=tkinter.PhotoImage(file="bakudan.png")
        canvas.create_image(170+px*50, 120+py*50, image=gazou_bak, tag="BAKUDAN")
        time.sleep(1)
        canvas.delete("MAP")
        if flag3 == 1:
            for i in range(len(hinto2)):
                hinto2[i].place_forget()
                hinto3[i].place_forget()
        canvas.delete("MYCHR")
        gazou_gameover1=tkinter.PhotoImage(file="text_gameover_e.png")
        canvas.create_image(400,250, image=gazou_gameover1, tag="OVER")
        yari_annnnai.place(x=200,y=320)
        hinto.clear()
        hinto2.clear()
        hinto3.clear()
        jirai.clear()
        iti.clear()
        kiroku.clear()
        hi2=0
        flag2 += 1
    
    if flag2 == 0:
        root.after(120,main_proc)
    else:
        yarinaosi()
        
#タイトルと画面の表示、キーとマウスの変化が起きた際、それぞれに対応した関数を処理する
root = tkinter.Tk()
root.title("宝探しゲーム")
root.resizable(False, False)
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.bind("<Button-1>", button_press)
root.bind("<ButtonRelease-1>", button_release)

canvas=tkinter.Canvas(root, width=1200, height=600, bg="snow")
canvas.pack()

#ゲームのUI画面の部品
gazou_titlehaikei=tkinter.PhotoImage(file="title capcha.png")
canvas.create_image(600,300, image=gazou_titlehaikei, tag="TITLE")
gazou_titleface=tkinter.PhotoImage(file="catsiro.png")
canvas.create_image(450,370, image=gazou_titleface, tag="FACE")
gazou_rulu_haikei=tkinter.PhotoImage(file="cat_rulu2.png")
gazou_rulu_sousa=tkinter.PhotoImage(file="cat_sousa.png")
rulu_sousa = tkinter.Label(root, text="マウスをクリックするか、Enterキーを押して次の画面へ",
                           font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
title_annnnai = tkinter.Label(root, text="マウスをクリックするか、上下の矢印キーで猫を動かしてEnterキーを押してね",
                              font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
title_annnnai.place(x=250,y=570)
yari_annnnai = tkinter.Label(root, text="Enterキーでやり直せるよ",font=("HGS創英角ﾎﾟｯﾌﾟ体",24),bg="snow",fg="salmon")
sup_d_game = tkinter.Label(root, text="矢印キーで動かしてヒントを集めてね\n  (爆弾は避けて!) ",font=("HGS創英角ﾎﾟｯﾌﾟ体",11),
                           bg="white",fg="salmon")

def game_main():
    global index,key,tx,ty,tak_d_game,jir_d_game,tak_k_game,px,py,flag4,map,mouse_y
    global gazou_titlehaikei,gazou_titleface,gazou_haikei,gazou_cat_mu,gazou_fuk,gazou_chara,entry,gazou_rulu_haikei
    #タイトル画面の処理(マウスの操作、キーボードの操作によって、スタート、ルール説明、終了、それぞれの処理を行う)
    if index == 0:
        if key == "Up" and ty != 0:
            ty=ty-1
            tx=tx+1
            canvas.coords("FACE",450+tx*60,370+ty*80)
        if key == "Down" and ty != 2:
            ty=ty+1
            tx=tx-1
            canvas.coords("FACE",450+tx*60,370+ty*80)
        if  (key == "Return" and flag4 == 0) or (mouse_y != "" and flag4 == 0):
            title_annnnai.place_forget()
            if (mouse_y == "" and ty == 0) or mouse_y == 1:
                index += 1
                canvas.delete("TITLE")
                canvas.delete("FACE")
            if (mouse_y== "" and ty == 1) or mouse_y == 2:
                canvas.delete("TITLE")
                canvas.delete("FACE")
                canvas.create_image(600,300, image=gazou_rulu_haikei, tag="RULE")
                rulu_sousa.place(x=300,y=550)
                flag4 = 1
                key =""
                mouse_y = ""
            if (mouse_y == "" and ty == 2) or mouse_y == 3:
                root.destroy()
        if  (key == "Return" and flag4 == 1) or (mouse_y != "" and flag4 == 1):
            canvas.delete("RULE")
            canvas.create_image(600,300, image=gazou_rulu_sousa, tag="SOUSA")
            flag4 = 2
            key =""
            mouse_y = ""
        if  (key == "Return" and flag4 == 2) or (mouse_y != "" and flag4 == 2):
            canvas.delete("SOUSA")
            gazou_titlehaikei=tkinter.PhotoImage(file="title capcha.png")
            canvas.create_image(600,300, image=gazou_titlehaikei, tag="TITLE")
            gazou_titleface=tkinter.PhotoImage(file="catsiro.png")
            canvas.create_image(450,370, image=gazou_titleface, tag="FACE")
            rulu_sousa.place_forget()
            title_annnnai.place(x=250,y=570)
            ty=0
            tx=0
            key=" "
            mouse_y = ""
            flag4 = 0
        root.after(100,game_main)
                
    elif index == 1:
        #スタートを押した際の処理(タイトル画面の消去とﾌﾟレイ画面の表示、ヒントの位置、爆弾の位置、猫の位置をランダムで決める)
        gazou_haikei=tkinter.PhotoImage(file="cat_haikei.png")
        canvas.create_image(600,300, image=gazou_haikei, tag="HAIKEI")
        title_game = tkinter.Label(root, text="言葉を当てろ!宝探しゲーム",font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        stage_game = tkinter.Label(root, text="STAGE1",font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        res_d_game = tkinter.Label(root, text="言葉のヒント:",font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        kot_d_game = tkinter.Label(root, text="答え:",font=("HGS創英角ﾎﾟｯﾌﾟ体",20),bg="snow",fg="salmon")
        tak_k_game = tkinter.Label(root, text="ヒントの残りの数:"+str(hi),font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        jir_k_game = tkinter.Label(root, text="爆弾の数:"+str(ji),font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        gazou_cat_mu=tkinter.PhotoImage(file="cat_mu.png")
        gazou_fuk=tkinter.PhotoImage(file="fukidasi.png")
        title_game.place(x=750, y=50)
        stage_game.place(x=1050, y=50)
        res_d_game.place(x=800, y=250)
        kot_d_game.place(x=100, y=500)
        tak_k_game.place(x=150, y=50)
        jir_k_game.place(x=450, y=50)
        canvas.create_image(1050,500, image=gazou_cat_mu, tag="CATMU")
        canvas.create_image(850,400, image=gazou_fuk, tag="FUKIDASI")
        entry=tkinter.Entry(width=50)
        entry.place(x=200, y=510)
        button = tkinter.Button(root, text="答える",font=("Times New Roman",12),bg="skyblue",fg="white",command=click_btn)
        button.place(x=550, y=500)
        sup_d_game.place(x=720, y=380)

        map=[[1 for i in range(10)] for j in range(7)]
        for y in range(7):
            for x in range(10):
                if map[y][x] == 1:
                    canvas.create_rectangle(150+x*50,100+y*50,150+x*50+39,100+y*50+39, fill="snow", tag="MAP")

        gazou_chara=tkinter.PhotoImage(file="cat2.png")
        px,py=place()
        canvas.create_image(170+px*50,120+py*50, image=gazou_chara, tag="MYCHR")

        for i in range(5):
            hinto_x,hinto_y=place()
            hinto.append([hinto_x,hinto_y])
        for i in range(3):
            jirai_x,jirai_y=place()
            jirai.append([jirai_x,jirai_y])

        hinto_distance,jirai_distance=calc_saitan_distance()
        RESULT1 = math.floor(hinto_distance * 100) / 100
        RESULT2 = math.floor(jirai_distance * 100) / 100
        tak_d_game = tkinter.Label(root, text="ヒントまでの最短距離:"+str(RESULT1),font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        jir_d_game = tkinter.Label(root, text="爆弾までの最短距離:"+str(RESULT2),font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="salmon")
        tak_d_game.place(x=800, y=150)
        jir_d_game.place(x=800, y=200)

        main_proc()

game_main()
root.mainloop()