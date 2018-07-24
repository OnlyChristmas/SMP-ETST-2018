#!/bin/bash
EXPERIMENT="final_output/exp1"
SEG="final_output/seg"
if [ ! -d $EXPERIMENT ]; then
  mkdir -p $EXPERIMENT
fi
if [ ! -d ${SEG} ]; then
  mkdir -p ${SEG}
fi
#
python3 remove_tokens.py --input final_corpus/A数据集.txt --output_senfile ${SEG}/train_sen.txt  --space 0 --output_senfile_space ${SEG}/train_sen_space.txt --output_idfile ${SEG}/train_id_space.txt
#
if [ ! -d ${SEG}/train_split/ ]; then
  mkdir -p ${SEG}/train_split/
fi
split -l 1500000 ${SEG}/train_sen.txt ${SEG}/train_split/train_split
THULAC/thulac -seg_only -model_dir models/ -input ${SEG}/train_split/train_splitaa -output ${SEG}/train_split/train_seg_thuaa.txt
THULAC/thulac -seg_only -model_dir models/ -input ${SEG}/train_split/train_splitab -output ${SEG}/train_split/train_seg_thuab.txt
THULAC/thulac -seg_only -model_dir models/ -input ${SEG}/train_split/train_splitac -output ${SEG}/train_split/train_seg_thuac.txt
THULAC/thulac -seg_only -model_dir models/ -input ${SEG}/train_split/train_splitad -output ${SEG}/train_split/train_seg_thuad.txt
cat ${SEG}/train_split/train_seg_thuaa.txt ${SEG}/train_split/train_seg_thuab.txt ${SEG}/train_split/train_seg_thuac.txt ${SEG}/train_split/train_seg_thuad.txt > ${SEG}/train_seg_thu_nonpunct.txt
#
cppjieba-master/build/load_test -i ${SEG}/train_sen_space.txt -o ${SEG}/train_seg_jieba.txt
#
python3 prepro_df.py --input ${SEG}/train_seg_thu_nonpunct.txt --output_df ${SEG}/df_thu.p --output_idf ${SEG}/idf_thu.p
python3 prepro_df.py --input ${SEG}/train_seg_jieba.txt --output_idf ${SEG}/idf_jieba.p
python3 save_iip_T1.py --df_file ${SEG}/df_thu.p  --train_seg_file  ${SEG}/train_seg_thu_nonpunct.txt  --tmp_file ${SEG}/iip_set_data.p --outfile  ${SEG}/iip_tmp.p