import tkinter
import tkinter.messagebox
import random
import time

masu=[[0 for _ in range(5)] for _ in range(5)]
masu_r=[]
sh=0
kati=0
sy=0
sen=""
se="P"

def masume(p1):
    global title,rulu,sen,sh,se
    cvs.delete("all")
    cvs.create_image(500,350, image=gazou_titlehaikei, tag="HAIKEI")
    if sen == "C":
        a=random.randint(1,3)
        b=random.randint(1,3)
        masu[a][b]=2
        sh=sh+1
        se="C"
        sen=""
    if sen == "P":
        se="P"
        sen=""
    for i in range(0,6):
        p1.create_line(100+100*i, 100, 100+100*i, 600, fill="gray" ,width=8)
        p1.create_line(100, 100+i*100, 600, 100+i*100, fill="gray" ,width=8)
    for y in range(5):
        for x in range(5):
            if masu[y][x] == 1:
                p1.create_oval(120+100*x,120+100*y,180+100*x,180+100*y, outline="red", width=12)
            if masu[y][x] == 2:
                p1.create_line(120+100*x,120+100*y,180+100*x,180+100*y, fill="snow", width=12)
                p1.create_line(180+100*x,120+100*y,120+100*x,180+100*y, fill="snow", width=12)
    cvs.update()
                
def click(e):
    global cvs,sh,se
    if 100<=int(e.x)<=600 and 100<=int(e.y)<600 and ((se=="P" and sh % 2 == 0) or (se=="C" and sh % 2 == 1)):
        mx=(int(e.x)-100)//100
        my=(int(e.y)-100)//100
        if masu[my][mx] == 0:
            sh=sh+1
            masu[my][mx]=1
            masume(cvs)
            time.sleep(0.5)
            hantei(4)
            syouhai()
            if sh < 25 and sy == 0:
                computer()
                masume(cvs)
                time.sleep(0.5)
                hantei(4)
                syouhai()

def click_btn():
    global cvs,sen,sy,masu
    if masu==[[0 for _ in range(5)] for _ in range(5)]:
        sy=0
        sen="P"
        masume(cvs)

def click_btn2():
    global cvs,sen,sy,masu
    if masu==[[0 for _ in range(5)] for _ in range(5)]:
        sy=0
        sen="C"
        masume(cvs)

def click_btn3():
    global cvs,sen,sy,masu
    if masu==[[0 for _ in range(5)] for _ in range(5)]:
        sy=0
        r=random.randint(1,2)
        if r == 1:
            sen="P"
        elif r == 2:
            sen="C"
        masume(cvs)
        
    

def computer():
    global cvs,sh,kati
    #3つ×が置いてあった時
    for y in range(5):
        for x in range(5):
            if masu[y][x] == 0:
                masu[y][x]=2
                hantei(4)
                if kati==2:
                    computer_te["text"]="勝ちに行きます\n","y軸",str(y),"x軸",str(x)
                    sh=sh+1
                    return
                masu[y][x]=0
    #3つ〇が置いてあった時、防ぐ
    for y in range(5):
        for x in range(5):
            if masu[y][x] == 0:
                masu[y][x]=1
                hantei(4)
                if kati==1:
                    masu[y][x]=2
                    computer_te["text"]="クリアを防ぎます\n","y軸",str(y),"x軸",str(x)
                    sh=sh+1
                    return
                masu[y][x]=0
    
    #2つ×が置いてあった時、リーチをかける
    for y in range(5):
        for x in range(5):
            if masu[y][x] == 0:
                masu[y][x]=2
                hantei(3)
                if kati==2:
                    computer_te["text"]="リーチをかけます\n","y軸",str(y),"x軸",str(x)
                    sh=sh+1
                    return
                masu[y][x]=0
    
    #2つ〇が置いてあった時、リーチを防ぐ
    for y in range(5):
        for x in range(5):
            if masu[y][x] == 0:
                masu[y][x]=1
                hantei(3)
                if kati==1:
                    masu[y][x]=2
                    computer_te["text"]="リーチを防ぎます\n","y軸",str(y),"x軸",str(x)
                    sh=sh+1
                    return
                masu[y][x]=0
    
    #近くに〇がある場合、その周囲をランダムに置く
    flag=False
    if se=="P":
        for y in range(5):
            for x in range(5):
                if (x != 0 and masu[y][x-1]==1) or (x!=4 and masu[y][x+1]==1) or (y!= 0 and masu[y-1][x]==1)\
                or (y!=4 and masu[y+1][x]==1):
                    if masu[y][x]==0:
                        masu_r.append([y,x])
                        flag=True
    
    if flag:
        flag=False
        ra=random.randint(0,len(masu_r)-1)
        py=masu_r[ra][0]
        px=masu_r[ra][1]
        masu[py][px]=2
        computer_te["text"]="〇の近くに置いて妨害します\n ","y軸",str(py),"x軸",str(px)
        masu_r.clear()
        sh=sh+1
        return
    
    flag=False
    if se=="C":
        for y in range(5):
            for x in range(5):
                if (x != 0 and masu[y][x-1]==2) or (x!=4 and masu[y][x+1]==2) or (y!= 0 and masu[y-1][x]==2)\
                or (y!=4 and masu[y+1][x]==2):
                    if masu[y][x]==0:
                        masu_r.append([y,x])
                        flag=True
    
    if flag:
        flag=False
        ra=random.randint(0,len(masu_r)-1)
        py=masu_r[ra][0]
        px=masu_r[ra][1]
        masu[py][px]=2
        computer_te["text"]="×の近くに置いて勝機を狙います\n ","y軸",str(py),"x軸",str(px)
        masu_r.clear()
        sh=sh+1
        return

    while True:
        x=random.randint(0,4)
        y=random.randint(0,4)
        if masu[y][x] == 0:
            computer_te["text"]="適当に置きます\n","y軸",str(y),"x軸",str(x)
            masu[y][x]=2
            sh=sh+1
            break

def hantei(ko):
    global kati
    kati=0
    # 横のフラグ
    for v in range(5):
        flag=0
        flag2=0
        flag3=0
        flag4=0
        for i in range(5):
            if masu[v][i] == 1 and (flag2<ko):
                flag = flag+1
                flag2=0
                flag4=1
            if masu[v][i] == 2 and (flag<ko):
                flag2 = flag2+1
                flag=0
                flag3=1
            if masu[v][i] == 0 and (flag<ko and flag2<ko):
                flag=0
                flag2=0
        if ko==3 and ((flag4==1 and flag2>=3) or (flag>=3 and flag3==1)):
            kati = 0
        elif flag>=ko:
            kati = 1
        elif flag2>=ko:
            kati = 2
    #縦のフラグ
    for v in range(5):
        flag=0
        flag2=0
        flag3=0
        flag4=0
        for i in range(5):
            if masu[i][v] == 1 and (flag2<ko):
                flag = flag+1
                flag2=0
                flag4=1
            if masu[i][v] == 2 and (flag<ko):
                flag2 = flag2+1
                flag=0
                flag3=1
            if masu[i][v] == 0 and (flag<ko and flag2<ko):
                flag=0
                flag2=0
        if ko==3 and ((flag4==1 and flag2>=3) or (flag>=3 and flag3==1)):
            kati = 0
        elif flag>=ko:
            kati = 1
        elif flag2>=ko:
            kati = 2
    #斜めのフラグ
    for i in range(3):
        flag=0
        flag2=0
        flag3=0
        flag4=0
        if i==0:
            s1=1
            s2=0
            ra=4
        if i==1:
            s1=0
            s2=0
            ra=5
        if i==2:
            s1=0
            s2=1
            ra=4
        for v in range(ra):
            if masu[s1+v][s2+v] == 1 and (flag2<ko):
                flag = flag+1
                flag2=0
                flag4=1
            if masu[s1+v][s2+v] == 2 and (flag<ko):
                flag2 = flag2+1
                flag=0
                flag3=1
            if masu[s1+v][s2+v] == 0 and (flag<ko and flag2<ko):
                flag=0
                flag2=0
        if ko==3 and ((flag4==1 and flag2>=3) or (flag>=3 and flag3==1)):
            kati = 0
        elif flag>=ko:
            kati = 1
        elif flag2>=ko:
            kati = 2
    
    for i in range(3):
        flag=0
        flag2=0
        flag3=0
        flag4=0
        if i==0:
            s1=0
            s2=3
            ra=4
        if i==1:
            s1=0
            s2=4
            ra=5
        if i==2:
            s1=1
            s2=4
            ra=4
        for v in range(ra):
            if masu[s1+v][s2-v] == 1 and (flag2<ko):
                flag = flag+1
                flag2=0
                flag4=1
            if masu[s1+v][s2-v] == 2 and (flag<ko):
                flag2 = flag2+1
                flag=0
                flag3=1
            if masu[s1+v][s2-v] == 0 and (flag<ko and flag2<ko):
                flag=0
                flag2=0
        if ko==3 and ((flag4==1 and flag2>=3) or (flag>=3 and flag3==1)):
            kati = 0
        elif flag>=ko:
            kati = 1
        elif flag2>=ko:
            kati = 2

def syouhai():
    global kati,sh,sy
    if kati==1:
        tkinter.messagebox.showinfo("おめでとう","ゲームクリアです！")
        sy = sy+1
        replay()
    elif kati==2:
        tkinter.messagebox.showinfo("駄目でした","ゲームオーバーです！")
        sy = sy+1
        replay()
    elif kati==0 and sh == 25:
        tkinter.messagebox.showinfo("引き分け","引き分けです、もう1度やり直してください")
        sy = sy+1
        replay()
    else:
        return

def replay():
    global sh,se
    sh=0
    if se == "C":
        sen == "C"
    if se == "P":
        sen == "P"
    for y in range(5):
        for x in range(5):
            masu[y][x]=0
    
def main():
    global cvs,sy,sen
    title = tkinter.Label(root, text="四目並べ",font=("HGS創英角ﾎﾟｯﾌﾟ体",24),bg="snow",fg="black")
    rulu = tkinter.Label(root, text="縦、横、ななめに\n4つ揃えた方が勝ち！",font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="black")
    button_p = tkinter.Button(root, text="先攻",font=("Times New Roman",24),bg="skyblue",fg="black",command=click_btn)
    button_c = tkinter.Button(root, text="後攻",font=("Times New Roman",24),bg="red",fg="black",command=click_btn2)
    button_r = tkinter.Button(root, text="ランダム",font=("Times New Roman",24),bg="gold",fg="black",command=click_btn3)
    button_p.place(x=700, y=400)
    button_c.place(x=700, y=500)
    button_r.place(x=700, y=600)
    title.place(x=720, y=120)
    rulu.place(x=700, y=200)
    if sy == 0:
        root.bind("<Button>",click)
    root.mainloop()


if __name__ == '__main__':
    print("Hello world")
    root=tkinter.Tk()
    root.title("四目並べ")
    root.resizable(False,False)
    cvs=tkinter.Canvas(root,width=1000,height=700,bg="white")
    cvs.pack()
    gazou_titlehaikei=tkinter.PhotoImage(file="haikei.png")
    cvs.create_image(500,350, image=gazou_titlehaikei, tag="HAIKEI")
    computer_te = tkinter.Label(root, text="コンピューターが相手します",font=("HGS創英角ﾎﾟｯﾌﾟ体",16),bg="snow",fg="black")
    computer_te.place(x=700, y=280)
    main()