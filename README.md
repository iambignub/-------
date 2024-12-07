# 南宁房价分析小项目
python爬虫，spark分析，flask网页，echarts

一、实验原理或实验内容
系统开发设计：通过WebMagic（Java爬虫框架）编写网络爬虫程序，采集XX市
二手房交易数据，将采集的数据存储到MongoDB数据库中。当数据采集完成后，利用
Spark 计算框架读取MongoDB中存储的二手房交易数据，并进行离线分析，最后将分
析结果存储到MongoDB数据库中。为了可以更加直观的查看分析结果，我们通过
Web 系统获取MongoDB数据库中存储的分析结果，实现数据的可视化。

二、实验器材及实验条件
Windows 11，MongoDB，flask，spark，pycharm

三、实验步骤与结果
1. 数据采集: 实现爬虫程序，采集链家网站的南宁二手房数据，由于没有县的数
据，所以这里只爬取几个区的，保存到MongoDB数据库中。
```python
import requests
 import threading
 import pandas as pd
 from lxml import etree
 # 全部信息列表
count = []
 1
2
 # 创建线程锁对象
lock = threading.RLock()
 # 生成1-10页url
 def url_creat():
    links = []  # 在循环外初始化列表
    for i in range(1, 100):  # 根据需要调整range参数
        url = f'https://nn.lianjia.com/ershoufang/pg{i}/'  # 注意字符串格式化的
简洁性
        links.append(url)  # 向列表中添加当前循环生成的URL
    return links  # 循环结束后返回完整的链接列表
# 对url进行解析
def url_parse(url):
    headers = {
        'Accept': 
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/web
 p,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'lianjia_uuid=7e346c7c-5eb3-45d9-8b4f-e7cf10e807ba; 
UM_distinctid=17a3c5c21243a-0c5b8471aaebf5-6373267-144000-17a3c5c21252dc; 
_smt_uid=60d40f65.47c601a8; _ga=GA1.2.992911268.1624510312; 
select_city=370200; lianjia_ssid=f47906f0-df1a-49e2-ad9b-648711b11434; 
CNZZDATA1253492431=1056289575-1626962724
https%253A%252F%252Fwww.baidu.com%252F%7C1626962724; 
CNZZDATA1254525948=1591837398-1626960171
https%253A%252F%252Fwww.baidu.com%252F%7C1626960171; 
CNZZDATA1255633284=1473915272-1626960625
https%253A%252F%252Fwww.baidu.com%252F%7C1626960625; 
CNZZDATA1255604082=1617573044-1626960658
https%253A%252F%252Fwww.baidu.com%252F%7C1626960658; 
_jzqa=1.4194666890570963500.1624510309.1624510309.1626962867.2; _jzqc=1; 
_jzqy=1.1624510309.1626962867.2.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=
 baidu; _jzqckmp=1; _qzjc=1; 
sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217a3c5c23964c1
05089a8de73cbf-6373267-1327104
17a3c5c23978b3%22%2C%22%24device_id%22%3A%2217a3c5c23964c1-05089a8de73cbf
6373267-1327104
17a3c5c23978b3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%2
 2%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_r
 eferrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referr
 er_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%
 9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22baidu%2
 2%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%2
 2%3A%22wyyantai%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%2
 2%24latest_utm_term%22%3A%22biaoti%22%7D%7D; 
Hm_lvt_9152f8221cb6243a53c83b956842be8a=1624510327,1626962872; 
_gid=GA1.2.134344742.1626962875; 
Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1626962889; 
_qzja=1.1642609541.1626962866646.1626962866646.1626962866647.1626962872770.
 1626962889355.0.0.0.3.1; _qzjb=1.1626962866646.3.0.0.0; _qzjto=3.1.0; 
_jzqb=1.3.10.1626962867.1; 
srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNzQ3M2M3OWQyZTQwNGM5OGM1MDBjMmMxODk5NTBhOWRhN
 mEyNjhkM2I5ZjNlOTkxZTdiMDJjMTg0ZGUxNzI0NDQ5YmZmZGI1ZjZmMDRkYmE0MzVmNmNlNDIw
 Y2RiM2YxZTUzZWViYmQwYmYzMDQ1NDcyMzYwZTQzOTg3MzJhYTRjMTg0YjNhYjBkMGMyZGVmOWZ
 iYjdlZWQwMDcwNWFkZmI5NzA5MjM1NmQ1NDg0MzQ3NGIzYjkwY2IyYmEwMjA2NjBjMjI2OWRjNj
 FiNDE3ZDc1NGViNjhlMzIzZmI0MjFkNzU5ZGNlMzAzMDhlNDAzYzIzNjllYWFlMzYxZGYxYjNmZ
 mVkNGMxYTk1MmQ3MGY2MmJhMTQ1NWI4ODIwNTE5ODI2Njg2MmVkZTk4OWZiMDhjNTJhNzE3OTBl
 NDFiZDQzZTlmNDNmOGRlMTFjYTAwYTRlZTZiZWY5MTZkMTcwN1wiLFwia2V5X2lkXCI6XCIxXCI
 sXCJzaWduXCI6XCI3ZjI1NWI1ZlwifSIsInIiOiJodHRwczovL3FkLmxpYW5qaWEuY29tL2Vyc2
 hvdWZhbmcvMTAzMTE2MDkzOTU5Lmh0bWwiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        'Host': 'nn.lianjia.com',
        'Pragma': 'no-cache',
        'Referer': 'https://nn.lianjia.com/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", 
"Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)
    # ul列表下的全部li标签
    li_List = tree.xpath("//*[@class='sellListContent']/li")
    # 上锁
    lock.acquire()
    for li in li_List:
        # 标题
        title = li.xpath('./div/div/a/text()')[0]
        # 网址
        link = li.xpath('./div/div/a/@href')[0]
4
        # 位置
        postion = li.xpath('./div/div[2]/div/a/text()')[0] + 
li.xpath('./div/div[2]/div/a[2]/text()')[0]
        # 类型
        types = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[0]
        # 面积
        area = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[1]
        # 房屋信息
        info = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[2:-1]
        info = ''.join(info)
        # 总价
        count_price = li.xpath('.//div/div[6]/div/span/text()')[0] + '万'
        # 单价
        angle_price = li.xpath('.//div/div[6]/div[2]/span/text()')[0]
        dic = {'标题': title, "位置": postion, '房屋类型': types, '面积': area, 
"单价": angle_price, '总价': count_price, '介绍': info, "网址": link}
        print(dic)
        # 将房屋信息加入总列表中
        count.append(dic)
    # 解锁
    lock.release()
 def run():
    links = url_creat()
    threads = []
    # 多线程爬取
    for i in links:
        t = threading.Thread(target=url_parse, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # 将全部房屋信息转化为excel
    data = pd.DataFrame(count)
    data.to_excel('房屋信息.xlsx', index=False)
 if __name__ == '__main__':
    run()
```
![image](https://github.com/user-attachments/assets/8f29666e-d774-492d-8b79-28a7de47603d)
![image](https://github.com/user-attachments/assets/10b8c729-0c50-42ac-83f8-76eb019877c7)
- 配置spark环境
![image](https://github.com/user-attachments/assets/bc98040e-7b5d-4a4f-8f73-cd96b158a896)
![2872cf9464aea7c155c25989c422de9f](https://github.com/user-attachments/assets/98a544d9-6cb4-4286-a986-3b6eb29032fc)

编写python程序，下载需要的包
`pip install pyspark pymongo`
编写python程序
```python
from pyspark.sql import SparkSession
 from pyspark.sql.functions import col
 # 创建 SparkSession 并配置 MongoDB 连接器
spark = SparkSession.builder \
 .appName("RealEstateDataAnalysis") \
 .config("spark.mongodb.input.uri", 
"mongodb://127.0.0.1:27017/real_estate.house_info") \
 .config("spark.mongodb.output.uri", 
"mongodb://127.0.0.1:27017/real_estate.analysis_results") \
 .config("spark.jars.packages", "org.mongodb.spark:mongo-spark
connector_2.12:3.0.1") \
 .getOrCreate()
 # 读取 MongoDB 中的数据
df = spark.read.format("mongo").load()
 # 将总价列转换为数值类型
df = df.withColumn("总价", col("总价").cast("double"))
 # 数据分析示例：按区统计平均房价
result_df = df.groupBy("区").avg("总价").withColumnRenamed("avg(总价)", "平均总价")
 # 将分析结果写入 MongoDB
 result_df.write.format("mongo").mode("overwrite").save()
 print("数据分析完成并存储到MongoDB")
cmd运行```
spark-submit --jars "D:\spark-jars\mongo-spark-connector_2.12-3.0.1
assembly.jar" --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 
C:\Users\username\PycharmProjects\pythonProject3\py_spark.py
```
执行spark分析数据
![image](https://github.com/user-attachments/assets/ee99b662-8154-4b05-8406-c0388a66a1d7)

输出结果成功
![image](https://github.com/user-attachments/assets/7a6da7cc-7f90-4098-b986-8787c2e77ebd)

创建flask web对数据进行可视化
连接到MongoDB实现接口
```python
from flask import Flask, jsonify, render_template
 from pymongo import MongoClient
 app = Flask(__name__)
 # 连接到MongoDB
 client = MongoClient("mongodb://127.0.0.1:27017/")
 db = client["real_estate"]
 collection = db["analysis_results"]
 @app.route('/')
 def index():
 return render_template('index.html')
 @app.route('/api/data', methods=['GET'])
 def get_data():
 data = list(collection.find({}, {'_id': 0}))
 return jsonify(data)
 if __name__ == '__main__':
 app.run(debug=True)
```
前端：
```html
<!DOCTYPE html>
 <html lang="zh">
 <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>房产数据分析</title>
    <script 
src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
 </head>
 <body>
    <h1>房产数据分析</h1>
    <div id="main" style="width: 800px;height:400px;"></div>
    <script>
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                const labels = data.map(item => item.区);
                const avgPrices = data.map(item => item.平均总价);
                const avgAreas = data.map(item => item.平均面积);
                const counts = data.map(item => item.房子数量);
                var myChart = echarts.init(document.getElementById('main'));
                var option = {
                    title: {
                        text: '房产数据分析',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['平均总价', '平均面积', '房子数量'],
                        top: '10%'
                    },
                    xAxis: {
                        type: 'category',
                        data: labels
                    },
                    yAxis: [
                        {
                            type: 'value',
                            name: '价格和面积',
10
                            position: 'left'
                        },
                        {
                            type: 'value',
                            name: '房子数量',
                            position: 'right'
                        }
                    ],
                    series: [
                        {
                            name: '平均总价',
                            type: 'bar',
                            data: avgPrices,
                            yAxisIndex: 0,
                            itemStyle: {
                                color: 'rgba(255, 99, 132, 0.6)'
                            }
                        },
                        {
                            name: '平均面积',
                            type: 'bar',
                            data: avgAreas,
                            yAxisIndex: 0,
                            itemStyle: {
                                color: 'rgba(54, 162, 235, 0.6)'
                            }
                        },
                        {
                            name: '房子数量',
                            type: 'bar',
                            data: counts,
                            yAxisIndex: 1,
                            itemStyle: {
                                color: 'rgba(75, 192, 192, 0.6)'
                            }
                        }
                    ]
                };
                myChart.setOption(option);
            });
    </script>
 </body>
 </html>
```
- 调用了echarts，由于数值单位相差较大，所以不能同时显示
