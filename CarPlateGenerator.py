import enum
import os
import random

from PIL import Image, ImageFilter
import argparse

from PIL.ImageFile import ImageFile

SUPPORT_ASCII= "ABCDEFGHJKLMNPQRSTUVWXYZ1234567890"
SUPPORT_HANZI="京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川贵云藏陕甘青宁新港澳使领学警"
SYMBOL_WIDTH=90
SYMBOL_HEIGHT=180
SYMBOL_MARGIN=SYMBOL_WIDTH // 45 * 12
PLATE_VERTICAL_MARGIN=SYMBOL_WIDTH // 45 * 25
PLATE_HORIZONTAL_MARGIN=SYMBOL_WIDTH // 45 * 15
SCALER = SYMBOL_WIDTH // 45

class GenMode(enum.Enum):
    CARPLATE = 1
    SYMBOL = 2

# 图片类型枚举
class ImageType(enum.Enum):
    ASCII = 1
    HANZI = 2
def get_ascii_img() -> ImageFile:
    return Image.open("./assets/ascii.png")

def get_hanzi_img() -> ImageFile:
    return Image.open("./assets/hanzi.png")

def get_base_img() -> ImageFile:
    return Image.open("./assets/carplate_base.png")

def split_img(index:int,img_type:ImageType):

    match img_type:
        case ImageType.ASCII:
            rows = 4
            cols = 10

            if 24 <= index :
                index += 6

            left = (index  % cols) * SYMBOL_WIDTH
            top = (index // cols) * SYMBOL_HEIGHT
            right = left + SYMBOL_WIDTH
            bottom = top + SYMBOL_HEIGHT
            return get_ascii_img().crop((left,top,right,bottom)).convert('RGBA')
        case ImageType.HANZI:
            rows = 4
            cols = 9
            left = (index  % cols) * SYMBOL_WIDTH
            top = (index // cols) * SYMBOL_HEIGHT
            right = left + SYMBOL_WIDTH
            bottom = top + SYMBOL_HEIGHT
            return get_hanzi_img().crop((left,top,right,bottom)).convert('RGBA')

def blur_img(img:Image,level:int) -> ImageFile:
    return img.filter(ImageFilter.BoxBlur(level))

def gen_carplate(num,output,save_to_subdir,max_blur_level,format):
    # 获取基础图片文件
    base_img: ImageFile = get_base_img()

    # 循环生成指定数量的车牌图片
    for i in range(num):
        # 初始化车牌号码字符串
        carplate = ""
        # 复制基础图片以用于制作车牌
        carplate_img: ImageFile = base_img.copy()

        # 随机选择一个汉字作为行政区划简称
        admin_domain_index = random.randrange(0,len(SUPPORT_HANZI)-6)
        carplate += SUPPORT_HANZI[admin_domain_index]
        admin_domain_img = split_img(admin_domain_index,ImageType.HANZI)

        # 随机选择一个合规的ASCII字符作为机关代号
        organs_index = random.randrange(0,24)
        organs_img = split_img(organs_index,ImageType.ASCII)
        carplate += SUPPORT_ASCII[organs_index]

        # 将行政区划简称和机关代号图片粘贴到车牌图片上
        carplate_img.paste(admin_domain_img,(PLATE_HORIZONTAL_MARGIN,PLATE_VERTICAL_MARGIN),admin_domain_img)
        carplate_img.paste(organs_img,(PLATE_HORIZONTAL_MARGIN+SYMBOL_MARGIN+SYMBOL_WIDTH,PLATE_VERTICAL_MARGIN),organs_img)

        # 初始化序列号图片列表和序列号起始X坐标
        serial_symbol_imgs = []
        serial_symbols_start_x = PLATE_HORIZONTAL_MARGIN+3*SYMBOL_MARGIN+SYMBOL_WIDTH*2 + 10 * SCALER
        carplate += "_"

        # 生成并粘贴序列号图片
        for j in range(0,5):
            # 随机选择一个合规的ASCII字符作为序列号
            symbol_index = random.randrange(0,len(SUPPORT_ASCII))
            serial_symbol = split_img(symbol_index,ImageType.ASCII)
            # 将序列号图片添加到列表中
            serial_symbol_imgs.append(serial_symbol)
            # 将序列号图片粘贴到车牌图片上
            carplate_img.paste(serial_symbol,(serial_symbols_start_x + j * (SYMBOL_WIDTH + SYMBOL_MARGIN),PLATE_VERTICAL_MARGIN),serial_symbol)
            carplate += SUPPORT_ASCII[symbol_index]

        # 保存生成的车牌图片
        os.makedirs(output,exist_ok=True)
        if save_to_subdir:
            os.makedirs(f'{output}/{carplate}',exist_ok=True)
            carplate_img.convert('RGB').save(f'{output}/{carplate}/{carplate}.{format}',format=format)
            for level in range(1,max_blur_level+1):
                blur_img(carplate_img,level).convert('RGB').save(f'{output}/{carplate}/{carplate}_blur_{level}.{format}',format=format)
        else:
            carplate_img.convert('RGB').save(f'{output}/{carplate}.{format}',format=format)
            for level in range(1,max_blur_level+1):
                blur_img(carplate_img,level).convert('RGB').save(f'{output}/{carplate}_blur_{level}.{format}',format=format)
    ...

def gen_symbol(output,save_to_subdir,max_blur_level,format):
    def gen(sets, img_type:ImageType):
        symbol_ = sets[i]
        symbol_img = split_img(i, img_type)
        background_img = Image.new('RGBA', (1,1))
        background_img.putpixel((0,0), (0, 27, 122,255))
        background_img = background_img.resize(symbol_img.size)
        background_img.paste(symbol_img, (0,0), symbol_img)
        symbol_img = background_img
        if save_to_subdir:
            os.makedirs(f'{output}/{symbol_}',exist_ok=True)
            symbol_img.convert('RGB').save(f'{output}/{symbol_}/{symbol_}.{format}',format=format)
            for level in range(1,max_blur_level+1):
                blur_img(symbol_img,level).convert('RGB').save(f'{output}/{symbol_}/{symbol_}_blur_{level}.{format}',format=format)
        else:
            symbol_img.save(f'{output}/{symbol_}.{format}',format=format)
            for level in range(1,max_blur_level+1):
                blur_img(symbol_img,level).convert('RGB').save(f'{output}/{symbol_}_blur_{level}.{format}',format=format)
    # 循环生成指定数量的车牌图片
    for i in range(0,len(SUPPORT_ASCII)):
        gen(SUPPORT_ASCII,ImageType.ASCII)

    for i in range(0,len(SUPPORT_HANZI)-4):
        gen(SUPPORT_HANZI,ImageType.HANZI)

def main():
    # 接受参数
    parser = argparse.ArgumentParser()
    share_parser = argparse.ArgumentParser(add_help=False)
    share_parser.add_argument('-o','--output', type=str,metavar='路径', help='输出路径', default='./output')
    share_parser.add_argument('-s','--save_to_subdir',type=bool,choices=[True,False],help='是否保存到子目录',default=False)
    share_parser.add_argument('-b','--max_blur_level',type=int,metavar='整数',help='最大模糊程度',default=0)
    share_parser.add_argument('-f','--format',type=str,choices=['png','jpeg'],help='保存格式',default='png')

    type_parser = parser.add_subparsers(title='生成模式',dest='type')
    symbol_parser = type_parser.add_parser('symbol', help='生成独立符号', parents=[share_parser])

    carplate_parser = type_parser.add_parser('carplate', help='生成车牌', parents=[share_parser])
    carplate_parser.add_argument('-n','--num', type=int,metavar='整数', help='生成数量',required=True)

    args = parser.parse_args()

    output = args.output
    save_to_subdir = args.save_to_subdir
    max_blur_level = args.max_blur_level

    os.makedirs(output,exist_ok=True)

    print(args)

    match gen_type(args.type):
        case GenMode.SYMBOL:
            gen_symbol(output,save_to_subdir,max_blur_level,args.format)
        case GenMode.CARPLATE:
            gen_carplate(args.num,output,save_to_subdir,max_blur_level,args.format)



def gen_type(type_str):
    return GenMode[type_str.upper()]

if __name__ == '__main__':
    main()