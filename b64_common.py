padding_char = '='
ascii_group_size = 3
encoded_group_size = 4
all_chars_len = 64
all_chars_with_padding_len = 65

def alignment_of_index_ascii(index):
  return index % ascii_group_size

def missing_to_alignment_ascii(length):
  return (ascii_group_size - (length % ascii_group_size)) % ascii_group_size

def alignment_of_index_encoded(index):
  return index % encoded_group_size

def missing_to_alignment_encoded(length):
  return (encoded_group_size - (length % encoded_group_size)) % encoded_group_size
