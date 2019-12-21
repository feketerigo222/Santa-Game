import tkinter
import time
import cv2
import random
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
                flag_label.place(x=360, y=600)
                return
            elif fight.flag_ax == False:
                flag_label["text"] = "家に入る手段がない"
                flag_label.place(x=360, y=600)
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
            flag_label.place(x=360, y=600)
        elif p == 5:
            fight.flag_ax = True
            santa.atk *= 3
            map_data[y][x] = 0
            canvas.delete("all")
            draw_map(santa_direction)
            flag_label["text"] = "斧を手に入れた"
            flag_label.place(x=360, y=600)
        elif p == 6:
            if fight.flag_money == True:
                fight.flag_toy = True
                map_data[y][x] = 7
                canvas.delete("all")
                draw_map(santa_direction)
                flag_label["text"] = "おもちゃを買った"
                flag_label.place(x=360, y=600)
            elif fight.flag_ax == True and fight.flag_money == False:
                fight.flag_toy = True
                fight.flag_emergency = True
                map_data[y][x] = 1
                canvas.delete("all")
                draw_map(santa_direction)
                flag_label["text"] = "素直におもちゃを渡さないあいつが悪いんだ…"
                flag_label.place(x=200, y=600)
            else:
                flag_label["text"] = "お金がない"
                flag_label.place(x=360, y=600)
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

# タイトル消去


def forget_title(event):
    frame.destroy()


# エンディング表示


def ending():
    canvas.delete("all")
    ending_frame = tkinter.Frame(width=960, height=640)
    ending_frame.place(x=10, y=10)
    ending_canvas = tkinter.Canvas(ending_frame, width=960, height=640)
    ending_canvas.place(x=0, y=0)
    ending_canvas.create_rectangle(0, 0, 960, 640, fill="white")
    ending_label_up = tkinter.Label(ending_frame, width=0, height=0, text=" ", font=("Chiller", 230),
                                    fg="red", bg="white")
    ending_label_down = tkinter.Label(ending_frame, width=0, height=0, text=" ", font=("Chiller", 230),
                                      fg="red", bg="white")
    ending_label_up["text"] = "Merry"
    ending_label_down["text"] = "Christmas"
    ending_label_up.place(x=240, y=0)
    ending_label_down.place(x=40, y=340)
    cap = cv2.VideoCapture('movie/shining.mp4')

    fps = 250

    if cap.isOpened() == False:
        print("Error!")

    while cap.isOpened():

        ret, ending = cap.read()

        if ret == True:

            time.sleep(1/fps)
            cv2.imshow('ending', ending)

            if cv2.waitKey(1) & 0xFF == ord('q'):

                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()


# ウィンドウ作成
root = tkinter.Tk()
root.title("DETROIT BECOME SANTA")
root.minsize(980, 660)
root.option_add("*font", ["メイリオ", 14])

# キャンバス作成
canvas = tkinter.Canvas(width=960, height=640)
canvas.place(x=10, y=10)
canvas.create_rectangle(0, 0, 960, 640, fill="white")

# タイトル作成
frame = tkinter.Frame(width=960, height=640)
frame.place(x=10, y=10)
title = tkinter.Canvas(frame, width=960, height=640)
title.place(x=0, y=0)
title.create_rectangle(0, 0, 960, 640, fill="black")
title_label_up = tkinter.Label(frame, width=0, height=0, text=" ", font=("Arial Black", 70),
                               fg="white", bg="black")
title_label_down = tkinter.Label(frame, width=0, height=0, text=" ", font=("Arial", 20),
                                 fg="white", bg="black")
press_any_key = tkinter.Label(frame, width=0, height=0, text=" ", font=("Arial", 25),
                              fg="white", bg="black")
title_label_up["text"] = "DETROIT"
title_label_down["text"] = "B   E   C   O   M   E       S   A   N   T   A"
press_any_key["text"] = "-  Press any key to start  -"
title_label_up.place(x=240, y=220)
title_label_down.place(x=230, y=340)
press_any_key.place(x=280, y=480)

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
             tkinter.PhotoImage(file="img/map/soldout.png"),
             tkinter.PhotoImage(file="img/map/enemy.png")]

# 乱数で敵生成
e = [0] * 13
i = 0
while i < 13:
    num = random.random()
    if num < 0.5:
        e[i] = 8
    else:
        e[i] = 9
    i += 1

# マップデータ
MAX_WIDTH = 15
MAX_HEIGHT = 10
map_data = [[2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, e[0], 0, 2, 0, e[1], 0, 2, 4, 2, 3, 2],
            [2, 0, 0, 2, 2, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2],
            [2, 2, 2, 0, 0, 0, 2, e[2], 0, 2, 2, 0, 2, 0, 2],
            [2, 0, 0, 0, 2, 0, 0, 2, 0, e[3], 0, e[4], 2, 0, 2],
            [2, e[5], 2, 0, 0, e[6], 0, 2, 0, 2, 0, 2, 0, e[7], 2],
            [2, 0, 0, e[8], 2, 0, 0, 0, 0, 2, 0, 0, e[9], 0, 2],
            [2, 5, 2, 0, 0, 2, 2, 2, 0, 0, e[10], 2, 0, 0, 2],
            [2, 0, e[11], 0, e[12], 6, 2, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]


# 戦闘画面の準備
fightmanager = fight.FightManager()


draw_map(santa_direction)


# title消去
root.bind("<Any-KeyPress>", forget_title)

# ボタンでの移動
root.bind("<Key-Up>", click_button_up)
root.bind("<Key-Down>", click_button_down)
root.bind("<Key-Left>", click_button_left)
root.bind("<Key-Right>", click_button_right)

root.mainloop()
