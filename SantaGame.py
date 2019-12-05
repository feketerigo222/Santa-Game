import tkinter

# マップ描画


def draw_map():
    for y in range(0, MAX_HEIGHT):
        for x in range(0, MAX_WIDTH):
            p = map_data[y][x]
            if p >= 5:
                p = 5
            canvas.create_image(x * 62 + 31, y * 62 + 31, image=images[p])

    # サンタ表示
    canvas.create_image(santa_x * 62 + 31, santa_y * 62 +
                        31, image=images[4], tag="santa")

# 移動先のチェック
