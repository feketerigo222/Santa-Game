import tkinter
import random
import time
import random

# 初期フラグ
flag_ax = False
flag_money = False
flag_toy = False
flag_emergency = False


class FightManager:
    # コンストラクタ
    def __init__(self):
        self.dialog = tkinter.Frame(width=960, height=640)
        self.dialog.place(x=10, y=10)
        self.canvas = tkinter.Canvas(self.dialog, width=960, height=640)
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 0, 960, 640, fill="black")
        # ボタン作成
        self.fbutton = tkinter.Button(
            self.dialog, text="攻撃", font=("メイリオ", 20))
        self.fbutton.place(x=280, y=550)
        self.fbutton["command"] = self.click_fight
        self.rbutton = tkinter.Button(
            self.dialog, text="力をためる", font=("メイリオ", 20))
        self.rbutton.place(x=580, y=550)
        self.rbutton["command"] = self.click_reserve
        # # 非表示
        self.dialog.place_forget()
        # 画像の読み込み
        self.images = [tkinter.PhotoImage(file="img/map/police.png"),
                       tkinter.PhotoImage(file="img/map/yakuza.png"),
                       tkinter.PhotoImage(file="img/map/police_emergency.png")]
        self.canvas.create_image(180, 160, image=self.images[0])
        # ラベルを配置
        self.label = tkinter.Label(
            self.dialog, text="ラベル", fg="white", bg="black", justify="left", font=("メイリオ", 20))
        self.label.place(x=650, y=10)

    # 戦闘開始

    def fight_start(self, map_data, x, y, santa):
        global flag_emergency
        self.dialog.place(x=10, y=10)
        self.map_data = map_data
        self.santa_x = x
        self.santa_y = y
        self.santa = santa
        # 敵の画像を表示
        p = self.map_data[y][x]
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 960, 640, fill="black")
        if flag_emergency == True and p == 8:
            self.canvas.create_image(480, 300, image=self.images[2])
        else:
            self.canvas.create_image(480, 300, image=self.images[p-8])
        self.label["text"] = ""
        # 敵のオブジェクトを作成
        if p == 8:
            self.enemy = Police()
            # 不審者フラグが立ってれば攻撃力3倍
            if flag_emergency == True:
                self.enemy.atk *= 3
        elif p == 9:
            self.enemy = Yakuza()
        self.label["text"] = self.enemy.name + "が現れた"

    # 攻撃ボタン

    def click_fight(self):
        self.fbutton["state"] = "disabled"
        self.rbutton["state"] = "disabled"
        self.do_turn(self.santa.get_atk())

    # 力をためるボタン

    def click_reserve(self):
        self.fbutton["state"] = "disabled"
        self.rbutton["state"] = "disabled"
        self.santa.reserve()
        self.do_turn(-1)

    # 戦闘処理
    def do_turn(self, santa_atk):
        global flag_money
        # 主人公のターン
        enemy_dfs = self.enemy.get_dfs()
        if santa_atk < 0:
            labeltext = "サンタは力をためた"
        else:
            labeltext = "サンタは攻撃した"
            self.label["text"] = labeltext
            self.dialog.update()
            # サンタの攻撃の結果表示
            time.sleep(1)  # 2秒待ち
            dmg = santa_atk - enemy_dfs
            self.enemy.culc_hp(santa_atk, enemy_dfs)
            if dmg <= 0:
                labeltext = labeltext + "\n防がれた"
            else:
                labeltext = labeltext + "\n" + str(dmg) + \
                    "のダメージを与えた"
        # ラベル更新、残り体力表示
        self.label["text"] = labeltext
        self.dialog.update()
        time.sleep(1)  # 2秒待ち
        labeltext = labeltext + \
            "\n敵の残り体力は" + str(self.enemy.hp)
        self.label["text"] = labeltext
        self.dialog.update()
        if self.enemy.hp < 1:
            time.sleep(1)  # 2秒待ち
            self.fbutton["state"] = "normal"
            self.rbutton["state"] = "normal"
            self.fight_win()
        # 敵のターン
        time.sleep(1)  # 2秒待ち
        santa_dfs = self.santa.get_dfs()
        enemy_name = self.enemy.get_name()
        if enemy_name == "ヤクザ" and flag_money == True:
            labeltext = labeltext + "\n\n敵はカツアゲをしてきた" + "\nお金を失った"
            flag_money = False
        elif random.random() < 0.2:
            labeltext = labeltext + "\n\n敵は力をためた"
            self.enemy.reserve()
        else:
            labeltext = labeltext + "\n\n敵の攻撃"
            self.label["text"] = labeltext
            self.dialog.update()
            # 敵の攻撃の結果表示
            time.sleep(1)  # 2秒待ち
            enemy_atk = self.enemy.get_atk()
            dmg = enemy_atk - santa_dfs
            self.santa.culc_hp(enemy_atk, santa_dfs)
            if dmg <= 0:
                labeltext = labeltext + "\n防いだ"
            else:
                labeltext = labeltext + "\n" + str(dmg) + \
                    "のダメージを受けた"
        # ラベル更新、残り体力表示
        self.label["text"] = labeltext
        self.dialog.update()
        time.sleep(1)  # 2秒待ち
        labeltext = labeltext + \
            "\nサンタの残り体力は" + str(self.santa.hp)
        self.label["text"] = labeltext
        self.dialog.update()
        if self.santa.hp < 1:
            time.sleep(1)
            self.fight_lose()
        else:
            self.fbutton["state"] = "normal"
            self.rbutton["state"] = "normal"
    # 勝利

    def fight_win(self):
        global flag_emergency
        if flag_emergency == True:
            self.map_data[self.santa_y][self.santa_x] = 1
        else:
            self.map_data[self.santa_y][self.santa_x] = 0
        self.dialog.place_forget()

    # 敗北
    def fight_lose(self):
        canvas = tkinter.Canvas(self.dialog, width=960, height=640)
        canvas.create_rectangle(0, 0, 960, 640, fill="black")
        canvas.place(x=0, y=0)
        num = random.random()
        print(num)
        if num < 0.5:
            lose_label = tkinter.Label(width=0, height=0, text=" ", font=("BIZ UD明朝 Medium", 60),
                                       fg="red", bg="black")
            lose_label["text"] = "YOU DIED"
            lose_label.place(x=330, y=280)
        else:
            lose_label_up = tkinter.Label(width=0, height=0, text=" ", font=("HGS行書体", 100),
                                          fg="red", bg="black")
            lose_label_down = tkinter.Label(width=0, height=0, text=" ", font=("BIZ UD明朝 Medium", 15),
                                            fg="red", bg="black")
            lose_label_up["text"] = "死"
            lose_label_down["text"] = "D E A T H"
            lose_label_up.place(x=420, y=230)
            lose_label_down.place(x=440, y=360)

# キャラクターの親クラス


class Character:
    # コンストラクタ
    def __new__(cls):
        obj = super().__new__(cls)
        obj.rsv = 1
        return obj
    # 力をためる

    def reserve(self):
        self.rsv = self.rsv + 1
    # 攻撃力を求める

    def get_atk(self):
        r = self.rsv
        self.rsv = 1
        return random.randint(1, self.atk * r)
    # 防御力を求める

    def get_dfs(self):
        return random.randint(0, self.dfs)
    # 体力計算

    def culc_hp(self, atk, dfs):
        dmg = atk - dfs
        # ダメージ無し
        if dmg < 1:
            return self.hp
        # 体力を減らす
        self.hp = self.hp - dmg
        if self.hp < 1:
            self.hp = 0
        return self.hp

    # # 名前を求める
    def get_name(self):
        return self.name

# サンタクラス


class Santa(Character):
    def __init__(self):
        self.name = "サンタ"
        self.hp = 30
        self.atk = 15
        self.dfs = 10

# 警官


class Police(Character):
    def __init__(self):
        self.name = "警察官"
        self.hp = 20
        self.atk = 15
        self.dfs = 8

# ヤクザ


class Yakuza(Character):
    def __init__(self):
        self.name = "ヤクザ"
        self.hp = 10
        self.atk = 8
        self.dfs = 5
