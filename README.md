# README

* 压缩红黄绿三色图片，并生成C程序需要的数据数据，存放在.h文件
* **程序目前只完成图片压缩红黄绿部分，解压及自定义颜色部分待续**

## 使用方法

* 将图片按数字编号顺序放入[input](input)目录；
* 生成的文件在[output](output)目录；
* 程序运行方法：
  * 程序使用Python3进行编码；
  * 依赖Pillow库；
  * 请执行`python3 img2bin -h`查看帮助信息；
    ```
    usage: img2bin.py [-h] [-i INPUT] [-o OUTPUT] [-r RED] [-g GREEN] [-b BLUE]
                      [-f FIX] [-c] [-d]

    progrom description

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            input image dir
      -o OUTPUT, --output OUTPUT
                            output image dir
      -r RED, --red RED     red
      -g GREEN, --green GREEN
                            green
      -b BLUE, --blue BLUE  blue
      -f FIX, --fix FIX     fix read/green/blue value
      -c, --compression     do image compression
      -d, --decompression   do image decompression
    ```