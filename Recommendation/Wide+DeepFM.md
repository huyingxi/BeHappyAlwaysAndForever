模型本身没有什么可说的其实。主要是结合场景去解释。
#### wide+deep
![image](http://ox5l2b8f4.bkt.clouddn.com/images/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0%20-%20Wide%20and%20Deep%20Learning%20for%20Recommender%20Systems/1.jpg)
一般的推荐系统的总体架构。主要两部分，候选生成模型和排序系统。具体使用的时候，针对当前的用户和场景，首先从海量数据集里筛选出一小部分作为候选，而后将这个小集合再放到模型里进行打分排序。

###### 模型
![image](http://ox5l2b8f4.bkt.clouddn.com/images/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0%20-%20Wide%20and%20Deep%20Learning%20for%20Recommender%20Systems/3.jpg)
Wide部分用的是逻辑回归，采取的输入是原始的输入特征和一些transformed features。具体的公式:
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/0C922EC0F83A40F881775C7AD9AD6386?ynotemdtimestamp=1534595163888)
这是一个cross-product transformation的过程，文章举例子说,AND(user_installed_app=netflix,impression_app=pandora”) 这个特征，只有 Netflix 和 Pandora 两个条件都达到了，值才为 1.也就是通常所说的二阶特征。

Deep部分就是DNN模型了。原始的稀疏，高维特征首先会转换成embedding vector之后再作为输入，维度一般从10到100。

训练的时候是Joint Training也就是一起train的。这和emsemble是有区别的。前者一同训练，后者只在预测的时候再联系。
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/AA238EECBB1C4F63A3389B42D9DEFCB9?ynotemdtimestamp=1534595163888)

下面是应用在app 推荐时的具体模型：
![image](http://ox5l2b8f4.bkt.clouddn.com/images/%E8%AE%BA%E6%96%87%E7%AC%94%E8%AE%B0%20-%20Wide%20and%20Deep%20Learning%20for%20Recommender%20Systems/4.jpg)

#### DeepFM

模型架构上面基本一样，区别在于Wide部分改为了FM。
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/1D491888086F4CE098A8D3BA0C6B84F4?ynotemdtimestamp=1534595782475)
文章先举了一些例子，如人们在吃饭的时候下载美食app(2-order,时间和app类别)，男性儿童喜欢射击游戏(3-order,性别，年龄，app类别)。特征工程比较难以涵盖所有n-order特征。而DeepFM模型以原始特征作为输入，可以同时抽象出浅层和深层特征去做预测。

##### FM
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/7758EDF0AFB641138751151BFF2C1DD6?ynotemdtimestamp=1534595782475)
FM模型在一阶特征外增加了二阶特征。其抽取二阶特征的方式更加有效率，尤其是当数据集稀疏的时候，在传统的二阶特征构建方法里，特征i和j得到的二阶特征的参数，必须要特征i和j同时出现在一条数据里才能被训练。而FM不需要，它对每一个特征抽象出一个V，而后使用V之间的点乘结果作为二阶特征的参数，这样，V的训练其实并不依赖于i，j必须同时出现。其实这个过程和embedding基本一致，就是将类别embedding成V而后勇V之间的点乘相似度来作为二阶特征的参数。
那么原先的一阶特征似乎从论文看来就是使用onehot输入的，并没有使用embedding，当然这个地方其实也完全可以用，并不会有什么问题。
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/D2931C5E55134F2E911365042A347FA4?ynotemdtimestamp=1534596990276)


##### Deep
这部分是常规的DNN。需要注意的是这里用的embedding就是FM那里的V，也就是说embedding向量是共享的。

下面主要说下和其他NN的区别。
![image](https://note.youdao.com/yws/public/resource/74e30b2073532fef8651d868894bc264/8B39A87D593A4000AAE0E688E8F00F8B?ynotemdtimestamp=1534596990276)
###### FNN
使用FM预训练作为初始参数输入到NN里去，一方面embedding会受制于FM，另一方面预训练比较低效。且这样无法学习到both high and low order feature interactions。
###### PNN
为了捕捉高阶特征，增加了一个product layer在embedding层和第一个hidden层之间。其实就是将不同特征的embedding再做乘法后输入到下一层。该模型同样没有捕捉低阶特征。
###### Wide+Deep
相比于其，DeepFM不需要进行任何特征工程。
