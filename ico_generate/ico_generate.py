from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter


def create_material_design_icon():
    # 创建512x512像素的图像（更大的尺寸以便后续缩放）
    size = 512
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)

    # Material Design 调色板
    primary_color = (33, 150, 243, 255)  # 蓝色500（添加Alpha通道）
    secondary_color = (255, 193, 7, 255)  # 琥珀色500（添加Alpha通道）
    background_color = (255, 255, 255, 255)  # 不透明白色

    # 创建圆形背景（Material Design 强调形状）
    bg_size = int(size * 0.9)
    bg_pos = ((size - bg_size) // 2, (size - bg_size) // 2)

    draw.ellipse(
        [bg_pos[0], bg_pos[1], bg_pos[0] + bg_size, bg_pos[1] + bg_size],
        fill=background_color,
    )

    # 绘制带有轻微阴影的圆形背景
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse(
        [bg_pos[0], bg_pos[1], bg_pos[0] + bg_size, bg_pos[1] + bg_size],
        fill=(0, 0, 0, 80),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    icon = Image.alpha_composite(icon, shadow)

    # 重新创建绘图对象以应用后续绘制
    draw = ImageDraw.Draw(icon)

    # 绘制书本图标（简化几何形状）
    book_width = int(size * 0.5)
    book_height = int(size * 0.35)
    book_x = (size - book_width) // 2
    book_y = (size - book_height) // 2

    # 书本主体
    draw.rounded_rectangle(
        [book_x, book_y, book_x + book_width, book_y + book_height],
        radius=20,
        fill=primary_color,
        outline=(255, 255, 255, 230),  # 边框颜色
        width=4,  # 边框宽度
    )

    # 书本脊背
    spine_width = int(book_width * 0.15)
    draw.rectangle(
        [
            book_x + book_width - spine_width,
            book_y,
            book_x + book_width,
            book_y + book_height,
        ],
        fill=(25, 118, 210),  # 更深的蓝色700
    )

    # 书本内页线
    for i in range(1, 5):
        line_y = book_y + i * (book_height // 5)
        draw.line(
            [
                book_x + 20,
                line_y,
                book_x + book_width - spine_width - 20,
                line_y,
            ],
            fill=(255, 255, 255, 180),
            width=4,
        )

    # 添加钢笔图标（Material Design风格的简洁线条）
    pen_length = int(size * 0.4)
    pen_x = book_x + book_width // 2
    pen_y = book_y + book_height // 2 - 20

    # 钢笔杆
    draw.line(
        [pen_x, pen_y - pen_length // 2, pen_x, pen_y + pen_length // 2],
        fill=secondary_color,
        width=12,
        joint="curve",
    )

    # 顶部高光：
    draw.line(
        [
            pen_x,
            pen_y - pen_length // 2,
            pen_x,
            pen_y - pen_length // 2 + int(pen_length * 0.2),
        ],
        fill=(255, 255, 255, 180),
        width=6,
        joint="curve",
    )

    # 钢笔尖
    pen_tip_size = int(size * 0.1)
    draw.polygon(
        [
            (pen_x - pen_tip_size, pen_y + pen_length // 2),
            (pen_x, pen_y + pen_length // 2 + pen_tip_size),
            (pen_x + pen_tip_size, pen_y + pen_length // 2),
        ],
        fill=secondary_color,
    )

    # 添加"Edit"文字（Material Design风格）
    # 指定下载的 RobotoSlab 字体路径
    font_path = (
        "/data/data/com.termux/files/home/.termux/fonts/RobotoSlab[wght].ttf"
    )
    try:
        font = ImageFont.truetype(font_path, int(size * 0.15))
    except IOError:
        # 如果加载失败，回退到默认字体
        font = ImageFont.load_default()
        print("警告：自定义字体加载失败，已回退到默认字体")

    text = "EDIT"  # 改为全大写更符合Material风格
    # 使用新的textbbox方法替代已弃用的textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 调整文字位置，增加与书本的距离
    text_y_offset = (
        book_y + book_height + int(size * 0.08)
    )  # 从30改为按比例计算

    # "EDIT" 文字添加阴影效果
    shadow_offset_text = int(size * 0.008)
    draw.text(
        (
            (size - text_width) // 2 + shadow_offset_text,
            text_y_offset + shadow_offset_text,
        ),
        text,
        font=font,
        fill=(0, 0, 0, 100),  # 文本阴影色
    )

    # 添加文字背景圆角矩形
    text_bg_padding = int(size * 0.03)
    draw.rounded_rectangle(
        [
            (size - text_width) // 2 - text_bg_padding,
            text_y_offset - text_bg_padding,
            (size + text_width) // 2 + text_bg_padding,
            text_y_offset + text_height + text_bg_padding,
        ],
        radius=int(size * 0.02),
        fill=(255, 255, 255, 220),  # 半透明白色背景
    )
    draw.text(
        ((size - text_width) // 2, text_y_offset),
        text,
        font=font,
        fill=primary_color,  # 使用主色调更协调
    )

    # 只保存PNG格式（透明背景）
    icon.save("material_app_icon.png")
    print("PNG图标已成功生成: material_app_icon.png")

    return icon


if __name__ == "__main__":
    create_material_design_icon()
