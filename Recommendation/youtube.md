#### YouTube Recommendations
[Deep Neural Networks for YouTube Recommendations](http://cseweb.ucsd.edu/classes/fa17/cse291-b/reading/p191-covington.pdf)

YouTube视频推荐的特点:数据量大，视频更新很快，数据非常稀疏且噪音比较大。

推荐系统的总体结构还是候选集合生成和打分排序两个部分，如下图:
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/1BE04C8AB58546D19E41B6A8613D3F97?ynotemdtimestamp=1534598811603)

##### Candidate Generation
候选集生成。这一部分负责根据用户和上下文信息从海量视频里得到几百个视频，早先一般都是用矩阵分解去做，而用NN去做则可以理解成是做的非线性的矩阵分解。
我们把推荐看作是一个分类问题。那么问题就是，给定用户U和上下文C，用户在时间t看的视频是i的概率为:
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/B698C1B7E53C47A8978C073B1559B9E6?ynotemdtimestamp=1534598811603)

这里的u是用户特征的embedding，v是候选视频的embedding。那么，接下来就是训练一个好的u。网络结构如下:
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/9905F7CF3E414153ADA508DA5319F520?ynotemdtimestamp=1534598811603)

网络的输入包括:用户浏览历史(视频序号id序列,进行embedding的average)，用户搜索历史(搜索内容序列，进行embedding的average)，geographic embedding(地理位置),example age(视频出现时间),gender(性别)等。输出的是用户的vector u,而后这个u按照上面的公式计算出softmax loss后进行训练。

这里因为softmax分类类别过多，采用了sample negative的方法来进行训练。没有使用分层分类，因为那样会使得一些毫不相干的类别聚类。具体采用的应该就是类似于word2vec方案里的那种negative sampling吧。

在serving的时候，需要使用输出的u和视频库里的视频计算得到top N个结果。这里也可以采用之前采用的hash的方法去做。(原文没有详细解释如何使用hash，猜测可能是和lsh一样?那么其实是需要一定程度上确保输出的u和视频的v都是同一个分布?总之不明确如何使用hash去做搜索)

论文提到将example age作为特征输入，并且实验结果证明加了这个特征后，模型输出的概率分布确实和实际情况的曲线类似了。不过，，，这里没明白怎么把这个特征输入。。。

##### 样本选择
训练数据使用了youtube上的所有视频观看记录，而不是推荐的视频的观看记录，否则的话面对新视频就很难推荐。还有一个要点就是对每个用户生成固定数量的训练样本，这样可以避免一部分活跃用户主导了损失方向。

其次，用户的搜索记录处理成无序的。举例来说，用户刚刚搜索了一个视频，那么我们的模型很可能会预测出用户刚刚搜索的这个视频，这显然不是一个好的预测，因为用户在搜索时已经看过或者决定不看了。所以这里把搜索记录处理成无序的。

再者，之前很多的协同过滤系统是将用户历史观看记录全部放到模型输入，取其中一个作为输出来预测。而我们认为这不是很自然，因为我们要预测的是用户下一个要看的视频。所以我们的采样方式如下:
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/E6770B1B95524FF3939BFE8C412666BF?ynotemdtimestamp=1534598811603)

##### Ranking
基本的模型结构和之前类似。
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/D6FF7B8EA5A5424EB0D209FA320361F6?ynotemdtimestamp=1534604934730)

这里有两个点需要注意。

一是连续特征归一化。具体归一化的方式是:![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/B34127BA5F2744218B457D80A12AC609?ynotemdtimestamp=1534603669935),并且还增加了x平方，x开方也作为输入来使得网络有更强的表达能力，并且实验证明这是有效的。

二是时间建模
###### Watch Time建模
模型的目标是给定了二分类结果后，还要预测用户的观看时间。这块不懂，后续看懂再写。。
