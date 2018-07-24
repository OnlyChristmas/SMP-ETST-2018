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
python3 remove_tokens.py --input final_corpus/B数据集.txt --output_senfile ${SEG}/tst_sen.txt  --space 0
python3 remove_tokens.py --input final_corpus/B数据集.txt --output_senfile ${SEG}/tst_sen_space.txt --output_idfile ${SEG}/tst_id_space.txt --space 1
#
THULAC/thulac -seg_only -model_dir models/ -input ${SEG}/tst_sen.txt -output ${SEG}/tst_seg_thu_nonpunct.txt
cppjieba-master/build/load_test -i ${SEG}/tst_sen_space.txt -o ${SEG}/tst_seg_jieba.txt
python3 save_iip_T2.py --iip_set_data ${SEG}/iip_set_data.p  --iip_tmp_file ${SEG}/iip_tmp.p  --test_seg_file  ${SEG}/tst_seg_thu_nonpunct.txt  --train_seg_file  ${SEG}/train_seg_thu_nonpunct.txt  --outfile  ${SEG}/iip.p
#
python3 main.py --output ${EXPERIMENT}/test_thu.csv   --iip_file ${SEG}/iip.p  --inputStandard  ${SEG}/train_id_space.txt --inputPreAlign final_corpus/B数据集.txt --inputStandard_seg ${SEG}/train_seg_thu_nonpunct.txt --inputPreAlign_seg ${SEG}/tst_seg_thu_nonpunct.txt --df_file ${SEG}/df_thu.p --idf_file ${SEG}/idf_thu.p --output2 ${EXPERIMENT}/test_jieba.csv --inputStandard2 ${SEG}/train_id_space.txt --inputStandard_seg2 ${SEG}/train_seg_jieba.txt --inputPreAlign_seg2 ${SEG}/tst_seg_jieba.txt --idf_file2 ${SEG}/idf_jieba.p
python3 combine_json.py --input1 ${EXPERIMENT}/test_thu.csv.sentence --input2 ${EXPERIMENT}/test_jieba.csv.sentence --output ${EXPERIMENT}/result.csv --df_file ${SEG}/df_thu.p
