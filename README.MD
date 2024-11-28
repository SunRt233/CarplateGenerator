# 车牌生成器

## 简介
这是一个用于生成车牌图片的工具。支持生成独立的符号图片和完整的车牌图片，并可以设置模糊程度和保存格式。


## 安装
确保你已经安装了 Python 和所需的库。你可以使用以下命令安装所需的库：

```sh 
pip install pillow argparse
```

## 使用方法

本工具支持两种生成模式：
- `symbol`: 生成独立的符号图片。
- `carplate`: 生成完整的车牌图片。

### 生成车牌

```sh
python CarPlateGenerator.py carplate -n 10 -o ./output -s True -b 2 -f png
```
#### 参数详细说明
- `-o`, `--output` `<路径>`:
  - **描述**: 指定输出目录的路径。
  - **默认值**: `./output`
- `-s`, `--save_to_subdir` `<布尔值>`:
  - **描述**: 如果设置为 `True`，则每个生成的图片将保存在单独的子目录中。
  - **默认值**: `False`
- `-b`, `--max_blur_level` `<整数>`:
  - **描述**: 设置生成图片的最大模糊程度。范围为 `0` 到任意正整数。
  - **默认值**: `0`
- `-f`, `--format` `<格式>`:
  - **描述**: 设置生成图片的保存格式，可选值为 `png` 或 `jpeg`。
  - **默认值**: `png`
- `-n`, `--num` `<整数>`:
  - **描述**: 在 `carplate` 模式下，指定生成的车牌数量。
  - **必需**: 是


### 生成独立符号
```shell
python CarPlateGenerator.py symbol -o ./output -s True -b 2 -f png
```

#### 参数详细说明
- `-o`, `--output` `<路径>`: 指定输出目录的路径。默认为 `./output`。
- `-s`, `--save_to_subdir` `<布尔值>`: 是否保存到子目录。默认为 `False`。
- `-b`, `--max_blur_level` `<整数>`: 设置生成图片的最大模糊程度。默认为 `0`。
- `-f`, `--format` `<格式>`: 设置生成图片的保存格式，可选值为 `png` 或 `jpeg`。默认为 `png`。

## 代码结构
- `CarPlateGenerator.py`: 主程序文件，包含命令行参数解析和生成逻辑。
- `assets/`: 存放生成车牌所需的基础图片资源。

## 贡献
欢迎贡献代码和提出改进建议！请遵循项目的贡献指南。

## 许可证
本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE) 文件。