import struct

# <:리틀엔디안 / >:빅엔디안
# B:1바이트 / H:2바이트 / I:4바이트 / Q:8바이트
# ?:bool / f:float / d:double / s:char[]
# 대문자: 부호있음(signed) / 소문자(unsigned): 부호없음
# 출처: https://docs.python.org/ko/3/library/struct.html
# C#의 경우 대부분 리틀엔디안이 디폴트


# Int
def ReadInt16(f, big=False):
    if big == True:
        return struct.unpack(">h", f.read(2))[0]
    else:
        return struct.unpack("<h", f.read(2))[0]


def WriteInt16(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0x7FFF:
        raise Exception("Int16 overflow")
    if big == True:
        f.write(struct.pack(">h", number))
    else:
        f.write(struct.pack("<h", number))


def ReadInt32(f, big=False):
    if big == True:
        return struct.unpack(">i", f.read(4))[0]
    else:
        return struct.unpack("<i", f.read(4))[0]


def WriteInt32(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0x7FFFFFFF:
        raise Exception("Int32 overflow")
    if big == True:
        f.write(struct.pack(">i", number))
    else:
        f.write(struct.pack("<i", number))


def ReadInt64(f, big=False):
    if big == True:
        return struct.unpack(">q", f.read(8))[0]
    else:
        return struct.unpack("<q", f.read(8))[0]


def WriteInt64(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0x7FFFFFFFFFFFFFFF:
        raise Exception("Int64 overflow")
    if big == True:
        f.write(struct.pack(">q", number))
    else:
        f.write(struct.pack("<q", number))


# UInt
def ReadUInt16(f, big=False):
    if big == True:
        return struct.unpack(">H", f.read(2))[0]
    else:
        return struct.unpack("<H", f.read(2))[0]


def WriteUInt16(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0xFFFF:
        raise Exception("UInt16 overflow")
    if big == True:
        f.write(struct.pack(">H", number))
    else:
        f.write(struct.pack("<H", number))


def ReadUInt32(f, big=False):
    if big == True:
        return struct.unpack(">I", f.read(4))[0]
    else:
        return struct.unpack("<I", f.read(4))[0]


def WriteUInt32(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0xFFFFFFFF:
        raise Exception("UInt32 overflow")
    if big == True:
        f.write(struct.pack(">I", number))
    else:
        f.write(struct.pack("<I", number))


def ReadUInt64(f, big=False):
    if big == True:
        return struct.unpack(">Q", f.read(8))[0]
    else:
        return struct.unpack("<Q", f.read(8))[0]


def WriteUInt64(f, number, big=False):
    if isinstance(number, str):
        number = int(number)
    if number > 0xFFFFFFFFFFFFFFFF:
        raise Exception("UInt64 overflow")
    if big == True:
        f.write(struct.pack(">Q", number))
    else:
        f.write(struct.pack("<Q", number))


# String
# code from SYSTEM.IO.BINARYREADER
def Read7BitEncodedInt(f):
    var1 = 0
    var2 = 0
    for i in range(5):
        b = int.from_bytes(f.read(1), byteorder="little")
        var1 |= (b & 0x7F) << var2
        var2 += 7
        if (b & (0x80)) == 0 and i < 5:
            return var1
        elif 5 <= i:
            raise IOError(
                "Too many bytes in what should have been a 7 bit encoded Int32."
            )


def ReadString(f, encoding):
    num = Read7BitEncodedInt(f)
    if num is None:
        raise IOError("Read7BitEncodedInt returned None")
    if num < 0:
        raise IOError("Invalid binary file (string len < 0)")
    if num == 0:
        return ""
    string_bytes = f.read(num)
    return string_bytes.decode(encoding)


# 출처: https://cafe.naver.com/hansicgu/29903, "행복한나라"님
def WriteString(f, text, encoding):
    encoded_text = text.encode(encoding)
    text_size = len(encoded_text)
    if text_size < 0x7F:
        f.write(struct.pack("B", text_size))
    elif 0x7F <= text_size <= 0xFF:
        f.write(struct.pack("B", text_size))
        f.write(struct.pack("B", 0x01))
    elif 0xFF < text_size:
        add_value = text_size // 0x80
        sync2 = text_size - (0x40 * add_value)
        if add_value >= 0x02:
            f.write(struct.pack("B", sync2 - (0x40 * (add_value)) + 0x80))
        else:
            f.write(struct.pack("B", sync2 - (0x40 * (add_value))))
        f.write(struct.pack("B", add_value))
    if text_size > 0:
        f.write(encoded_text)
