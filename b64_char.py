import bitops
from b64_common import *

bits_to_chars_table = {
  "000000": "A",
  "000001": "B",
  "000010": "C",
  "000011": "D",
  "000100": "E",
  "000101": "F",
  "000110": "G",
  "000111": "H",
  "001000": "I",
  "001001": "J",
  "001010": "K",
  "001011": "L",
  "001100": "M",
  "001101": "N",
  "001110": "O",
  "001111": "P",
  "010000": "Q",
  "010001": "R",
  "010010": "S",
  "010011": "T",
  "010100": "U",
  "010101": "V",
  "010110": "W",
  "010111": "X",
  "011000": "Y",
  "011001": "Z",
  "011010": "a",
  "011011": "b",
  "011100": "c",
  "011101": "d",
  "011110": "e",
  "011111": "f",
  "100000": "g",
  "100001": "h",
  "100010": "i",
  "100011": "j",
  "100100": "k",
  "100101": "l",
  "100110": "m",
  "100111": "n",
  "101000": "o",
  "101001": "p",
  "101010": "q",
  "101011": "r",
  "101100": "s",
  "101101": "t",
  "101110": "u",
  "101111": "v",
  "110000": "w",
  "110001": "x",
  "110010": "y",
  "110011": "z",
  "110100": "0",
  "110101": "1",
  "110110": "2",
  "110111": "3",
  "111000": "4",
  "111001": "5",
  "111010": "6",
  "111011": "7",
  "111100": "8",
  "111101": "9",
  "111110": "+",
  "111111": "/"
}

char_to_bits_table = {
  "A": "000000",
  "B": "000001",
  "C": "000010",
  "D": "000011",
  "E": "000100",
  "F": "000101",
  "G": "000110",
  "H": "000111",
  "I": "001000",
  "J": "001001",
  "K": "001010",
  "L": "001011",
  "M": "001100",
  "N": "001101",
  "O": "001110",
  "P": "001111",
  "Q": "010000",
  "R": "010001",
  "S": "010010",
  "T": "010011",
  "U": "010100",
  "V": "010101",
  "W": "010110",
  "X": "010111",
  "Y": "011000",
  "Z": "011001",
  "a": "011010",
  "b": "011011",
  "c": "011100",
  "d": "011101",
  "e": "011110",
  "f": "011111",
  "g": "100000",
  "h": "100001",
  "i": "100010",
  "j": "100011",
  "k": "100100",
  "l": "100101",
  "m": "100110",
  "n": "100111",
  "o": "101000",
  "p": "101001",
  "q": "101010",
  "r": "101011",
  "s": "101100",
  "t": "101101",
  "u": "101110",
  "v": "101111",
  "w": "110000",
  "x": "110001",
  "y": "110010",
  "z": "110011",
  "0": "110100",
  "1": "110101",
  "2": "110110",
  "3": "110111",
  "4": "111000",
  "5": "111001",
  "6": "111010",
  "7": "111011",
  "8": "111100",
  "9": "111101",
  "+": "111110",
  "/": "111111"
}

def bits_to_char(b):
  return bits_to_chars_table[b]

def char_to_bits(c):
  return char_to_bits_table[c]

def all_chars(with_padding=False):
  padding = [padding_char] if with_padding else []
  return list(char_to_bits_table.keys()) + padding

def bit_options_given_n_msbits(bits):
  n_bits = len(bits)
  assert n_bits < 6, "unexpected number of bits"
  n_rest = 6 - n_bits
  rest_opts = bitops.permutations(n_rest)
  return [bits + o for o in rest_opts]

def bit_options_given_n_lsbits(bits):
  n_bits = len(bits)
  assert n_bits < 6, "unexpected number of bits"
  n_rest = 6 - n_bits
  rest_opts = bitops.permutations(n_rest)
  return [o + bits for o in rest_opts]

def char_options_given_n_msbits(bits):
  return [bits_to_char(c) for c in bit_options_given_n_msbits(bits)]

def char_options_given_n_lsbits(bits):
  return [bits_to_char(c) for c in bit_options_given_n_lsbits(bits)]

def zero_aligned_char_options(c):
  ''' given a 0-aligned char c, find the possible values of the 2 encoded chars representing it.

      for a string cXY (where c is zero aligned in the ascii string), we get:
      [6 ms bits of c][2 lsbits of c + 4 msbits of X][4 lsbits of X + 2 msbits of Y][6 lsbits of Y]
  '''
  bits = bitops.from_char(c)
  first, second = bits[:6], bits[6:]
  return (
    [bits_to_char(first)],
    char_options_given_n_msbits(second),
  )

def one_aligned_char_options(c):
  ''' given a 1-aligned char c, find the possible values of the 2 encoded chars representing it.

      for a string XcY (where X is zero aligned in the ascii string), we get:
      [6 ms bits of X][2 lsbits of X + 4 msbits of c][4 lsbits of c + 2 msbits of Y][6 lsbits of Y]
  '''
  bits = bitops.from_char(c)
  first, second = bits[:4], bits[4:]
  return (
    char_options_given_n_lsbits(first),
    char_options_given_n_msbits(second),
  )

def two_aligned_char_options(c):
  ''' given a 2-aligned char c, find the possible values of the 2 encoded chars representing it.

      for a string XYc (where X is zero aligned in the ascii string), we get:
      [6 ms bits of X][2 lsbits of X + 4 msbits of Y][4 lsbits of Y + 2 msbits of c][6 lsbits of c]
  '''
  bits = bitops.from_char(c)
  first, second = bits[:2], bits[2:]
  return (
    char_options_given_n_lsbits(first),
    [bits_to_char(second)],
  )

def char_options(c, index):
  ''' get the list of encoded options for an ascii char,
      given a char and its index in the ascii string '''
  if alignment_of_index_ascii(index) == 0:
    return zero_aligned_char_options(c)
  elif alignment_of_index_ascii(index) == 1:
    return one_aligned_char_options(c)
  else:
    return two_aligned_char_options(c)

def common_options(l1, l2):
  ''' select only options that are common to two sets '''
  return list(set(l1) & set(l2))

def options_of_two_chars(c1, c2, index):
  ''' get the list of options for 2 ascii chars, given the index of the first in the ascii string.
      returns a 3 option sets (does not accept chars from crossing groups)
  '''
  first, second1 = char_options(c1, index)
  second2, third = char_options(c2, index+1)
  alignment = alignment_of_index_ascii(index) 

  if alignment == 0:
    # ABx ==> [a1, a2b1, b2x1, x2] ==> [a1, a2b1, b2x1]
    return [first, common_options(second1, second2), third]
  elif alignment == 1:
    # xAB ==> [x1, x2a1, a2b1, b2] ==> [x2a1, a2b1, b2]
    return [first, common_options(second1, second2), third]
  else:
    # xyA Bqp => [x1, x2y1, y2a1, a1] + [a2, a2p1, p2q1, q2]
    raise RuntimeError("should not try to combine options from different encoded groups")