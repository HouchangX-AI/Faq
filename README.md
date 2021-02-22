# BEFAQ

我们将Sentence BERT模型应用到FAQ问答系统中。开发者可以使用BEFAQ系统快速构建和定制适用于特定业务场景的FAQ问答系统。</br>

## 特点：

<br>（1）使用了Elasticsearch、Faiss、Annoy 作为召回引擎</br>
<br>（2）使用了Sentence BERT 语意向量（Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks）</br>
<br>（3）对同义问题有很好的支持</br>
<br>（4）支持多领域语料（保证了召回的数据是对应领域的，即使是同样的问题，也可以得到不同的答案。）</br>


## BEFAQ的框架结构如下图
![image](https://github.com/hhzrd/BEFAQ/blob/master/image/BEFAQ%20%E6%A1%86%E6%9E%B6.png)


## 如何使用

### 1、安装Es7.6.1

请参考博客[ES（Elasticsearch）7.6.1安装教程](https://blog.csdn.net/weixin_37792714/article/details/108025200)进行安装。

### 2、sentence-transformers 多语言预训练模型的下载

    首先进入到项目的根目录，然后
    cd data/model
    wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/distiluse-base-multilingual-cased.zip
    unzip distiluse-base-multilingual-cased.zip

### 
### 3、修改BEFAQ的配置文件

    项目根目录下的data/线上用户反馈回复.xlsx 是QA数据的来源，其中的数据会被写入到Es中。
    项目根目录下的sheetname.conf 是读取Excel文档数据的配置文件。如果你想要先跑通代码尝试一下。可以先不修改这里的配置。
    项目根目录下的es/es.ini 是BEFAQ关于ES的配置文件。这个配置文件里需要配置Es的IP（域名）和端口号，Es的登陆的用户名和密码。一定要根据自己的Es的配置进行修改，才能让BEFAQ连接上你的Es。
    项目根目录下的faq/befaq_conf.ini 是BEFAQ的配置文件。


### 4、如何开启BEFAQ服务

    进入项目的根目录，然后
    cd es
    
    将数据从excel 写到ES
    python write_data2es.py
    
    将问题处理成Sentence BERT 向量，保存到bin类型文件中，便于后期读取问题的向量。
    python write_vecs2bin.py
    
    训练Faiss和Annoy模型
    python train_search_model.py
    
    进入项目的根目录(cd  ..)，然后
    cd faq
    
    启动BEFAQ服务 （如果数据没有发生变化，后期启动服务只需要进行这一步）
    python main_faq.py 
    
    在终端中测试BEFAQ。BEFAQ的服务是post请求。(将xxx.xx.xx.xx替换成自己的ip)
    
    curl -d "question=忘记原始密码怎么修改密码&get_num=3&threshold=0.5&owner_name=领域1"   http://xxx.xx.xx.xx:8129/BEFAQ
    
    接口url:
    http://xxx.xx.xx.xx:8129/BEFAQ
    接口参数说明
    question：用户的问题。必需
    get_num：接口最多返回几条数据。非必需，默认为3
    threshold：阈值，相似度高于这个阈值的数据才会被接口返回。非必需，默认为0.5
    owner_name：数据所有者的名称，也就是excel中每个领域的数据对应的sheet name。用来区分多领域数据。必需
    
    返回的数据格式：
    [
        {
            "q_id": 5,
            "specific_q_id": 10,
            "question": "忘记原始密码如何修改密码？",
            "answer": "您可在登录界面，密码登录，使用找回密码功能进行验证。",
            "confidence": 0.99
        }
    ]




### 

