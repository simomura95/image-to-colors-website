import base64
import io
from PIL import Image  # for reading image files
import numpy as np
import pandas as pd
import os
from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap

RGB_DELTA = 24
N_COLORS = 10

# create flask app
app = Flask(__name__)
app.app_context().push()  # to avoid errors during runtime
Bootstrap(app)  # bootstrap on app
app.config['SECRET_KEY'] = os.environ.get('FLASK_LOGIN_KEY')  # needed for flask login and flash



def best_n_colors(df_sorted: pd.DataFrame, rgb_delta: int, n_best: int):
    best_n = [df_sorted[0]]
    for color_new in df_sorted[1:]:
        add = True
        for color_saved in best_n:
            if (color_saved-rgb_delta < color_new).all() and (color_new < color_saved+rgb_delta).all():
                add = False
                break
        if add:
            best_n.append(color_new)
            if len(best_n) >= n_best:
                return best_n


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        return render_template("index.html")
    file = request.files.get("file")
    file_extension = file.filename.split('.')[-1]
    if file_extension not in ('png', 'jpg', 'jpeg'):
        flash("Insert a .png, .jpg or .jpeg file!")
        return render_template("index.html")
    with Image.open(file) as img:
        if file_extension == 'png':  # if .png file, convert it into .jpg
            # img_rgb = img.convert("RGB")  # to work with .png files (they have 4 channels)
            # convert works bad with png with transparent background (it becomes black)
            img.load()  # required for png.split()
            image = Image.new("RGB", img.size, (255, 255, 255))
            image.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        else:  # is already a jpeg
            image = img
        data = io.BytesIO()
        image.save(data, "JPEG")
        b64_file = base64.b64encode(data.getvalue())

    img_array = np.array(image.getdata())
    colors_df = pd.DataFrame(img_array, columns=["red", "green", "blue"])
    colors_df_sorted = colors_df.groupby(by=["red", "green", "blue"], as_index=False).value_counts().sort_values(by="count", ascending=False)[["red", "green", "blue"]].values
    best_10_colors = best_n_colors(colors_df_sorted, RGB_DELTA, N_COLORS)
    colors_hex = ["#{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2]).upper() for color in best_10_colors]

    return render_template("index.html", colors=colors_hex, img=b64_file.decode('utf-8'))



# with Image.open("hades.png") as img:
#     img_rgb = img.convert("RGB")  # to work with .png files (they have 4 channels)
# img_array = np.array(img_rgb.getdata())
# colors_df = pd.DataFrame(img_array, columns=["red", "green", "blue"])
# colors_df_sorted = colors_df.groupby(by=["red", "green", "blue"], as_index=False).value_counts().sort_values(by="count", ascending=False)[["red", "green", "blue"]].values
#
# best_10_colors = best_n_colors(colors_df_sorted, RGB_DELTA, N_COLORS)
#
# # for debug: print colors in terminal
# for color in best_10_colors:
#     print(color)
#     print("#{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2]).upper())
#     print(f'\033[48;2;{color[0]};{color[1]};{color[2]}m{"color"}\033[0m')

if __name__ == '__main__':
    app.run(debug=True)
