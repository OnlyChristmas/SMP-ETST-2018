import json
import argparse
import pickle
import numpy as np


def BLEUDER(candidate, ref, df_data=None, df_nonexist=11.508355, bp=True):
    ref_count = dict()
    for word in ref:
        ref_count[word] = ref_count.get(word, 0) + 1
    cand_count = dict()
    for word in candidate:
        cand_count[word] = cand_count.get(word, 0) + 1

    denominator = 0.0
    numerator = 0.0
    for k, v in cand_count.items():
        df = df_data[k] if k in df_data else df_nonexist
        denominator += v * df
        if k in ref_count:
            numerator += min(ref_count[k], cand_count[k]) * df
    cbleu_p = float(numerator)/float(denominator)
    if not bp:
        return cbleu_p
    if len(candidate) > len(ref):
        BP = 1
    else:
        BP = np.exp(1 - float(len(ref))/len(candidate))
    BLEU = cbleu_p#BP #*

    return BLEU


def remove_no_digit(w):
    s = ""
    for c in w:
        if c.isdigit():
            s += c
    return s

def remove_no_alpha(w):
    s = ""
    if isinstance(w, list):
        for word in w:
            for c in word:
                if ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z'):
                    s += c
        return s
    for c in w:
        if ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z'):
            s += c
    return s

def combine_json(thu_file, jieba_file, output_file, df_file=None):
    df_file = pickle.load(open(df_file, 'rb'))
    df_data = df_file['document_frequency']
    df_nonexists = np.log(df_file['ref_len'])
    num_dict = ['五','六','七','八','九','十','百','千','万']
    num_dict1 = ['一','二', '三','四','五','六','七','八','九','十','百','千','万','亿']

    thu_out = json.load(open(thu_file, encoding='utf8'))
    jieba_out = json.load(open(jieba_file, encoding='utf8'))

    final_out = open(output_file, 'w', encoding='utf8')
    final_out.write("test_id,result\n")

    new_out = {}
    for i in range(len(thu_out)):


        thu_item = thu_out[str(i)]
        jieba_item = jieba_out[str(i)]
        new_out[i] = thu_item['selected']

        src_seg = thu_item['src_seg'].strip().split()
        tgt_seg = thu_item['tgt_seg'].strip().split()


        jieba_flag = False

        if thu_item['selected'] != jieba_item['selected'] and (float(jieba_item['score']) < 0.3085 or float(jieba_item['score']) > 0.55):
            jieba_flag = True
            new_out[i] = jieba_item['selected']

        if jieba_flag:
            tgt_seg = jieba_item['tgt_seg'].split()
            src_seg = jieba_item['src_seg'].split()

        else:
            tgt_seg = thu_item['tgt_seg'].split()
            src_seg = thu_item['src_seg'].split()
        score = max(float(thu_item['score']), float(jieba_item['score']))

        ifselected = new_out[i] != 'null'

        remove_flag = False

        if not ifselected and BLEUDER(jieba_item['tgt_seg'].strip().split(),  jieba_item['src_seg'].strip().split(),df_file, df_nonexists) > 0.65 and not remove_flag:
            new_out[i] = jieba_item['src_id'] if jieba_flag and 'src_id' in jieba_item else thu_item['src_id']


        digits = []
        for w in tgt_seg:
            if w[0].isdigit() or w[-1].isdigit():
                digits.append(remove_no_digit(w))
        dflag = True
        for w in digits:
            if (len(w) == 1 or w =='10') and len(set(''.join(src_seg)).intersection(set(num_dict1))) >= 1:
                continue
            if w not in src_seg and w not in remove_no_digit(''.join(src_seg)):
                dflag = False
        if len(digits) > 1 and not dflag and ifselected and score < 0.745:  #
            new_out[i] = 'null'
            remove_flag = True

        ifselected = new_out[i] != 'null'
        score = max(float(thu_item['score']), float(jieba_item['score']))

        digits = {}
        for w in src_seg:
            if w[0].isdigit() or w[-1].isdigit():
                digits[remove_no_digit(w)] = 1
        dflag = True
        count = 0
        for w in digits:
            if (len(w) == 1 or w == '10') and len(set(''.join(tgt_seg)).intersection(set(num_dict1))) >= 1:
                break
            if w not in ''.join(tgt_seg):#
                dflag = False
                count += 1
        if len(digits) >= 1 and not dflag and count and  score < 0.57 and ifselected:  #
            new_out[i] = 'null'
            remove_flag = True


        digits = {}
        for w in src_seg:
            if w[0].isdigit():
                digits[w] = 1
        count = 0
        for w in digits:
            if (len(w) == 1 or w =='10') and len(set(''.join(tgt_seg)).intersection(set(num_dict1))) >= 1:
                continue
            if w in ''.join(tgt_seg):
                continue
            if w not in tgt_seg:
                count += 1

        score = max(float(thu_item['score']), float(jieba_item['score']))
        if len(digits) >= 1 and float(score) + 0.05 * len(digits) - 0.2 * (count) > 0.51 and not ifselected and not remove_flag and score > 0.3:
            print(digits, score, float(score) + 0.05 * len(digits) - 0.2 * (count), ' '.join(src_seg) + '\n', ' '.join(tgt_seg))
            new_out[i] = jieba_item['src_id'] if jieba_flag and 'src_id' in jieba_item else thu_item['src_id']

        ifselected = new_out[i] != 'null'


        digits = []
        for w in src_seg:
            if w[0].isdigit() or w[-1].isdigit():
                digits.append(remove_no_digit(w))

        for w in num_dict:
            if w in ''.join(tgt_seg):
                digits = []
        dflag = True
        for w in digits:
            if (len(w) == 1 or w == '10') and len(set(''.join(tgt_seg)).intersection(set(num_dict))) >= 1:
                continue
            if w == 'P005001':
                continue
            if w not in tgt_seg and w not in remove_no_digit(''.join(tgt_seg)):
                dflag = False
        if len(digits) > 1 and not dflag and ifselected and score < 0.73:
            new_out[i] = 'null'
            remove_flag = True

        ifselected = new_out[i] != 'null'


        digits = []
        for w in src_seg:
            if w[0].isdigit():
                digits.append(w)
        dflag = True
        for w in digits:
            if w not in tgt_seg:
                dflag = False
        digits = []
        for w in tgt_seg:
            if w[0].isdigit():
                digits.append(w)
        for w in digits:
            if w not in src_seg:
                dflag = False
        if len(digits) > 1 and dflag and not ifselected and score > 0.3:
            new_out[i] = jieba_item['src_id'] if jieba_flag and 'src_id' in jieba_item else thu_item['src_id']

        ifselected = new_out[i] != 'null'


    count = 0
    for k, v in new_out.items():
        tgt_id = thu_out[str(k)]['tgt_id']
        final_out.write(str(tgt_id)+','+str(v)+'\n')
        if v.strip() != thu_out[str(k)]['selected'].strip():
            count += 1
    print(count)

    final_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input1', type=str, default='./final_output/exp/test_thu.csv.sentence')
    parser.add_argument('--input2', type=str, default='./final_output/exp/test_jieba.csv.sentence')
    parser.add_argument('--output', type=str, default="./final_output/exp/result_combined_nobp.csv")
    parser.add_argument('--df_file', type=str, default='./final_output/seg/df_thu.p')

    args = parser.parse_args()
    combine_json(args.input1, args.input2, args.output, args.df_file)
