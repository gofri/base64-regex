import base64
import re
import b64

any_b64 = r'[A-Za-z0-9+/]'
any_b64_padding = r'[A-Za-z0-9+/=]'

def _quantify_mutli(options, pattern, mod):
    size = len(options)
    count = size // mod
    if count > 1:
        pattern += r'{' + str(count) + r'}'
    return pattern

def _options_to_regex(options):
    ''' 
        the ugly tricks:
        1. if it's a single option, just use the char.
        2. if we had multiple any_char or any_char_with_padding,
            we squashed them in generate_regex_for_index.
            so here we just find them (multiples of either 64/64 respectively),
            and replace them with a shortened pattern.
        4. otherwise - a set of options [...]
    '''
    if len(options) == 1:
        return options[0]
    elif len(options) % b64.all_chars_len == 0:
        return _quantify_mutli(options, any_b64, b64.all_chars_len)
    elif len(options) % b64.all_chars_with_padding_len == 0:
        return _quantify_mutli(options, any_b64_padding, b64.all_chars_with_padding_len)
    else:
        return r'[' + ''.join(options) + r']'

def _option_set_to_regex(opset):
    return ''.join(_options_to_regex(o) for o in opset)

def _generate_regex_for_index(parts, index):
    '''
        the ugly trick: if we have any_char / any_char_with_padding,
        we squash them together so that we can generate a thin pattern for them later 
    '''
    opset = b64.generate_option_sets(parts, index)
    new_opset = []
    in_all = False
    in_all_padded = False
    for o in opset:
        now_in_all = len(o) == b64.all_chars_len
        now_in_all_padded = len(o) == b64.all_chars_with_padding_len
        if (in_all and now_in_all) or (in_all_padded and now_in_all_padded):
            new_opset[-1] = new_opset[-1] + o
        else:
            new_opset.append(o)
        in_all = now_in_all 
        in_all_padded = now_in_all_padded

    return _option_set_to_regex(new_opset)

def generate_regex(parts):
    per_index = (_generate_regex_for_index(parts, i) for i in range(b64.ascii_group_size))
    return '|'.join(f'{r}' for r in per_index)

if __name__ == '__main__':
    import string
    import random

    def rand_str(cnt, letters=None):
        letters = letters if letters else string.ascii_letters
        return ''.join(random.choice(letters) for i in range(cnt))

    def inject_str(what, into):
        at = random.randint(0, len(into) - 1)
        return into[:at] + what + into[at:]

    def rand_pat():
        opts = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return 'ghp_' + rand_str(36, opts)

    ascii_pattern = r'ghp_[A-Za-z0-9]{36}'
    pattern = generate_regex(['ghp_', 36])
    my_pat = rand_pat()

    print('pat:', my_pat)
    print('pattern:', pattern, len(pattern))

    test_count = 1000
    for i in range(test_count):
        text = inject_str(my_pat, rand_str(100))
        extracted_from_src = re.findall(ascii_pattern, text)[0]
        encoded = base64.b64encode(text.encode('ascii')).decode('ascii')
        res = re.findall(pattern, encoded)[0]
        decoded = base64.b64decode(res).decode('ascii')

        extracted = re.findall(ascii_pattern, decoded)[0]
        assert extracted == extracted_from_src