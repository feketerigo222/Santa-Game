import tkinter
import time
import SantaGameFight as fight


# サンタの位置
santa_x = 1
santa_y = 0
santa = fight.Santa()
santa_direction = 0

# マップ描画


def draw_map(santa_direction):
    for y in range(0, MAX_HEIGHT):
        for x in range(0, MAX_WIDTH):
            p = map_data[y][x]
            if p >= 8:
                p = 8
            canvas.create_image(x * 64 + 32, y * 64 + 32, image=mapImages[p])

    # サンタ表示
    canvas.create_image(santa_x * 64 + 31, santa_y * 64 +
                        31, image=santaImages[santa_direction], tag="santa")
    # i = 0
    # j = 0
    # while j < 100:
    #     while i < 5:
    #         canvas.create_image(santa_x * 64 + 31, santa_y * 64 + 31,
    #                             image=santaImages[santa_direction][i], tag="santa")
    #         canvas.update()
    #         i += 1
    #         if i == 4:
    #             i = 0
    #         time.sleep(0.25)


# 移動先のチェック


def check_move(x, y, santa_direction):
    global santa_x, santa_y
    flag_label.place_forget()
    if x >= 0 and x < MAX_WIDTH and y >= 0 and y < MAX_HEIGHT:
        p = map_data[y][x]
        if p == 2:
            return
        elif p == 3:
            if fight.flag_toy == False:
                flag_label["text"] = "おもちゃがない"
                flag_label.place(x=380, y=600)
                return
            elif fight.flag_ax == False:
                flag_label["text"] = "家に入る手段がない"
                flag_label.place(x=380, y=600)
                return
            else:
                ending()
                return
        elif p == 4:
            fight.flag_money = True
            map_data[y][x] = 0
            canvas.delete("all")
            draw_map(santa_direction)
            flag_label["text"] = "お金を拾った"
            flag_label.place(x=380, y=600)
        elif p == 5:
            fight.flag_ax = True
            santa.atk *= 3
            map_data[y][x] = 0
            canvas.delete("all")
            draw_map(santa_direction)
            flag_label["text"] = "斧を手に入れた"
            flag_label.place(x=380, y=600)
        elif p == 6:
            if fight.flag_money == True:
                fight.flag_toy = True
                map_data[y][x] = 0
                canvas.delete("all")
                draw_map(santa_direction)
                flag_label["text"] = "おもちゃを買った"
                flag_label.place(x=380, y=600)
            elif fight.flag_ax == True:
                fight.flag_toy = True
                fight.flag_emergency = True
                map_data[y][x] = 1
                canvas.delete("all")
                draw_map(santa_direction)
                flag_label["text"] = "素直におもちゃを渡さないあいつが悪いんだ…"
                flag_label.place(x=380, y=600)
            else:
                flag_label["text"] = "お金がない"
                flag_label.place(x=380, y=600)
                return

        elif p >= 8:
            fightmanager.fight_start(
                map_data, x, y, santa)
        santa_x = x
        santa_y = y
        canvas.delete("all")
        draw_map(santa_direction)


# 上ボタンが押された


def click_button_up(event):
    global santa_direction
    santa_direction = 3
    check_move(santa_x, santa_y-1, santa_direction)

# 下ボタンが押された


def click_button_down(event):
    global santa_direction
    santa_direction = 0
    check_move(santa_x, santa_y+1, santa_direction)

# 左ボタンが押された


def click_button_left(event):
    global santa_direction
    santa_direction = 2
    check_move(santa_x-1, santa_y, santa_direction)

# 右ボタンが押された


def click_button_right(event):
    global santa_direction
    santa_direction = 1
    check_move(santa_x+1, santa_y, santa_direction)


# エンディング表示


def ending():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 640, 448, fill="black")
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
root.minsize(980, 660)
root.option_add("*font", ["メイリオ", 14])

# キャンバス作成
canvas = tkinter.Canvas(width=960, height=640)
canvas.place(x=10, y=10)
canvas.create_rectangle(0, 0, 960, 640, fill="gray")

# フラグ用ラベル
flag_label = tkinter.Label(width=0, height=0, text=" ", font=("メイリオ", 20),
                           fg="white", bg="black",)

# # ボタン配置
# button_up = tkinter.Button(text="↑")
# button_up.place(x=720, y=150)
# button_up["command"] = click_button_up
# button_down = tkinter.Button(text="↓")
# button_down.place(x=720, y=210)
# button_down["command"] = click_button_down
# button_left = tkinter.Button(text="←")
# button_left.place(x=660, y=180)
# button_left["command"] = click_button_left
# button_right = tkinter.Button(text="→")
# button_right.place(x=780, y=180)
# button_right["command"] = click_button_right


# 画像データ読み込み
# サンタ画像

santaImages = [tkinter.PhotoImage(file="img/santa/front.gif"),
               tkinter.PhotoImage(file="img/santa/right.gif"),
               tkinter.PhotoImage(file="img/santa/left.gif"),
               tkinter.PhotoImage(file="img/santa/back.gif"), ]
# santaImages = [[tkinter.PhotoImage(file="img/santa/front.gif", format="gif -index 0", master=root),
#                 tkinter.PhotoImage(file="img/santa/front.gif",
#                                    format="gif -index 1", master=root),
#                 tkinter.PhotoImage(file="img/santa/front.gif",
#                                    format="gif -index 2", master=root),
#                 tkinter.PhotoImage(file="img/santa/front.gif", format="gif -index 3", master=root), ],

#                [tkinter.PhotoImage(file="img/santa/right.gif", format="gif -index 0", master=root),
#                 tkinter.PhotoImage(file="img/santa/right.gif",
#                                    format="gif -index 1", master=root),
#                 tkinter.PhotoImage(file="img/santa/right.gif",
#                                    format="gif -index 2", master=root),
#                 tkinter.PhotoImage(file="img/santa/right.gif", format="gif -index 3", master=root), ],

#                [tkinter.PhotoImage(file="img/santa/left.gif", format="gif -index 0", master=root),
#                 tkinter.PhotoImage(file="img/santa/left.gif",
#                                    format="gif -index 1", master=root),
#                 tkinter.PhotoImage(file="img/santa/left.gif",
#                                    format="gif -index 2", master=root),
#                 tkinter.PhotoImage(file="img/santa/left.gif", format="gif -index 3", master=root), ],

#                [tkinter.PhotoImage(file="img/santa/back.gif", format="gif -index 0", master=root),
#                 tkinter.PhotoImage(file="img/santa/back.gif",
#                                    format="gif -index 1", master=root),
#                 tkinter.PhotoImage(file="img/santa/back.gif",
#                                    format="gif -index 2", master=root),
#                 tkinter.PhotoImage(file="img/santa/back.gif", format="gif -index 3", master=root), ]]

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
MAX_WIDTH = 15
MAX_HEIGHT = 10
map_data = [[2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 3, 0, 0, 1, 4, 2, 2, 2, 2, 2, 2],
            [2, 0, 4, 2, 2, 1, 0, 1, 6, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 5, 0, 0, 0, 1, 0, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 1, 1, 1, 8, 2, 2, 2, 2, 2, 2],
            [2, 0, 9, 0, 9, 0, 5, 0, 0, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]


# 戦闘画面の準備
fightmanager = fight.FightManager()


draw_map(santa_direction)

# ボタンでの移動
root.bind("<Key-Up>", click_button_up)
root.bind("<Key-Down>", click_button_down)
root.bind("<Key-Left>", click_button_left)
root.bind("<Key-Right>", click_button_right)


root.mainloop()
