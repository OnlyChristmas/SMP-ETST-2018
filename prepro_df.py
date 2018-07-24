from six.moves import cPickle
import time
import numpy as np
import argparse


def prepro_df(input_file, output_df_file, output_idf_file):
    start = time.time()
    df = dict()
    count_lines = 0
    with open(input_file, 'r', encoding='utf8') as f:
        for i, line in enumerate(f):
            count_lines += 1
            tokens = line.strip().split()
            tmp = dict()
            for token in tokens:
                tmp[token] = 1
            for k in tmp:
                df[k] = df.get(k,0) + 1
    num_lines = count_lines + 1
    print('number of lines', num_lines)
    logs = dict()
    df_log = dict()

    for k,v in df.items():
        if v in logs:
            df_log[k] = logs[v]
        else:
            ans = np.log(num_lines/v)
            df_log[k] = ans
            logs[v] = ans

    if output_df_file is not None:
        cPickle.dump({'document_frequency': df, 'ref_len': count_lines}, open(output_df_file, 'wb'), protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump({'document_frequency': df_log, 'ref_len': count_lines}, open(output_idf_file, 'wb'), protocol=cPickle.HIGHEST_PROTOCOL)
    print(time.time() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output_df', type=str, default=None)
    parser.add_argument('--output_idf', type=str)
    args = parser.parse_args()
    prepro_df(args.input, args.output_df, args.output_idf)