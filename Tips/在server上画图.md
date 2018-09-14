在服务器上使用matplotlib画图如何操作。大概两种方法.

**一种是在server上不画出来而只是保存图片而后下载到本地打开图片查看。**

这种情况下需要对server环境进行如下修改:

1. 进入到正在使用的python环境

2. ```python
   import matplotlib
   matplotlib.matplotlib_fname()
   #记录下打印出来的结果，这里用A文件表示
   ```

3. 打开A文件，将其中某行的  backend TkAgg 改为 backend Agg

那么下面给出一个简单的画图的例子:

```python
 import seaborn as sns
 import numpy as np
 import matplotlib.pyplot as plt
 import matplotlib as mpl
 sen_dist = [1,1,1,1,2,2,3,5,6,7,7,7,8,8,8,8,8,8]
 sen_dist = np.array(sen_dist)
 #plt.figure(0)
 sns.set(color_codes=True)
 sns.distplot(np.array(sen_dist),bins=180)
 plt.savefig('sen.png')
 plt.close('all')
```



**第二个是使用Xwindow显示，直觉来说相当于会把一切需要图形界面展示的内容都直接映射到本地展示**

具体的设置步骤如下:

1. 对于服务器端，打开`/etc/ssh/sshd_config`这个文件，将其中某一行  ForwardX11 no改为:ForwardX11 yes,并且确保前面没有注释符`#`

2. 客户端，打开``/etc/ssh/sshd_config`这个文件`，将其中 ForwardAgent，ForwardX11, ForwardX11Trusted这三个都改为yes，并且确保前面没有注释符`#`

3. 重新连接ssh。需要注意的是这时候连接需要加一个-X后缀。如下例子

   ```
   ssh -X yourname@018.009.014.10
   ```

4. 这样就可以将远程服务器上需要图形界面展示的内容都在本地打开了。测试是否配置成功的话，可以在server上新建一个文本文件thisfile.txt，然后在服务器上运行 gedit thisfile.txt，试试。可以的话说明已经配置完成，那么以后用matplotlib画图，自然也会直接在本地机器上显示。

5. 不过嘛，我自己测试的时候发现显示图形的速度非常慢，不清楚是网络还是什么原因。

   下面也给出一个简单的画图例子

   ```python
   import matplotlib.pyplot as plt,numpy as np
   x = np.linspace(-1, 1, 50)
   print(x)
   y = 2*x + 1
   plt.plot(x, y)
   plt.show()
   ```

   

6. 报错:

   ```
   1.不行呢
   试着在本地机器上运行一下：xhost +
   2.报错内容：gdk-WARNING **: locale not supported by C library解决方法
   在服务上运行下面三行
   sudo locale-gen zh_CN.UTF-8
   sudo locale-gen
   sudo locale
   ```

   

以上。