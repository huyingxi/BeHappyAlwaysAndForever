### gate attention and  add semantic relevance

##### 一: Modeling Human Reading with Neural Attention [Paper](https://arxiv.org/pdf/1608.05604.pdf)

​       将rnn cell里常见的update gate单独拎出来，使用hard attention来进一步实现。从而实现了在encoder过程中skip一些词的效果。

​      或者专注固执，或者视而不见，这种现象不光生活里有，在人们阅读时也是常见的。目前大多数model都集中于在predict过程中通过attention等方式来获取focus，而忽视了在encoder过程里也应该存在。（实际上无论gru还是lstm都是有update gate的，所以不能说完全没有考虑encoder过程中focus这个问题）。模型结构如下:

![20180811-1](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/1A5C08AEB59447448FE5FADA0FFE70FF?ynotemdtimestamp=1533991133017)

​       首先文章模型的目的似乎是要模拟人类阅读时忽视了哪些词和阅读需要的时间长短，所以模型在encoder每一个timestep上有一个predict distribution，也就是根据已经阅读的信息来predict下一个将要读到的词的distribution，称为PR。而后为了模拟阅读时常常跳过一些词，使用了一个hard attention称为A的东西来给出是否要读下一个词的binary predict。A的输入包括当前step的状态，当前step的PR，下一个将要读的词。

![20180811-2](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/156C552BC4034BE8A80FB3B49EA37E19?ynotemdtimestamp=1533991133017)

​      而PR自然也有自己的损失：

![20180811-3](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/F8A79475C021455EBA3A02AD3BC23CF3?ynotemdtimestamp=1533991133017)

​       那么在language model中总共的loss就是decoder的loss和上面这个的加和。

​      那么看这个论文的原因主要是另外一篇论文引用了它的这种在encoder过程里加上了gate attention部分。

##### 二:Improving Semantic Relevance for Sequence-to-Sequence Learning of Chinese Social Media Text Summarization [Paper](http://xueshu.baidu.com/s?wd=paperuri%3A%28445a1bdcad0e11eea8c09fe7d8cd965a%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Farxiv.org%2Fabs%2F1706.02459&ie=utf-8&sc_us=16357873022190972693)

​       文章指出abstract summary存在的主要问题是得到的summary和原文相似但是语义上相差很多。举了一个栗子:

![20180811-4](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/0D9AEC85B86B424CBFC7AFF5C25400B5?ynotemdtimestamp=1533991133017)

​         文章认为source texts和summary应该具备high semantic relevance，所以提出的model encourage high similarity between their represenation。模型如下:

![20180811-5](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/5648204D7DEE4C23B07101EF20215D85?ynotemdtimestamp=1533991133017)

​       模型包括encoder，decoder，similarity三部分，training objective是maximize the similarity score。那么就是两个问题，1.拿什么来表示source text和summary，2.用什么loss来度量similarity。

​       也就是在这里的encoder部分，借鉴了上一篇论文里的gate attention思路，每一个word都会被放到gated attention network里面来衡量它的重要性，具体来说在每个timestep，gate attention输入hidden state和word vector，输出score值，然后word vector乘以score后再fed into RNN encoder。在这里选择最后一个hidden state来表示source text。

​       在decoder过程里最后一个output是包含了both source text and generated summarizes的信息的，所以直接相减就可以得到summary的表示。如下，Vs表示summary，Sm是decoder的最后一个state，hN是encoder的最后一个state。

![20180811-6](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/FC24C701BD99438D8B04CE3C08EDACC8?ynotemdtimestamp=1533991133017)

​       那么第二个问题，如何衡量similarity。这里直接使用cosine similarity。相应的loss function自然就是原loss和该loss的加权。![20180811-7](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/11E287BEF2F54F038A9621CE20C82C7C?ynotemdtimestamp=1533991133017)

​       论文里将增加了Semantic Relevance Based neural model称为SRB，加了gate attention的称为SRB+Attention。实验部分是在中文数据集上做的。

![20180811-8](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/C527324CB4124948A114BB238366C71D?ynotemdtimestamp=1533991133017)

![1533991053084](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/1A8C5D3CA1D64365A4CB3ACB7D2FF128?ynotemdtimestamp=1533991133017)

