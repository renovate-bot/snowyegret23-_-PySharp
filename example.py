import struct
import sys
import csv
from PySharp.Binary import *


def bin_extract():
    with open("data.bin", "rb") as f:
        with open("data.csv", "w", newline="", encoding="utf-8") as d:
            writer = csv.writer(d)
            entry_num = ReadInt16(f)
            for _ in range(entry_num):
                writer.writerow([ReadInt64(f), ReadString(f, "utf-8")])


def bin_repack():
    with open("data.csv", "r", newline="", encoding="utf-8") as f:
        with open("data_repack.bin", "wb") as d:
            csv_list = list(csv.reader(f))
            WriteInt16(d, len(csv_list))
            for i in range(len(csv_list)):
                WriteInt64(d, csv_list[i][0])
                WriteString(d, csv_list[i][1], "utf-8")


def same_check():
    with open("data.bin", "rb") as f:
        original = f.read()
    with open("data_repack.bin", "rb") as f:
        repack = f.read()
    if original == repack:
        print("same")
    else:
        print("different")


bin_extract()
bin_repack()
same_check()
