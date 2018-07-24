# -*- coding: utf-8 -*-
"""
@Time     2018/7/13 18:04
@Author   bw_Zhang
@Software PyCharm
"""
import time
import pickle
import argparse
from six.moves import cPickle


def inverted_index_preprocess(iip_set_data, iip_tmp_file, test_seg_file, train_seg_file, outfile):
    start = time.time()
    filtered_df_data = cPickle.load(open(iip_tmp_file, "rb"))
    set_data = cPickle.load(open(iip_set_data, "rb"))

    total = 0
    filtered_sents = []
    count = 0

    with open(test_seg_file, encoding='utf8') as f:
        for index, line in enumerate(f):
            words = line.strip().split()
            words_set = set(words)
            output = set()
            for w in words:
                if w in filtered_df_data:
                    output = output.union(filtered_df_data[w])

            final_output = []
            for sent_ind in output:
                if len(words_set) > 20:
                    if len(set_data[sent_ind].intersection(words_set)) / len(words_set) > 0.4:
                        final_output.append(sent_ind)
                elif len(words_set) > 10:
                    if len(set_data[sent_ind].intersection(words_set)) / len(words_set) > 0.3:
                        final_output.append(sent_ind)
                else:
                    if len(set_data[sent_ind].intersection(words_set)) >= 1:
                        final_output.append(sent_ind)

            if index % 400 == 0:
                print('已构造索引 test_seg :', index, '\t时间：', time.time() - start)

            total += len(final_output)
            filtered_sents.append(final_output)
            count += 1

    tst_dict = {}
    with open(test_seg_file, encoding='utf8') as f:
        for index, line in enumerate(f):
            line = ''.join(line.strip().split())
            tst_dict[line] = tst_dict.get(line, []) + [index]

    tst_dict = {k: v for k, v in tst_dict.items() if len(v) > 1}

    with open(train_seg_file, encoding='utf8') as f:
        for index, line in enumerate(f):
            words = ''.join(line.strip().split())
            flag = False
            for k, v in tst_dict.items():
                if k != words:
                    continue
                else:
                    for tst_i in v:
                        filtered_sents[tst_i].append(index)
                    flag = True
            if flag:
                tst_dict.pop(words, None)
            if len(tst_dict) == 0:
                print(index)
                break

    cPickle.dump(filtered_sents, open(outfile, 'wb'), protocol=cPickle.HIGHEST_PROTOCOL)

    print('average sentences for test', total / (count))
    print('time for preprocessing', time.time() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iip_set_data', type=str)
    parser.add_argument('--iip_tmp_file', type=str)
    parser.add_argument('--test_seg_file', type=str)
    parser.add_argument('--train_seg_file', type=str)
    parser.add_argument('--outfile', type=str)
    args = parser.parse_args()

    inverted_index_preprocess(iip_set_data=args.iip_set_data, iip_tmp_file=args.iip_tmp_file,
                              test_seg_file=args.test_seg_file, train_seg_file=args.train_seg_file,
                              outfile=args.outfile)

