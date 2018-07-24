
SMP_ETST 2018 christmas源码

时间：2018年7月1日

---

#### 算法简介
本方法的核心算法WFTS(Weighted F-measure-based method for text sourcing)为基于TF-IDF的句子相似度的度量。我们提出了一种简便、快速的句子相似度的计算方法。通过计算待查句子词语和源句子词语基于TF-IDF加权的的改良版的查准率和查全率，最终计算出由TF-IDF加权的F1-score得分，为两个句子相似度的度量方法。F1-score得分能够比较全面的衡量句子间词语的匹配程度，而TF-IDF可以更好地建模词语的重要程度。为了加快搜索速度，我们采用了倒排索引技术进行预选，通过词语迅速对源数据集的的句子进行检索。最后，我们结合jieba分词和THULAC分词的结果做了模型融合。




#### 代码功能

- 数据预处理部分
  1. remove_tokens.py:去除一些不必要的标点符号、特殊符号，去除空格，全角字符转半角字符，将数据的每行句子ID与句子分开。
  1. 调用THULAC进行分词（由于THULAC不支持大文件的切词，我们将A数据集文件切成4份分别切词）
  1. 调用cpp-jieba进行分词
  1. prepro_df.py:计算源数据集的词语的文档频率（document frequency）和逆文档频率（IDF）。
  1. 建立源数据集的倒排索引表。
- 文本溯源算法部分：
  1. main.py 主算法文件
  2. combine_json.py 合并中间文件，生成最终结果

---

#### 运行环境参考
- Intel(R) Xeon(R) CPU E5-2697 v4 @ 2.30GHz
- 内存 200 GB
- Linux version 3.10.0-514.el7.x86_64
- gcc version 4.8.5 20150623 (Red Hat 4.8.5-11)
- Python 3.4.5



#### 运行时间参考
我们在多种不同Linux环境下运行程序，下面是我们的平均运行时间。

1. 最终测试集
  - 预处理总时间 1267秒 （21.1分钟)
    - 数据集去特殊符号: 218秒
    - THULAC分词：272秒
    - jieba分词：112秒
    - 计算TF-IDF 164秒
    - 建倒排索引表 501秒
  - 核心算法 115秒 (1.9分钟）
2. 验证集
  - 数据预处理（加载源数据集到开始检测）时间约为：28秒
  - 算法运行（开始检测到得出最终结果）时间约为：7秒
  - 总用时： 35秒

---


#### 使用说明
- [数据下载](https://pan.baidu.com/s/1khlXOI5YZY8-x2tNFVoeUA)  密码：`5164`
- 将数据文件"A数据集.txt"和"B数据集"的UTF-8格式文件放在主目录final_corpus文件夹下。
- 自行下载[C++ THULAC](https://github.com/thunlp/THULAC)编译, 文件夹命名为“THULAC”，放在项目根目录下。
- 下载[THULAC训练好的模型](http://thulac.thunlp.org/message_v1_1), 命名为“models”放在根目录下。
- 下载[cppjieba-master](https://github.com/yanyiwu/cppjieba)并编译，文件夹命名为“cppjieba-master”, 放在根目录下。
- 顺次运行 T1_part.sh, T2_part.sh
- 最终结果为final_output/exp1/result.csv  这里的exp1是本次实验的输出文件夹



#### 注意事项
- 程序运行需要大量的内存空间（？>32GB）
- THULAC不支持大文件的切词，我们将A数据集文件切成4份分别切词。
- 由于THULAC分词软件本身未知bug，可能`core dump`，自行下载[C++ THULAC](https://github.com/thunlp/THULAC)编译,可以解决。




#### License
[BSD]() © [christmas](https://github.com/OnlyChristmas)
