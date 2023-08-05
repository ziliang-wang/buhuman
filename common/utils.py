from datetime import datetime
import random
import string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw


class ImageCode(object):

    def get_text(self):
        list = random.sample(string.ascii_letters + string.digits, 4)
        return ''.join(list)

    def rand_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue

    def draw_lines(self, draw, num, width, height):
        for _ in range(num):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)

            x2 = random.randint(0, width)
            y2 = random.randint(height, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    def gen_image_code(self):
        text = self.get_text()
        # print(text)
        # 圖片的寬和高
        # width, height = 120, 50
        width, height = 110, 48
        image = Image.new('RGB', (width, height), '#f3f5f6')
        font = ImageFont.truetype(font='C:\Windows\Fonts\Arial.ttf', size=30)
        draw = ImageDraw.Draw(image)
        # 整合字串
        for i in range(4):
            draw.text((random.randint(3, 10) + 25 * i, random.randint(3, 10)),
                      text=text[i], fill=self.rand_color(), font=font)
        # 繪製干擾線

        self.draw_lines(draw, 2, width, height)
        # image.show()
        return image, text

    def get_code(self):
        image, code = self.gen_image_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        image_b_string = buf.getvalue()
        return code, image_b_string


# image_code = ImageCode()
# image_code.gen_image_code()
def model_to_json(result):
    result_dict = {}

    for k, v in result.__dict__.items():
        if not k.startswith('_sa_'):
            if isinstance(v, datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            result_dict[k] = v

    return result_dict


def compress_image(source, dest, width=1200):
    im = Image.open(source)
    x, y = im.size
    if x > width:
        ys = int(y*width/x)
        xs = width
        tmp = im.resize((xs, ys), Image.ANTIALIAS)
        tmp.save(dest, quality=80)
    else:
        im.save(dest, quality=80)
