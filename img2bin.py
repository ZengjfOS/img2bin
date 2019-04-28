#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
from os import walk
from PIL import Image

class BinHead:
    MAX_PICTURE_COUNT   = 100
    HEAD_SIZE           = 812       # 4 * 3 + 4 * 100 + 4 * 100
    OUTPUT_FILENAME     = "binArray"

    count = 0
    width = 0
    height = 0
    pictureOffsets = []
    pictureSizes = []

    @classmethod
    def int2bytes(cls, data):
        return data.to_bytes(4, byteorder="big")

    @classmethod
    def generateHead(cls):
        bytes = []
        bytes.extend(cls.int2bytes(cls.count))
        bytes.extend(cls.int2bytes(cls.width))
        bytes.extend(cls.int2bytes(cls.height))

        if len(cls.pictureOffsets) <= cls.MAX_PICTURE_COUNT:
            for offset in cls.pictureOffsets:
                bytes.extend(cls.int2bytes(offset))
            for offset in range(cls.MAX_PICTURE_COUNT - len(cls.pictureOffsets)):
                bytes.extend(cls.int2bytes(int(0)))
        else:
            for offset in range(cls.MAX_PICTURE_COUNT):
                bytes.extend(cls.int2bytes(cls.pictureOffsets[offset]))

        if len(cls.pictureSizes) <= cls.MAX_PICTURE_COUNT:
            for size in cls.pictureSizes:
                bytes.extend(cls.int2bytes(size))
            for size in range(cls.MAX_PICTURE_COUNT - len(cls.pictureSizes)):
                bytes.extend(cls.int2bytes(int(0)))
        else:
            for size in range(cls.MAX_PICTURE_COUNT):
                bytes.extend(cls.int2bytes(cls.pictureSizes[size]))

        print(bytes)
        # print(bytearray(bytes))
        # print(len(bytes))

        return bytearray(bytes)


    def __str__(self):
        return "count: " + str(self.count) + " width: " + str(self.width) + " height: " + str(self.height)

def bin2c(input, output):

    with open(input, 'rb') as fp_read:
        cnt = 0
        fp_write = open(output, 'w')

        arrayName = output.split(".")[0].split("/")[-1]
        fp_write.write('const unsigned char %s[] = {\n\t' % arrayName)

        while 1:
            binByte = fp_read.read(1)
            if len(binByte) > 0:
                cnt = cnt + 1
                fp_write.write("0x%02X," % int(ord(binByte)))
                if cnt % 8 == 0:
                    fp_write.write('\n\t')
                else:
                    fp_write.write(' ')
            else:
                fsize = os.path.getsize(input)
                if cnt == fsize:
                    print("C head file generate Success!")
                else:
                    print("C head file generate Failed!")
                break

        fp_write.write('\n};')
        fp_write.close()

def getFiles(file_dir):

    f = []

    for (dirpath, dirnames, filenames) in walk(file_dir) :
        pass

    for file in filenames:
        # print(file)
        f.append(file_dir + "/" + file)

    return f

def parseCMD() :
    parser = argparse.ArgumentParser(description='progrom description')
    parser.add_argument('-i', '--input', type=str, default="input", help="input image dir")
    parser.add_argument('-o', '--output', type=str, default="output", help="output image dir")
    parser.add_argument('-r', '--red', type=lambda x: int(x,0), default=-1, help="red")
    parser.add_argument('-g', '--green', type=lambda x: int(x,0), default=-1, help="green")
    parser.add_argument('-b', '--blue', type=lambda x: int(x,0), default=-1, help="blue")
    parser.add_argument('-f', '--fix', type=lambda x: int(x,0), default=5, help="fix read/green/blue value")
    parser.add_argument('-c', '--compression', action='store_true', help="do image compression")
    parser.add_argument('-d', '--decompression', action='store_true', help="do image decompression")

    args = parser.parse_args()
    # print(args.input)
    # print(args.compression)
    # print(args.decompression)
    # print(args.red)
    # print(args.green)
    # print(args.blue)

    return args, parser

def compression(args, files):

    dataArrays = []
    for image in files:
        BinHead.count += 1

        print("--------------------------------------")
        print("current deal image path: " + image)

        img = Image.open(image)  

        width, height = img.size
        BinHead.width = width
        BinHead.height = height
        print("size: " + str(width) + " x " + str(height))
        print("file format: " + img.format)
        print("deepth: " + img.mode)

        checkColorTypeFlag = False
        colorType = 0

        dataArray = []
        for row in range(height):
            for col in range(width):

                pix = img.getpixel((col, row))

                if args.red == -1 or args.green == -1 or args.blue == -1:
                    if pix[0] >= 0xC8 and pix[1] >= 0xC8 and pix[2] <= 0X0A:
                        # print("Color is: yellow")
                        checkColorTypeFlag = True
                        colorType = 2                   # yellow
                    elif pix[0] >= 0xC8 and pix[1] <= 0X0A and pix[2] <= 0X0A:
                        # print("Color is: red")
                        checkColorTypeFlag = True
                        colorType = 0                   # red
                    elif pix[0] <= 0x0A and pix[1] >= 0xC8 and pix[2] <= 0X0A:
                        # print("Color is: Green")
                        checkColorTypeFlag = True
                        colorType = 1                   # green
                    else:
                        pass
                    
                    if checkColorTypeFlag:
                        # print("0x%10x" % ((0xFF000000 | (row * BinHead.width + col)) << 8 | (colorType << 0x06)))
                        # print(((0xFF000000 | (row * binHead.width + col)) << 8 | (colorType << 0x06)).to_bytes(5, byteorder="little"))
                        dataArray.append(((0xFF000000 | (row * BinHead.width + col)) << 8 | (colorType << 0x06)).to_bytes(5, byteorder="big"))

                        checkColorTypeFlag = False

                elif pix[0] >= args.red - args.fix and pix[1] >= args.green - args.fix and pix[2] >= args.blue - args.fix:
                    # print(pix)
                    pass
                else:
                    pass

        dataArrays.append(dataArray)

    print("--------------------output-------------------")
    # generate bin file head info
    BinHead.pictureOffsets.append(int(BinHead.HEAD_SIZE))
    for index in range(len(dataArrays)):
        BinHead.pictureSizes.append(len(dataArrays[index]) * 5)
        BinHead.pictureOffsets.append(BinHead.pictureOffsets[index] + len(dataArrays[index]) * 5)

    outputFile = args.output + "/" + BinHead.OUTPUT_FILENAME + ".bin"
    binFile = open(outputFile, "wb")

    binFile.write(BinHead.generateHead())

    for datas in dataArrays:
        for data in datas:
            binFile.write(data)

    binFile.flush()
    binFile.close()

    bin2c(outputFile, outputFile.split(".")[0] + ".h")

def main():
    args, parser = parseCMD()

    if args.compression:
        print("do compression")

        files = getFiles(args.input)
        print(files)

        compression(args, files)

        pass
    elif args.decompression:
        print("do decompression")

        pass
    else:
        parser.print_help()
        exit(0)

if __name__ == '__main__':
    main()
