def from_num(d, fill=0):
  bits = bin(d)[2:]
  if fill > 0:
    bits = bits.zfill(fill)
  return bits

def from_char(c):
  return from_num(ord(c), fill=8)

def permutations(bit_count):
  return [from_num(i).zfill(bit_count) for i in range(2**bit_count)]