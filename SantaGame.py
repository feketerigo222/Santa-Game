import tkinter
import SantaGameFight


# サンタの位置
santa_x = 1
santa_y = 0
santa = SantaGameFight.Santa()

# 初期フラグ
flag_ax = False
flag_money = False
flag_toy = False
flag_emergency = False
# マップ描画


def draw_map():
    for y in range(0, MAX_HEIGHT):
        for x in range(0, MAX_WIDTH):
            p = map_data[y][x]
            if p >= 8:
                p = 8
            canvas.create_image(x * 64 + 31, y * 64 + 31, image=mapImages[p])

    # サンタ表示
    canvas.create_image(santa_x * 64 + 31, santa_y * 64 +
                        31, image=santaImages[0], tag="santa")

# 移動先のチェック


def check_move(x, y):
    global santa_x, santa_y, flag_ax, flag_money, flag_toy, flag_ax
    if x >= 0 and x < MAX_WIDTH and y >= 0 and y < MAX_HEIGHT:
        p = map_data[y][x]
        if p == 2:
            return
        elif p == 3:
            if flag_toy == False:
                # おもちゃがないのコメント
                return
            elif flag_ax == False:
                # 家に入れないのコメント
                return
            else:
                ending()
                return
        elif p == 4:
            flag_money = True
            map_data[y][x] = 0
            canvas.delete("all")
            draw_map()
        elif p == 5:
            flag_ax = True
            map_data[y][x] = 0
            canvas.delete("all")
            draw_map()
        elif p == 6:
            if flag_money == True:
                flag_toy = True
                # おもちゃを買ったのコメント
                map_data[y][x] = 0
                canvas.delete("all")
                draw_map()
            elif flag_ax == True:
                flag_toy = True
                flag_emergency = True
                # おもちゃを強盗したのコメント
                map_data[y][x] = 1
                canvas.delete("all")
                draw_map()
            else:
                # お金が無いのコメント
                return

        elif p >= 8:
            fightmanager.fight_start(map_data, x, y, santa)
        santa_x = x
        santa_y = y
        canvas.delete("all")
        draw_map()

# 上ボタンが押された


def click_button_up():
    check_move(santa_x, santa_y-1)

# 下ボタンが押された


def click_button_down():
    check_move(santa_x, santa_y+1)

# 左ボタンが押された


def click_button_left():
    check_move(santa_x-1, santa_y)

# 右ボタンが押された


def click_button_right():
    check_move(santa_x+1, santa_y)

# エンディング表示


def ending():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 620, 434, fill="black")
    canvas.create_text(300, 200, fill="white", font=(
        "MS ゴシック", 15), text="""ゴールおめでとう。
        
        だが、君の戦いはまだ始まったばかりだ。
        
        
                             …つづく？""")

    # ボタンを無効か
    button_up["state"] = "disabled"
    button_down["state"] = "disabled"
    button_left["state"] = "disabled"
    button_right["state"] = "disabled"


# ウィンドウ作成
root = tkinter.Tk()
root.title("Santa Game")
root.minsize(840, 454)
root.option_add("*font", ["メイリオ", 14])

# キャンバス作成
canvas = tkinter.Canvas(width=620, height=434)
canvas.place(x=10, y=10)
canvas.create_rectangle(0, 0, 620, 434, fill="gray")

# ボタン配置
button_up = tkinter.Button(text="↑")
button_up.place(x=720, y=150)
button_up["command"] = click_button_up
button_down = tkinter.Button(text="↓")
button_down.place(x=720, y=210)
button_down["command"] = click_button_down
button_left = tkinter.Button(text="←")
button_left.place(x=660, y=180)
button_left["command"] = click_button_left
button_right = tkinter.Button(text="→")
button_right.place(x=780, y=180)
button_right["command"] = click_button_right

# 画像データ読み込み
# サンタ画像
santaImages = [tkinter.PhotoImage(file="img/santa/front.gif"),
               tkinter.PhotoImage(file="img/santa/right.gif"),
               tkinter.PhotoImage(file="img/santa/left.gif"),
               tkinter.PhotoImage(file="img/santa/back.gif"), ]

mapImages = [tkinter.PhotoImage(file="img/map/map.png"),
             tkinter.PhotoImage(file="img/map/blood.png"),
             tkinter.PhotoImage(file="img/map/tree.png"),
             tkinter.PhotoImage(file="img/map/house.png"),
             tkinter.PhotoImage(file="img/map/money.png"),
             tkinter.PhotoImage(file="img/map/ax.png"),
             tkinter.PhotoImage(file="img/map/toy.png"),
             tkinter.PhotoImage(file="img/map/blood2.png"),
             tkinter.PhotoImage(file="img/map/enemy.png")]

# マップデータ
MAX_WIDTH = 10
MAX_HEIGHT = 7
map_data = [[2, 0, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 3, 0, 0, 1, 4, 2],
            [2, 0, 4, 2, 2, 1, 0, 1, 6, 2],
            [2, 0, 0, 5, 0, 0, 0, 1, 0, 2],
            [2, 0, 0, 0, 0, 1, 1, 1, 8, 2],
            [2, 0, 8, 0, 0, 0, 5, 0, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]


# 戦闘画面の準備
fightmanager = SantaGameFight.FightManager()

draw_map()

root.mainloop()
