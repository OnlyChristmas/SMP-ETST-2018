# -*- coding: utf-8 -*-
"""
@Time     2018/7/1 14:54
@Author   bw_Zhang
@Software PyCharm
"""
import time
import pickle
import argparse
from six.moves import cPickle


def inverted_index_preprocess(df_file, train_seg_file, tmp_file , outfile):
    start = time.time()
    df_data = pickle.load(open(df_file, 'rb'))['document_frequency']

    filtered_df = {k: 1 for k, v in df_data.items() if v < 8000}
    filtered_df_short = {k: 1 for k, v in df_data.items() if v < 20000}
    filtered_df_data = {k: set() for k, v in df_data.items() if v < 20000}
    set_data = {}
    with open(train_seg_file, encoding='utf8') as f:
        for index, line in enumerate(f):
            words = line.strip().split()
            original_words = words
            words = [_ for _ in words if _ in filtered_df]
            set_data[index] = set(original_words)

            if index % 1000000 == 0:
                print('已处理 train_seg :', index, '\t时间：', time.time() - start)

            if len(words) > 5:
                for w in words:
                    if w in filtered_df:
                        filtered_df_data[w].add(index)
            else:
                for w in original_words:
                    if w in filtered_df_short:
                        filtered_df_data[w].add(index)

    cPickle.dump(filtered_df_data, open(outfile, 'wb'), protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(set_data, open(tmp_file, 'wb'), protocol=cPickle.HIGHEST_PROTOCOL)
                  




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--df_file', type=str)
    parser.add_argument('--train_seg_file', type=str)
    parser.add_argument('--tmp_file', type=str)
    parser.add_argument('--outfile', type=str)
    args = parser.parse_args()

    inverted_index_preprocess(df_file=args.df_file, tmp_file=args.tmp_file ,train_seg_file=args.train_seg_file,outfile=args.outfile)

