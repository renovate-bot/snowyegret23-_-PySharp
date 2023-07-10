import struct
import sys
import csv
from CSData.data import *


def bin_extract():
    with open("data.bin", "rb") as f:
        with open("data.csv", "w", newline="", encoding="utf-8") as d:
            writer = csv.writer(d)
            entry_num = ReadInt16(f)
            for _ in range(entry_num):
                writer.writerow([ReadInt64(f), ReadString(f, "utf-8")])


def bin_repack():
    data_lst = [["1", "test1"], ["2", "test2"], ["-3", "test3"], ["4", "test4"]]
    with open("data_repack.bin", "wb") as f:
        WriteInt16(f, len(data_lst))
        for data in data_lst:
            WriteInt64(f, data[0])
            WriteString(f, data[1], "utf-8")


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
