# -*- coding: utf-8 -*-
"""
@Time     2018/6/9 15:41
@Author   bw_Zhang
@Software PyCharm
"""

import os
import numpy as np
import pickle
import operator
import time
import argparse
import datetime
import heapq
import json
import shutil




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
    cbleu_p = float(numerator) / float(denominator)
    if not bp:
        return cbleu_p
    if len(candidate) > len(ref):
        BP = 1
    else:
        BP = np.exp(1 - float(len(ref)) / len(candidate))
    BLEU = BP * cbleu_p

    return BLEU


def BLEROUDER(candidate, ref, df_data=None, df_nonexist=11.508355):
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
    cbleu_p = float(numerator) / float(denominator)
    if len(candidate) > len(ref):
        BP = 1
    else:
        BP = np.exp(1 - float(len(ref)) / len(candidate))

    denominator = 0.0
    numerator = 0.0
    for k, v in ref_count.items():
        df = df_data[k] if k in df_data else df_nonexist
        denominator += v * df
        if k in cand_count:
            numerator += min(ref_count[k], cand_count[k]) * df
            # numerator += count_df_prod[k] if k in count_df_prod else min(cand_count[k], ref_count[k]) * df
    crouge_p = float(numerator) / float(denominator)
    if len(ref) > len(candidate):
        BP_r = 1
    else:
        BP_r = np.exp(1 - float(len(candidate)) / len(ref))
    BLEU = BP * cbleu_p  # np.exp(np.log(cbleu_p + 1e-10))
    ROUGE = crouge_p  #BP_r *

    return (2 * BLEU * ROUGE) / (BLEU + ROUGE + 1e-5)


def single_process_align_2(inputStandard, inputPreAlign, inputStandard_seg, inputPreAlign_seg, output,
                           df_file, idf_file, sent_file_name,
                           inputStandard_seg2, inputPreAlign_seg2, output2, idf_file2,
                           sent_file_name2, iip_file, anchor_threshold=0.5, sentence_file=True):
    start = time.time()
    with open(inputPreAlign, 'r', encoding='UTF-8') as fin_PreAlign:
        orig_PreAlign = fin_PreAlign.readlines()
    with open(inputStandard, 'r', encoding='UTF-8') as fin_Standard:
        orig_Stardard = fin_Standard.readlines()
    with open(inputStandard_seg, 'r', encoding='UTF-8') as fin_Standard_seg:
        seg_Stardard = fin_Standard_seg.readlines()
    with open(inputPreAlign_seg, 'r', encoding='UTF-8') as fin_PreAlign_seg:
        seg_PreAlign = fin_PreAlign_seg.readlines()

    # filtered_sents = inverted_index_preprocess(df_file=df_file, train_seg_file=inputStandard_seg,
    #                                            test_seg_file=inputPreAlign_seg)

    filtered_sents = pickle.load(open(iip_file, "rb"))

    new_filtered_sents = []

    fou = open(output, 'w', encoding='UTF-8')
    fou.writelines("test_id,result\n")
    df_data = pickle.load(open(idf_file, 'rb'))
    df_nonexist = np.log(df_data['ref_len'])
    df_data = df_data['document_frequency']
    len_Align = len(orig_PreAlign)
    print('Loading Data Time', time.time() - start)

    if sentence_file:
        sent_out = open(sent_file_name, 'w')
        sent_dict = {}

    for i in range(len_Align):
        new_filtered_sents.append([])
        BLEUscore_dict = {}
        seg_ref = seg_PreAlign[i].strip().split()
        for j in range(len(filtered_sents[i])):
            BLEUscore_dict[j] = BLEROUDER(seg_ref, seg_Stardard[filtered_sents[i][j]].strip().split(), df_data,
                                          df_nonexist)
            if BLEUscore_dict[j] > 0.15:
                new_filtered_sents[-1].append(filtered_sents[i][j])
        if len(BLEUscore_dict) == 0:
            max_score = 0
        else:
            standard_loc, max_score = max(BLEUscore_dict.items(), key=operator.itemgetter(1))
            anchor_threshold = 0.481


        if max_score >= anchor_threshold:
            fou.writelines(
                orig_PreAlign[i].split('\t')[0] + "," + orig_Stardard[filtered_sents[i][standard_loc]])

        else:
            fou.writelines(orig_PreAlign[i].split('\t')[0] + ",null\n")

        if sentence_file:
            sent_tmp = {}
            if max_score == 0:
                tgt_id, tgt_sent = orig_PreAlign[i].strip().split('\t')
                sent_tmp['selected'] = 'null'
                sent_tmp['tgt_sent'] = tgt_sent
                sent_tmp['tgt_seg'] = seg_PreAlign[i].strip()
                # sent_tmp['src_sent'] = 'null'
                sent_tmp['src_id'] = 'null'
                sent_tmp['src_seg'] = 'null'
                sent_tmp['tgt_index'] = i
                sent_tmp['src_index'] = -1
                sent_tmp['tgt_id'] = tgt_id
                sent_tmp['score'] = 0
                sent_tmp['bleu'] = 0
                sent_tmp['rouge'] = 0
            else:
                # src_id, src_sent = orig_Stardard[filtered_sents[i][standard_loc]].strip().split('\t')
                src_id = orig_Stardard[filtered_sents[i][standard_loc]].strip()
                tgt_id, tgt_sent = orig_PreAlign[i].strip().split('\t')
                # sent_tmp['src_sent'] = src_sent
                sent_tmp['src_id'] = src_id
                if max_score > anchor_threshold:
                    sent_tmp['selected'] = src_id
                else:
                    sent_tmp['selected'] = 'null'
                sent_tmp['tgt_seg'] = seg_PreAlign[i].strip()
                sent_tmp['src_seg'] = seg_Stardard[filtered_sents[i][standard_loc]].strip()
                sent_tmp['score'] = max_score
                sent_tmp['tgt_index'] = i
                sent_tmp['src_index'] = filtered_sents[i][standard_loc]
                sent_tmp['tgt_id'] = tgt_id
                sent_tmp['tgt_sent'] = tgt_sent
                sent_tmp['bleu'] = 0
                sent_tmp['rouge'] = 0
            sent_dict[i] = sent_tmp

        if i % 400 == 0:
            print('一次对齐 :', i, '\t时间：', time.time() - start)

    if sentence_file:
        json.dump(sent_dict, sent_out)
    fou.close()

    with open(inputStandard_seg2, 'r', encoding='UTF-8') as fin_Standard_seg:
        seg_Stardard = fin_Standard_seg.readlines()
    with open(inputPreAlign_seg2, 'r', encoding='UTF-8') as fin_PreAlign_seg:
        seg_PreAlign = fin_PreAlign_seg.readlines()

    fou = open(output2, 'w', encoding='UTF-8')
    fou.writelines("test_id,result\n")
    df_data = pickle.load(open(idf_file2, 'rb'))
    df_nonexist = np.log(df_data['ref_len'])
    df_data = df_data['document_frequency']
    len_Align = len(orig_PreAlign)
    print('Loading Data Time', time.time() - start)
    print('average num of sentences', sum([len(_) for _ in new_filtered_sents]) / len(new_filtered_sents))
    if sentence_file:
        sent_out = open(sent_file_name2, 'w')
        sent_dict = {}

    for i in range(len_Align):
        BLEUscore_dict = {}
        seg_ref = seg_PreAlign[i].strip().split()
        for j in range(len(new_filtered_sents[i])):
            BLEUscore_dict[j] = BLEROUDER(seg_ref, seg_Stardard[new_filtered_sents[i][j]].strip().split(), df_data,
                                          df_nonexist)

        if len(BLEUscore_dict) == 0:
            max_score = 0
        else:
            standard_loc, max_score = max(BLEUscore_dict.items(), key=operator.itemgetter(1))
            anchor_threshold = 0.481

        if max_score >= anchor_threshold:
            fou.writelines(
                orig_PreAlign[i].split('\t')[0] + "," + orig_Stardard[new_filtered_sents[i][standard_loc]])

        else:
            fou.writelines(orig_PreAlign[i].split('\t')[0] + ",null\n")

        if sentence_file:
            sent_tmp = {}
            if max_score == 0:
                tgt_id, tgt_sent = orig_PreAlign[i].strip().split('\t')
                sent_tmp['selected'] = 'null'
                sent_tmp['tgt_sent'] = tgt_sent
                sent_tmp['tgt_seg'] = seg_PreAlign[i].strip()
                # sent_tmp['src_sent'] = 'null'
                sent_tmp['src_id'] = 'null'
                sent_tmp['src_seg'] = 'null'
                sent_tmp['tgt_index'] = i
                sent_tmp['src_index'] = -1
                sent_tmp['tgt_id'] = tgt_id
                sent_tmp['score'] = 0
                sent_tmp['bleu'] = 0
                sent_tmp['rouge'] = 0
            else:
                # src_id, src_sent = orig_Stardard[new_filtered_sents[i][standard_loc]].strip().split('\t')
                src_id = orig_Stardard[new_filtered_sents[i][standard_loc]].strip()
                tgt_id, tgt_sent = orig_PreAlign[i].strip().split('\t')
                # sent_tmp['src_sent'] = src_sent
                if max_score > anchor_threshold:
                    sent_tmp['selected'] = src_id
                else:
                    sent_tmp['selected'] = 'null'

                sent_tmp['tgt_seg'] = seg_PreAlign[i].strip()
                sent_tmp['src_seg'] = seg_Stardard[new_filtered_sents[i][standard_loc]].strip()
                sent_tmp['score'] = max_score
                sent_tmp['src_id'] = src_id
                sent_tmp['tgt_index'] = i
                sent_tmp['src_index'] = new_filtered_sents[i][standard_loc]
                sent_tmp['tgt_id'] = tgt_id
                sent_tmp['tgt_sent'] = tgt_sent
                sent_tmp['bleu'] = 0
                sent_tmp['rouge'] = 0
            sent_dict[i] = sent_tmp

        if i % 400 == 0:
            print('二次对齐 :', i, '\t时间：', time.time() - start)

    if sentence_file:
        json.dump(sent_dict, sent_out)
    fou.close()
    print('Processing time', time.time() - start)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputStandard', type=str, default='./corpus/源句子.txt')
    parser.add_argument('--inputPreAlign', type=str, default='./corpus/待判定句子.txt')
    parser.add_argument('--inputStandard_seg', type=str)
    parser.add_argument('--inputPreAlign_seg', type=str)
    parser.add_argument('--df_file', type=str)
    parser.add_argument('--idf_file', type=str)
    parser.add_argument('--iip_file', type=str, default='')
    parser.add_argument('--output', type=str, default="./result.csv")

    parser.add_argument('--inputStandard2', type=str, default='./corpus/源句子.txt')
    parser.add_argument('--inputPreAlign2', type=str, default='./corpus/待判定句子.txt')
    parser.add_argument('--inputStandard_seg2', type=str)
    parser.add_argument('--inputPreAlign_seg2', type=str)
    parser.add_argument('--df_file2', type=str, default=None)
    parser.add_argument('--idf_file2', type=str)
    parser.add_argument('--output2', type=str, default="./result.csv")
    args = parser.parse_args()


    single_process_align_2(inputStandard=args.inputStandard, inputPreAlign=args.inputPreAlign,
                           inputStandard_seg=args.inputStandard_seg,
                           inputPreAlign_seg=args.inputPreAlign_seg, output=args.output,
                           df_file=args.df_file, idf_file=args.idf_file, anchor_threshold=0.45,
                           sentence_file=True, sent_file_name=args.output + '.sentence',
                           inputStandard_seg2=args.inputStandard_seg2,
                           inputPreAlign_seg2=args.inputPreAlign_seg2, iip_file=args.iip_file,
                           output2=args.output2,
                           idf_file2=args.idf_file2, sent_file_name2=args.output2 + '.sentence')
