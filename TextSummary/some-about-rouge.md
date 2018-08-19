

#### Rouge工具
##### ROUGE的公式:
![image](https://images0.cnblogs.com/blog/520267/201411/121636425387678.png)
其中，n-gram表示n元词，{Ref Summaries}表示参考摘要，即事先获得的标准摘要，Countmatch(n-gram)表示系统摘要和参考摘要中同时出现n-gram的个数，Count(n-gram)则表示参考摘要中出现的n- gram个数。

不难看出，ROUGE公式是由召回率的计算公式演变而来的，分子可以看作“检出的相关文档数目”，即系统生成摘要与标准摘要相匹配的N-gram个数，分母可以看作“相关文档数目”，即标准摘要中所有的N-gram个数。

不过实际中一般会使用召回和精准的调和平均。

前期因为安装pyrouge出了一堆问题，没有正确安装好，所幸后面发现了sumeval，一个比较方便使用的评估Rouge工具。[github链接](https://github.com/chakki-works/sumeval).

一般来说sumeval可以使用，不过在与一些论文的结果比对时可能还是需要使用ROUGE。

##### sumeval使用
sumeval评估Rouge需要初始化一个rouge对象，如下:

```
from sumeval.metrics.rouge import RougeCalculator
rouge = RougeCalculator(stopwords=True, lang="en")
rouge_1 = rouge.rouge_n(
            summary="I went to the Mars from my living town.",
            references="I went to Mars",
            n=1)
```
其中stopwords设置为True表明会先去掉stopword后再计算Rouge。该初始化还有其他参数,如下:

```
    "stopwords": true,
    "stemming": false,
    "word_limit": -1,
    "length_limit": -1,
    "alpha": 0.5,
    "tokenizer":None
```
其含义解释如下:

```python
#stopwords：设置成True则会从ref和summ里都去除stopwords。
if self.stopwords:
    words = [w for w in words if not self.lang.is_stop_word(w)]
#stemming:设置成True的话，会读取一个stemming.txt的文件，
#里面将一个词转换为另一个标准词·例如"went-go".
#不过不修改sumeval源码的话，原代码里只讲summ里的词替换
#颇有不妥，且读取stemming.txt的代码也存在明显问题。
if self.stemming and is_reference:
    words = [self.lang.stemming(w, min_length=3) for w in words]
#word_limit：设置为大于0的值的话对直接截断长度。
if self.word_limit > 0:
    words = words[:self.word_limit]
#length_limit：char级别的长度截断，此处没有考虑加上单词间的空格。
#alpha:对于rouge-n来说，会计算召回和精准，#alpha作为调和平均数的权重，具体公式为:
F = 1/(alpha * (1/P) + (1 - alpha) * (1/R))

#tokenizer：如果没有设置的话，sumeval会使用默认自己的tokenize进行分词。这样看来的话，为了统一似乎最好自己传入tokenize。
if self.tokenizer:
    words = self.tokenizer.tokenize(text_or_words)
else:
    words = self.lang.tokenize(text_or_words)
```


###### sumeval的结果和pyrouge是否相同?
sumeval相比于Rouge来说好用一些，且有代码，可以方便的查看原理和修改。虽然sumeval的readme中有提到使用pyrouge结果作为对比，不过实际上似乎二者得到的结果是不同的。

这可能主要是由于stemming的处理和alpha参数选择的不同。这个[issue](https://github.com/google/seq2seq/issues/89)里提到了ROUGE在计算score前进行了一系列的操作，所以往往其他包得不到与ROUGE一模一样的score。

##### pyrouge安装
在这一步卡了有些时日，还放弃过一段时间。
下面是正确的安装方法:

[原始blog链接](https://blog.csdn.net/wr339988/article/details/70165090)
下面是对上面blog内容的简述。

首先是下载一些需要的软件包[下载链接](https://pan.baidu.com/s/15EtAkQ6i24FBw3y2M2hStw)。

1. 检查perl版本，需要在5.6.0以上。命令:`perl -v`
2. 安装XML:Parser和XML:RegExp
   
```python
tar -zxvf XML-Parser-2.44.tar.gz
cd XML-Parser-2.44
perl Makefile.PL 
make 
make test
sudo make install
#然后RegExp也是一样的步骤
```

3. 安装LWP::UserAgent和XML::Parser::PerlSAX。而后按照step2的方法，安装XML::DOM.

```python
sudo apt-get update
sudo apt-get install libwww-perl
sudo apt-get install libxml-perl
#然后DOM安装和step2步骤一样
#如果报错的话输入下面两行
sudo apt-get install -f
sudo apt-get update --fix-missing 
```
4.安装DB_File

```python
#步骤和step2里一样，如果如下报错:
version.c:30:16: fatal error: db.h: 没有那个文件或目录
compilation terminated.
Makefile:360: recipe for target 'version.o' failed
make: *** [version.o] Error 1
#则说明未安装Berkeley DB library，或安装不正确。解决方法如下：

sudo apt-get install libdb-dev
#如果还没有用，可能是没有安装对应的版本，先使用
sudo apt-cache search libdb
#查看当前Berkeley DB library 的版本，然后再安装对应的版本.
sudo apt-get install libdb5.3-dev
```

5.设置ROUGE环境变量

```python
#在/etc/profile里加下面一行:
export ROUGE_EVAL_HOME="$ROUGE_EVAL_HOME:/usr/local/RELEASE-1.5.5/data"
#具体路径按照实际情况替换哦
```
6.测试ROUGE是否安装成功

```python
#进入ROUGE文件的路径，运行
perl runROUGE-test.pl
#不报错就完成了。
```
7.安装pyrouge

```python
#不要使用pip直接安装
git clone https://github.com/bheinzerling/pyrouge
cd pyrouge
python setup.py install
#设置下ROUGE路径
pyrouge_set_rouge_path /absolute/path/to/ROUGE-1.5.5/directory
或者
r = Rouge155('/absolute/path/to/ROUGE-1.5.5/directory')
#测试一下
python -m pyrouge.test
#不报错就说明完成了
```

