import math

# Определение таблицы констант
const = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

# Циклические сдвиги для раундов
s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

# Инициализаци 32-битных регистров (А, B, C, D,)
init_vect = [
    0x67452301,
    0xefcdab89,
    0x98badcfe,
    0x10325476
]


def fun_F(b, c, d):
    return (b & c) | (~b & d)


def fun_G(b, c, d):
    return (d & b) | (~d & c)


def fun_H(b, c, d):
    return b ^ c ^ d


def fun_I(b, c, d):
    return c ^ (b | ~d)


def divideOnBlocks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def chunkDivide(block, chunks):
    result = []
    size = len(block) // chunks
    for i in range(0, chunks):
        result.append(block[i * size:(i + 1) * size])
    return result


def define_round(i, B, C, D):  # Определение функции и раунда в текущем этапе
    function = ''
    k = 0
    # k номер 32-битного слова текущего 512-битного блока сообщения
    if 0 <= i <= 15:
        k = i
        function = fun_F(B, C, D)
    elif 16 <= i <= 31:
        k = (i * 5 + 1) % 16
        function = fun_G(B, C, D)
    elif 32 <= i <= 47:
        k = (i * 3 + 5) % 16
        function = fun_H(B, C, D)
    elif 48 <= i <= 63:
        k = (i * 7) % 16
        function = fun_I(B, C, D)
    return k, function


def left_shift(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(msg):
    msg = bytearray(msg)
    msg_len_bits = (len(msg) * 8) % (2 ** 64)  # 64-битное представление длины данных до выравнивания, для этапа 2
    msg += b'\x80'  # Добавление бита со значением 1, оставшиеся биты заполняются нулями

    while len(msg) % 64 != 56:  # Этап 1. Добавление недостающих битов
        msg += b'\x00'

    msg += msg_len_bits.to_bytes(8, byteorder='little')  # Этап 2. Добавление длины

    blocks = divideOnBlocks(msg, 64)  # Делим на блоки по 512 бит

    registers = init_vect[:]  # 128-битовый буфер для хранения результатов промежуточных вычислений
    for block in blocks:
        chunks = chunkDivide(block, 16) # Каждый блок делится на 16 cлов по 32 бита
        A, B, C, D = registers
        for i in range(64):
            k, F = define_round(i, B, C, D)
            X = int.from_bytes(chunks[k], byteorder='little')
            T = const[i]
            new_B = (B + left_shift((A + F + T + X), s[i])) & 0xFFFFFFFF
            A, B, C, D = D, new_B, B, C

        registers[0] += A
        registers[1] += B
        registers[2] += C
        registers[3] += D

        for elem in registers:
            elem &= 0xFFFFFFFF
        # for i, val in enumerate([A, B, C, D]):
        #     registers[i] += val
        #     registers[i] &= 0xFFFFFFFF
    return sum(elem << (32 * i) for i, elem in enumerate(registers))


def md5_to_hex(dig):
    raw = dig.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

# Solution # 1
#def md5_to_hex(dig):
#    try:
#        raw = dig.to_bytes(16, byteorder='little')
#    except:
#        dig = "0" + str(hex(dig))[2:]
#        dig = int(dig[2:],16)
#        raw = dig.to_bytes(16, byteorder='little')
#    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

# Solution #2
#def md5_to_hex(dig):
#    try:
#        raw = dig.to_bytes(16, byteorder='little')
#    except:
#        dig = dig - 340282366920938463463374607431768211456
#        raw = dig.to_bytes(16, byteorder='little')
#    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))


def start_md5(message):
    enc_message = message.encode("utf-8")
    return md5_to_hex(md5(enc_message))

