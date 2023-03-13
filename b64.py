import base64
import textwrap
import b64_char
from b64_common import *

def _break_string_into_encoded_groups(s, index):
  ''' break an ascii string into a list of strings,
      such that each of substring ends up in the same encoded group,
      where an encoded group is a set of 4 encoded chars that are related.'''
  pre = []
  tail_len = b64_char.missing_to_alignment_ascii(index)
  if tail_len > 0:
    # chop the unaligned begginning which is the first group
    pre = [s[:tail_len]]
    s = s[tail_len:]

  return pre + textwrap.wrap(s, width=3)

def _option_sets_for_group(group, index):
  ''' given a group or a subgroup (1 to 3 ascii chars) and the index of its leading char,
      provide a list of lists, representing possible encoded values for all of it chars.
      group of 1 ==> 2 option sets
      group of 2 ==> 3 option sets
      group of 3 ==> 4 option sets (practically, always definite, so each set is of length 1)
      '''
  alignment = alignment_of_index_ascii(index)
  if len(group) == 3:
    assert alignment == 0, "unexpected alignment of full group"
    return [[chr(c)] for c in base64.standard_b64encode(group.encode('ascii'))]
  elif len(group) == 2:
    return b64_char.options_of_two_chars(group[0], group[1], index)
  elif len(group) == 1:
    return b64_char.char_options(group[0], index)
  else:
    raise RuntimeError(f"unexpected group len {len(group)} of group {group}")

def _option_sets_for_string(s, index):
  ''' given a string and the index of its leading char, provide a list of lists,
      representing possible values for all of it chars.'''
  groups = _break_string_into_encoded_groups(s, index)
  options = []
  for g in groups:
    options += _option_sets_for_group(g, index)
    index += len(g)
  return options

def _option_sets_for_any(count, index):
  ''' get the option set for a given count of any ascii chars '''
  placeholder = '.'
  groups = _break_string_into_encoded_groups(placeholder * count, index)
  options = []
  for g in groups:
    options += (len(g)+1) * [b64_char.all_chars()]
  return options

def _merge_option_sets(left, right, index):
  ''' merge two option sets, given the index of the leading char in the left set. '''
  if len(left) == 0:
    return right
  elif len(right) == 0:
    return left

  # XXX:
  # index is ascii-wise, so first calculate using ascii.
  index_alignment = alignment_of_index_ascii(index)

  # the option-set is encoded-wise, so calculate using encoded.
  cross_alignment = alignment_of_index_encoded(index_alignment + len(left))

  if cross_alignment == 0: # independent groups - just append
    return left + right
  else: # cross point is shared between both - merge it
    cross = b64_char.common_options(left[-1], right[0])
    return left[:-1] + [cross] + right[1:]

def _bound_option_set(option_set, index):
  ''' add preceding and succeeding chars to complete a valid base64 encoding. '''
  alignment = alignment_of_index_ascii(index)

  # add prefix if missing
  pre = [b64_char.all_chars()] * alignment
  option_set = pre + option_set

  # add suffix if missing
  new_tail_len = b64_char.missing_to_alignment_encoded(len(option_set))
  post = [b64_char.all_chars(with_padding=True)] * new_tail_len
  option_set += post

  return option_set

def generate_option_sets(parts, index):
  ''' generate the option sets for any sequence of fixed strings and any-string-count,
      given the index of the first char in the ascii string.
  '''
  i = index

  merged = []
  for p in parts:
    if isinstance(p, int):
      new_opset = _option_sets_for_any(p, i)
      size = p
    elif isinstance(p, str):
      new_opset = _option_sets_for_string(p, i)
      size = len(p)
    else:
      raise RuntimeError("unexpected part {p}")
    
    merged = _merge_option_sets(merged, new_opset, index)
    i += size

  return _bound_option_set(merged, index)

if __name__ == '__main__':
  for index in range(3):
    print('-------------', index, '--------------')
    merged = []
    x = 'abcd'
    i = index
    op = _option_sets_for_string(x, i)
    print('pre x', x, i, len(op), len(x))
    merged = _merge_option_sets(merged, op, index)
    i += len(x)
    print('post x', len(merged), i)
    print('-')

    count_any = 4
    op = _option_sets_for_any(count_any, i)
    print('pre any', count_any, i, len(op), count_any)
    merged = _merge_option_sets(merged, op, index)
    i += count_any
    print('post any', len(merged), i)
    print('-')

    y = 'black'
    op = _option_sets_for_string(y, i)
    print('pre y', y, i, len(op), len(y))
    merged = _merge_option_sets(merged, op, index)
    i += len(y)
    print('post y', len(merged), i)
    print('-')

    count_more = 2
    op = _option_sets_for_any(count_more, i)
    print('pre more', count_more, i, len(op), count_more)
    merged = _merge_option_sets(merged, op, index)
    i += count_more
    print('post more', len(merged), i)
    print('---')

    complete_set = _bound_option_set(merged, index)
    alt = generate_option_sets([x, count_any, y, count_more], index)

    print('---')
    print('comp', len(complete_set), [len(x) for x in complete_set])
    print('alt', len(alt), [len(x) for x in alt])

    print('---')
    assert len(alt) == len(complete_set)
    assert alt == complete_set
    import random
    o1 = [random.choice(o) for o in alt]
    s = base64.b64decode(''.join(o1).encode('ascii'))
    print(s, len(s))
