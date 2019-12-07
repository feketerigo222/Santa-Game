import tkinter
import random
import time


class FightManager:
    # コンストラクタ
    def __init__(self):
        self.dialog = tkinter.Frame(width=820, height=434)
        self.dialog.place(x=10, y=10)
        self.canvas = tkinter.Canvas(self.dialog, width=820, height=434)
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 0, 620, 434, fill="black")
        # ボタン作成
        self.fbutton = tkinter.Button(self.dialog, text="攻撃")
        self.fbutton.place(x=180, y=340)
        self.fbutton["command"] = self.click_fight
        self.rbutton = tkinter.Button(self.dialog, text="力をためる")
        self.rbutton.place(x=320, y=340)
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
            self.dialog, text="ラベル", fg="white", bg="black", justify="left")
        self.label.place(x=360, y=10)

    # 戦闘開始

    def fight_start(self, mapdata, x, y, santa, flag_emergency):
        self.dialog.place(x=10, y=10)
        self.map_data = mapdata
        self.santa_x = x
        self.santa_y = y
        self.santa = santa
        # 敵の画像を表示
        p = self.map_data[y][x]
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 620, 434, fill="black")
        if flag_emergency == True and p == 8:
            self.canvas.create_image(180, 160, image=self.images[2])
        else:
            self.canvas.create_image(180, 160, image=self.images[p-8])
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
        # 主人公のターン
        enemy_dfs = self.enemy.get_dfs()
        if santa_atk < 0:
            labeltext = "サンタは力をためた"
        else:
            labeltext = "サンタは攻撃した"
            self.label["text"] = labeltext
            self.dialog.update()
            # サンタの攻撃の結果表示
            time.sleep(2)  # 2秒待ち
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
        time.sleep(2)  # 2秒待ち
        labeltext = labeltext + \
            "\n敵の残り体力は" + str(self.enemy.hp)
        self.label["text"] = labeltext
        self.dialog.update()
        if self.enemy.hp < 1:
            time.sleep(2)  # 2秒待ち
            self.fbutton["state"] = "normal"
            self.rbutton["state"] = "normal"
            self.fight_win()
            return
        # 敵のターン
        time.sleep(2)  # 2秒待ち
        santa_dfs = self.santa.get_dfs()
        if random.random() < 0.2:
            labeltext = labeltext + "\n\n敵は力をためた"
            self.enemy.reserve()
        else:
            labeltext = labeltext + "\n\n敵の攻撃"
            self.label["text"] = labeltext
            self.dialog.update()
            if self.santa.hp < 1:
                time.sleep(2)  # 2秒待ち
                self.fight_lose()
            else:
                #　ボタンを有効化して次のターンへ
                self.fbutton["state"] = "normal"
                self.rbutton["state"] = "normal"
            # 敵の攻撃の結果表示
            time.sleep(2)  # 2秒待ち
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
        time.sleep(2)  # 2秒待ち
        labeltext = labeltext + \
            "\nサンタの残り体力は" + str(self.santa.hp)
        self.label["text"] = labeltext
        self.dialog.update()
        if self.santa.hp < 1:
            time.sleep(2)
            self.fight_lose()
        else:
            self.fbutton["state"] = "normal"
            self.rbutton["state"] = "normal"
    # 勝利

    def fight_win(self):
        self.map_data[self.santa_y][self.santa_x] = 0
        # 不審者フラグ立ってれば血痕に変える
        self.dialog.place_forget()

    # 敗北
    def fight_lose(self):
        canvas = tkinter.Canvas(self.dialog, width=820, height=434)
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0, 0, 620, 434, fill="red")
        canvas.create_text(300, 200, fill="white", font=("MS ゴシック", 15), text="""勇者は負けてしまった
        最初からやり直してくれたまえ""")

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