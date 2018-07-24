import time
import argparse
import unicodedata


def DBC2SBC(ustring):


    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if not (0x0021 <= inside_code and inside_code <= 0x7e):
            rstring += uchar
            continue
        rstring += chr(inside_code)
    return rstring


def save_seg_sentence(inputfile, output_senfile, output_idfile, space=False, output_senfile_space=None):

    start = time.time()
    punct = {'、': 0, '\\': 0, '!': 0, '！': 0, '，': 0, ',': 0, '。': 0, '：': 0, ':': 0, '；': 0, ';': 0, '-': 0, '.': 0,
             '（': 0, '）': 0, '(': 0, ')': 0, '～': 0, "~": 0, '%': 0, '{': 0, '}': 0, '/': 0, '"': 0, '’': 0, '‘': 0,
             '”': 0, '“': 0, '<': 0, '>': 0, '——': 0, '=': 0, '?': 0, '？': 0, '±': 0, '+': 0, '°': 0, "》": 0,
             '《': 0, '×': 0, "*": 0, '@': 0, "#": 0, '$': 0, '￥': 0, "&": 0, '′': 0, '〕': 0, '〔': 0, '_': 0, '】': 0,
             '【': 0, '[': 0, ']': 0, '|': 0, '③': 0, '—': 0, '≥': 0, '≤': 0, '②': 0,
             '': 0, '＂': 0}
    punct_nondot = {'、': 0, '\\': 0, '!': 0, '！': 0, '，': 0, ',': 0, '。': 0, '：': 0, ':': 0, '；': 0, ';': 0, '-': 0,
                    '～': 0, "~": 0, '%': 0, '{': 0, '}': 0, '"': 0, '’': 0, '‘': 0,
                    '”': 0, '“': 0, '?': 0, '？': 0, '±': 0, '+': 0, '°': 0, '×': 0,
                    "*": 0, '@': 0, "#": 0, '$': 0, '￥': 0, "&": 0, '′': 0, '〕': 0, '〔': 0, '_': 0, '[': 0, ']': 0,
                    '|': 0,
                    '①': 0, '②': 0, '③': 0, '④': 0, '⑤': 0, '⑥': 0, '⑦': 0, '⑧': 0, '⑨': 0, '⑩': 0, '⑪': 0, '⑫': 0,
                    '⑬': 0,
                    '⑮': 0, '⑱': 0, '″': 0, '/': 0, '（': 0, '）': 0, '(': 0, ')': 0, '】': 0, '【': 0, "》": 0, '《': 0,
                    '≥': 0, '≤': 0, '——': 0,
                    '—': 0, '<': 0, '>': 0, '=': 0, '　': 0
                    }
    if output_idfile is not None:
        fou_id = open(output_idfile, 'w', encoding='utf-8')
    if output_senfile_space is not None:
        fou_space = open(output_senfile_space, 'w', encoding='utf-8')
    with open(output_senfile, 'w', encoding='UTF-8') as fou_sen:
        with open(inputfile, 'r', encoding='UTF-8') as fin:

            for index, sen in enumerate(fin):
                sen = unicodedata.normalize('NFKC', sen)
                sen_nospace = sen
                sen_space = sen
                for key in punct.keys():
                    if not space:
                        sen_nospace = sen_nospace.replace(key, '')
                    else:
                        sen_nospace = sen_nospace.replace(key, ' ')
                if output_senfile_space is not None:
                    for key in punct.keys():
                        sen_space = sen_space.replace(key, ' ')
                    id2, sen_space = sen_space.split('\t')
                    fou_space.write(sen_space.strip() + '\n')
                id, sen = sen_nospace.split('\t')
                if index % 1000000 == 0:
                    print('已处理', index,'\t时间：', time.time() - start)
                fou_sen.write(sen.strip() + '\n')
                if output_idfile is not None:
                    fou_id.write(id.strip() + '\n')

    if output_idfile is not None:
        fou_id.close()
    if output_senfile_space is not None:
        fou_space.close()
    print('Removing unnecessary tokens, time:', time.time() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output_senfile', type=str)
    parser.add_argument('--output_idfile', type=str, default=None)
    parser.add_argument('--output_senfile_space', type=str, default=None)
    parser.add_argument('--space', type=int)
    args = parser.parse_args()
    save_seg_sentence(args.input, args.output_senfile, args.output_idfile, args.space, args.output_senfile_space)
