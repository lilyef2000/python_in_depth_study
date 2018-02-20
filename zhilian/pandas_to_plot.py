# _*_ coding:utf-8 _*_
__author__ = 'antenna'
__date__ = '18-2-19 下午9:04'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import re
import matplotlib
import wordcloud
import jieba



# 读入文件名
import_from = 'Python_nation.json'

start_time = time.time()
# 读入json文件并做简单处理
with open(import_from, 'r', encoding="utf-8") as json_file:
    df = pd.read_json(json_file)
    # 查看df的信息
    # df.info()
    # print(df.columns)

df.index = df['_id']  # 索引列用'_id'列替换。
del (df['_id'])  # 删除原文件中'_id'列。
df_sort = df.sort_index()  # 给索引列重新排序。
df = df_sort
# print(df[['工作地点', '职位月薪']].head(10))


# 进行【职位月薪】列的分列操作，新增三列【bottom】、【top】、【average】分别存放最低月薪、最高月薪和平均月薪。
df['bottom'] = df['top'] = df['average'] = df['职位月薪']
pattern = re.compile('([0-9]+)')
q1 = q2 = q3 = q4 = 0

for i in range(len(df['职位月薪'])):
    item = df['职位月薪'].iloc[i].strip()
    result = re.findall(pattern, item)
    try:
        if result:
            try:
                # 此语句执行成功则表示result[0],result[1]都存在，即职位月薪形如‘6000-8000元/月’
                df['bottom'].iloc[i], df['top'].iloc[i] = result[0], result[1]
                df['average'].iloc[i] = str((int(result[0]) + int(result[1])) / 2)
                q1 += 1

            except:
                # 此语句执行成功则表示result[0]存在，result[1]不存在，职位月薪形如‘10000元/月以下’
                df['bottom'].iloc[i] = df['top'].iloc[i] = result[0]
                df['average'].iloc[i] = str((int(result[0]) + int(result[0])) / 2)
                q2 += 1
        else:
            # 此语句执行成功则表示【职位月薪】中并无数字形式存在，可能是‘面议’、‘found no element’
            df['bottom'].iloc[i] = df['top'].iloc[i] = df['average'].iloc[i] = item
            q3 += 1

    except Exception as e:
        q4 += 1
        print(q4, item, repr(e))

# for i in range(100):  # 测试一下看看职位月薪和bottom、top是否对的上号
#     print(df.iloc[i][['职位月薪', 'bottom', 'top', 'average']])  # 或者df[['职位月薪','bottom','top','average']].iloc[i]也可

# df[['职位月薪', 'bottom', 'top', 'average']].head(10)


# 进行【工作地点】列的处理，新增【工作城市】列，将工作地点中如‘苏州-姑苏区’、‘苏州-工业园区’等统统转化为‘苏州’存放在【工作城市】列。
df['工作城市'] = df['工作地点']
pattern2 = re.compile('(.*?)(\-)')
df_city = df['工作地点'].copy()

for i in range(len(df_city)):
    item = df_city.iloc[i].strip()
    result = re.search(pattern2, item)
    if result:
        # print(result.group(1).strip())
        df_city.iloc[i] = result.group(1).strip()
    else:
        # print(item.strip())
        df_city.iloc[i] = item.strip()

df['工作城市'] = df_city
# df[['工作地点', '工作城市']].head(20)


# ------------------------------
# -- 1.各个城市职位数量及分布 --
# ------------------------------
# print(df.工作城市.value_counts()) # 等价于df['工作城市'].value_counts()
# 用count()来看一下统计出来的城市数量
# print(df.工作城市.value_counts().count())
# print(type(df.工作城市.value_counts()))  # 用type()查看下类型。

# 将原来df['工作城市']列中选定的字段替换成空值nan
df_工作城市 = df['工作城市'].replace(['found no element', '宜昌', '张家口', '乐山', '甘孜', '潮州', '包头', '银川',
                              '唐山', '秦皇岛', '淄博', '凉山', '保定', '资阳', '达州', '文山', '南宁' ,'雅安', '巴中',
                              '广安', '盘锦', '南充', '洛阳', '湘潭', '阿坝', '海口', '来宾', '遂宁', '眉山', '十堰',
                              '宿迁', '西昌', '西宁', '德阳', '梅州', '揭阳', '舟山', '迪庆', '吉林市', '云浮', '湖州',
                              '阳江', '简阳', '株洲', '自贡', '宜宾', '阜阳', '清远', '全国', '汕尾', '内江', '肇庆',
                              '江门', '河源', '泸州', '茂名', '芜湖', '方家山', '滁州', '铜仁', '丽江', '昭通', '德宏',
                              '镇江', '湛江', '盐城', '衢州', '呼和浩特', '攀枝花', '广元', '丽水', '台州', '泰州', '绍兴',
                              '张家港', '温州', '太仓市', '金华', '嘉兴', '常熟', '韶关', '大理', '中山', '汕头', '廊坊',
                              '兰州', '淮安', '扬州', '连云港', '绵阳', '珠海', '徐州', '昆山', '常州', '乌鲁木齐', '南通',
                              '东莞', '惠州', '烟台', '南昌'], np.nan)
# 查看替换后各个城市职位计数
# print((df_工作城市.value_counts()))
# 查看替换后城市所包含的职位总数；查看替换后的城市数量，是否等于30.
# print(df_工作城市.value_counts().count())
# 将新的[df_工作城市]列添加到df表中，留作备用
df['df_工作城市'] = df_工作城市

# ------------------------------
# --  绘制 城市--职位数分布图 --
# ------------------------------
fig1 = plt.figure(1, facecolor='black')  # 设置视图画布1
ax1 = fig1.add_subplot(2, 1, 1, facecolor='#4f4f4f',
                       alpha=0.3)  # 在视图1中设置子图1,背景色灰色，透明度0.3(figure.add_subplot 和plt.suplot都行)
plt.tick_params(colors='white')  # 设置轴的颜色为白色
df_工作城市.value_counts().plot(kind='bar', rot=0, color='#ef9d9a')  # 画直方图图

# 设置图标题，x和y轴标题
title = plt.title(u'城市——职位数分布图', fontsize=18, color='yellow')  # 设置标题
xlabel = plt.xlabel(u'城市', fontsize=10, color='yellow')  # 设置X轴轴标题
ylabel = plt.ylabel(u'职位数量', fontsize=10, color='yellow')  # 设置Y轴轴标题

# 设置说明，位置在图的右上角
text1 = ax1.text(25, 3500, u'城市总数:30(个)', fontsize=12, color='cyan')  # 设置说明，位置在图的右上角
text2 = ax1.text(25, 3000, u'职位总数:16377(条)', fontsize=12, color='cyan')
text3 = ax1.text(25, 2500, u'有效职位:16377(条)', fontsize=12, color='red')

list_1 = df_工作城市.value_counts().values
# 添加每一个城市的坐标值
for i in range(len(list_1)):
    ax1.text(i - 0.3, list_1[i], str(list_1[i]), color='yellow')

# 可以用plt.grid(True)添加栅格线
# 可以用下面语句添加注释箭头。指向上海，xy为坐标值、xytext为注释坐标值，facecolor为箭头颜色。
# arrow = plt.annotate('职位数:3107', xy=(1,3107), xytext=(3, 4000),color='blue',arrowprops=dict(facecolor='blue', shrink=0.05))
ax2 = fig1.add_subplot(2, 1, 2)  # 设置子图2，是位于子图1下面的饼状图
# 为了方便，显示前8个城市的城市名称和比例、其余的不显示，用空字符列表替代，为此需要构造列表label_list和一个空字符列表['']*23。
x = df_工作城市.value_counts().values  # x是数值列表，pie图的比例根据数值占整体的比例而划分
label_list = []  # label_list是构造的列表，装的是前8个城市的名称+职位占比。
for i in range(8):
    t = df_工作城市.value_counts().values[i] / df_工作城市.value_counts().sum() * 100
    city = df_工作城市.value_counts().index[i]
    percent = str('%.1f%%' % t)
    label_list.append(city + percent)

# labels参数原本是与数值对应的标签列表，此处30个城市过多，所以只取了前8个城市显示。
# explode即饼图中分裂的效果explode=（0.1，1，1，。。）表示第一块图片显示为分裂效果
labels = label_list + [''] * 22
explode = tuple([0.1] + [0] * 29)
plt.pie(x, explode=explode, labels=labels, textprops={'color': 'yellow'})

# 可加参数autopct='%1.1f%%'来显示饼图中每一块的比例，但是此处30个城市，如果全显示的话会非常拥挤不美观，所以只能手动通过labels参数来构造。
# 若要显示标准圆形，可以添加：plt.axis('equal')

# plt.savefig("filename.png")
# plt.show()


# -------------------------------
# -- 2.工作经验-职位数量及分布 --
# -------------------------------
# print(df.工作经验.value_counts()) # 统计【工作经验】下各个字段的累计和
df_工作经验 = df['工作经验'].replace(['found no element'],np.nan)
# print(df_工作经验.value_counts())
# print(df_工作经验.value_counts().sum())

# -------------------------------------
# --  绘制 工作经验-职位数量及分布图 --
# -------------------------------------
fig2 = plt.figure(2, facecolor='black')
ax2_1 = fig2.add_subplot(2, 1, 1, facecolor='#4f4f4f', alpha=0.3)
plt.tick_params(colors='white')
df_工作经验.value_counts().plot(kind='bar', rot=0, color='#7fc8ff')
title = plt.title(u'工作经验——职位数分布图', fontsize=18, color='yellow')
xlabel = plt.xlabel(u'工作经验', fontsize=14, color='yellow')
ylabel = plt.ylabel(u'职位数量', fontsize=14, color='yellow')
plt.grid(True)
text1_ = ax2_1.text(5, 5600, u'城市总数:30(个)', fontsize=12, color='yellow')
text2 = ax2_1.text(5, 4850, u'职位总数:16377(条)', fontsize=12, color='yellow')
text3 = ax2_1.text(5, 4100, u'有效职位:16377(条)', fontsize=12, color='cyan')

# 设置子图2，是位于子图1下面的饼状图
ax2_2 = fig2.add_subplot(2, 1, 2)

# x是数值列表，pie图的比例根据数值占整体的比例而划分
x2 = df_工作经验.value_counts().values
labels = list(df_工作经验.value_counts().index[:5]) + [''] * 2
explode = tuple([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
plt.pie(x2, explode=explode, labels=labels, autopct='%1.1f%%', textprops={'color': 'yellow'})
plt.axis('equal')  # 显示为等比例圆形

# 设置图例，方位为右下角
legend = ax2_2.legend(loc='lower right', shadow=True, fontsize=12, edgecolor='cyan')

# plt.show()


# -------------------------------
# --    3.工作经验-平均月薪    --
# -------------------------------
# print(df.average.value_counts())
df_平均月薪 = df['average'].replace(['面议','found no element'],np.nan)
df3=pd.DataFrame(data={'工作经验':df_工作经验,'平均月薪':df_平均月薪})

#构造一个listi存放转化后float型的‘平均月薪’
import re
pattern = re.compile('([0-9]+)')
listi = []
for i in range(len(df.average)):
    item = df.average.iloc[i].strip()
    result = re.findall(pattern,item)
    try:
        if result:
            listi.append(float(result[0]))
        elif (item.strip()=='found no element' or item.strip()=='面议'):
            listi.append(np.nan)
        else:
            print(item)
    except Exception as e:
        print(item,type(item),repr(e))

#将df3.平均月薪列替换掉,同时给df新增一列'df_平均月薪'做备用。
df3['平均月薪'] = listi
df['df_平均月薪'] = df3['平均月薪']

# 看看更新后的数据是否正确
# df3['平均月薪'].value_counts() # 统计每个月薪字段的个数
# df3['平均月薪'][:10] # 查看前10个值
# type(df3['平均月薪'][1]) # 看看现在月薪的类型是不是浮点型
# print(df3['平均月薪'].value_counts().sum())#看看月薪样本总数
# print(df3['平均月薪'].mean()) #看看这14793个月薪样本的平均值是多少？
#
# df3.info()
grouped3 = df3['平均月薪'].groupby(df3['工作经验'])

# 新增一个平均值，即所有非空df3['平均月薪']的平均值
s3 = pd.Series(data = {'平均值':df3['平均月薪'].mean()})
result3 = grouped3.mean().append(s3)

# print("---unsort---")
# print(result3)
# sort_values()方法可以对值进行排序，默认按照升序，round（1）表示小数点后保留1位小数。
# result3.sort_values(ascending=False).round(1)  # 高版本pandas采用该方法
result3.sort(ascending=False) # 低版本pandas采用该方法
# print("---sorted---")
# print(result3.round(1))       # 低版本pandas采用该方法

# --------------------------------
# --  绘制 工作经验--平均月薪图 --
# --------------------------------
matplotlib.style.use('ggplot')
fig3 = plt.figure(3,facecolor = 'black')
ax3 = fig3.add_subplot(1,1,1,facecolor='#4f4f4f',alpha=0.3)
# result3.sort_values(ascending=False).round(1).plot(kind='barh',rot=0)  # 高版本pandas采用该方法
result3.round(1).plot(kind='barh',rot=0)   # 低版本pandas采用该方法

#设置标题、x轴、y轴的标签文本
title = plt.title('工作经验——平均月薪分布图',fontsize = 18,color = 'yellow')
xlabel= plt.xlabel('平均月薪',fontsize = 14,color = 'yellow')
ylabel = plt.ylabel('工作经验',fontsize = 14,color = 'yellow')

#添加值标签
list3 = result3.round(1).values
for i in range(len(list3)):
    ax3.text(list3[i],i,str(int(list3[i])),color='yellow')

#设置标识箭头
arrow = plt.annotate('Python平均月薪:14400元/月', xy=(14400,3.25), xytext=(20000,4.05),color='yellow',fontsize=16,arrowprops=dict(facecolor='cyan', shrink=0.05))

#设置图例注释（14973来源：df3['平均月薪'].value_counts().sum()）
text= ax3.text(27500,6.05,'月薪样本数:14973(个)',fontsize=16, color='cyan')

#设置轴刻度文字颜色为白色
plt.tick_params(colors='white')

# plt.show()


# -------------------------------------
# --    4.工作城市-平均月薪分布图    --
# -------------------------------------
# 此处df['df_工作城市']是之前经过筛选后的30个城市数据
df4=pd.DataFrame(data={'工作城市':df['df_工作城市'],'平均月薪':df['df_平均月薪']})
# df4.info()
grouped4 = df4['平均月薪'].groupby(df4['工作城市'])
# print("---1---")
# print(grouped4.mean()) # 查看对30个城市分组后，各个城市月薪的平均值
# print("---2---")
# print(grouped4.count().sum()) # 查看对30个城市分组后筛选出的平均月薪样本数 14427
# print("---3---")
# print(df4['平均月薪'].value_counts().sum()) # 看看月薪样本总数 月薪样本总数（所有城市） 1479
# print("---4---")
# print(df4['平均月薪'].mean()) #看看这14793个月薪样本的平均值是多少？14400

# 新增一个平均值，即所有非空df2['平均月薪']的平均值
s4 = pd.Series(data = {'平均值':df['df_平均月薪'].mean()})
result4 = grouped4.mean().append(s4)
# sort_values()方法可以对值进行排序，默认按照升序，round（1）表示小数点后保留1位小数。
# result4.sort_values(ascending=False).round(1)  # 高版本pandas采用该方法
result4.sort(ascending=False)   # 低版本pandas采用该方法

# --------------------------------
# --  绘制 工作城市--平均月薪图 --
# --------------------------------
#可以通过style.available查看可用的绘图风格，总有一款适合你
matplotlib.style.use('dark_background')
fig4 = plt.figure(4)
ax4 = fig4.add_subplot(1,1,1) # 可选facecolor='#4f4f4f',alpha=0.3，设置子图,背景色灰色，透明度0.3
# result4.sort_values(ascending=False).round(1).plot(kind='bar',rot=30) # 可选color='#ef9d9a'
result4.round(1).plot(kind='bar',rot=30) # 低版本pandas使用该方法

#设置图标题，x和y轴标题
title = plt.title(u'城市——平均月薪分布图',fontsize=18,color='yellow')#设置标题
xlabel = plt.xlabel(u'城市',fontsize=6,color='yellow')#设置X轴轴标题
ylabel = plt.ylabel(u'平均月薪',fontsize=6,color='yellow')#设置Y轴轴标题

#设置说明，位置在图的右上角
text1 = ax4.text(25,16250,u'城市总数:30(个)',fontsize=12, color='#FF00FF')#设置说明，位置在图的右上角
text2 = ax4.text(25,15100,u'月薪样本数:14427(条)',fontsize=12, color='#FF00FF')

#添加每一个城市的坐标值
list_4 = result4.round(1).values
for i in range(len(list_4)):
    ax4.text(i-0.5,list_4[i],int(list_4[i]),color='yellow')

#设置箭头注释
arrow = plt.annotate(u'全国月薪平均值:14400/月', xy=(4.5,14400), xytext=(7,15000),color='#9B30FF',fontsize=14,arrowprops=dict(facecolor='#FF00FF', shrink=0.05))

#设置轴刻度文字颜色为粉色
plt.tick_params(colors='pink')

# plt.show()


# ---------------------------
# --    5.学历-职位数量    --
# ---------------------------
# print("------学历要求------")
# print(df['学历要求'].value_counts())
df_学历要求=df['学历要求'].replace(['其他','高中','found no element'],np.nan)
# print("------学历要求(筛选小值后)------")
# print(df_学历要求.value_counts())  #
# print("------学历要求总样本------")
# print(df_学历要求.value_counts().sum()) # 16373
df['df_学历要求'] = df_学历要求 # 留作备用

# ------------------------------
# --  绘制 学历--职位数分布图 --
# ------------------------------
fig5 = plt.figure(5)
ax5_1 = fig5.add_subplot(2,1,1)  # 可选facecolor='#4f4f4f',alpha=0.3
df_学历要求.value_counts().plot(kind = 'bar',rot=0)   # color='#7fc8ff'

# 设置标题、x轴和y轴标题、图例文字
title = plt.title(u'学历要求——职位数分布图',fontsize = 18,color = 'yellow')
xlabel = plt.xlabel(u'学历要求',fontsize = 14,color = 'yellow')
ylabel = plt.ylabel(u'职位数量',fontsize = 14,color = 'yellow')
text1 = ax5_1.text(4.4,8200,u'职位总数:16373(条)',fontsize=14, color='#B452CD')

# 设置坐标轴的的颜色和文字大小
plt.tick_params(colors='#9F79EE',labelsize=13)

# 设置坐标值文字
list5 = df_学历要求.value_counts().values
for i in range(len(list5)):
    ax5_1.text(i-0.1,list5[i],int(list5[i]),color='yellow')
ax5_2=fig5.add_subplot(2,1,2)
xl = df_学历要求.value_counts().values
# print(xl)
labels = list(df_学历要求.value_counts().index)
explode = tuple([0.1,0,0,0,0,0,0])
plt.pie(xl,explode=explode,labels=labels,autopct='%1.1f%%',textprops={'color':'#B452CD'})
plt.axis('equal')
legend = ax5_2.legend(loc='lower right',shadow=True,fontsize=12,edgecolor='#B452CD')
plt.tick_params(colors='#9F79EE',labelsize=13)

# plt.show()


# -------------------------------
# --    6.最低学历-平均月薪    --
# -------------------------------
df6=pd.DataFrame(data={'学历要求':df['df_学历要求'],'平均月薪':df['df_平均月薪']})
# df6.info()
grouped6 = df6['平均月薪'].groupby(df6['学历要求'])
result6 = grouped6.mean()

# 查看grouped6的信息
# print("---分类平均月薪---")
# print(grouped6.mean())
# print("---分类样本数---")
# print(grouped6.count())
# print("---总有效样本数---")
# print(grouped6.count().sum())  # 14791

# --------------------------------
# --  绘制 学历--平均月薪分布图 --
# --------------------------------
matplotlib.style.use('ggplot')
fig6 = plt.figure(6,facecolor = 'black')
ax6 = fig6.add_subplot(1,1,1,facecolor='#4f4f4f',alpha=0.3)

# grouped6.mean().round(1).sort_values().plot(color = 'cyan') # 高版本pandas使用 在条形图上叠加一个折线图
# grouped6.mean().round(1).sort_values().plot(kind='bar',rot=0)
result6.sort(ascending=False)   # 低版本pandas采用该方法
result6.round(1).plot(color = 'cyan')
result6.round(1).plot(kind='bar',rot=0)

# 设置标题、x轴、y轴的标签文本
title = plt.title(u'学历——平均月薪分布图',fontsize = 18,color = 'yellow')
xlabel= plt.xlabel(u'学历要求',fontsize = 14,color = 'yellow')
ylabel = plt.ylabel(u'平均月薪',fontsize = 14,color = 'yellow')

# 添加值标签(坐标值文字)
# list6 = grouped6.mean().round(1).sort_values().values  # 高版本pandas使用
list6 = result6.round(1).values
list6 = [x for x in list6 if str(x) != 'nan'] # 清除nan项
for i in range(len(list6)):
    ax6.text(i-0.1,list6[i],int(list6[i]),color='yellow')

# 设置图例注释
text= ax6.text(0,27000,u'月薪样本数:14791(个)',fontsize=16, color='cyan')

# 设置轴刻度的文字颜色
plt.tick_params(colors='#9F79EE')

# plt.show()


# ----------------------------------------
# --    7.最低学历-工作经验-平均月薪    --
# ----------------------------------------
df7 = pd.DataFrame(data = {'平均月薪':df['df_平均月薪'],'学历要求':df['df_学历要求'],'工作经验':df_工作经验})
# df7.info()
grouped7 = df7['平均月薪'].groupby([df7['学历要求'],df7['工作经验']])
result7 = grouped7.mean()

#查看grouped7的信息
# print("---学历 工作经验 平均月薪---")
# print(grouped7.mean().round(1))
# print("---学历 工作经验 招聘职位---")
# print(grouped7.count())
# print("---总样本数---")
# print(grouped7.count().sum()) # 14791

result7.sort()
xlist = list(result7.round(1)[:,'1-3年'].index)
result7.round(1)[:,'1-3年'].reindex(xlist)
# print(xlist)

# --------------------------------------------
# --  绘制 最低学历-工作经验-平均月薪分布图 --
# --------------------------------------------
# 开始画图，设置基本参数
matplotlib.style.use('dark_background')
fig7 = plt.figure(7,facecolor = 'black')
ax7 = fig7.add_subplot(1,1,1,facecolor='#4f4f4f',alpha=0.3)
title = plt.title(u'最低学历-工作经验-平均月薪分布图',fontsize = 18,color = 'yellow')
xlabel = plt.xlabel(u'最低学历',fontsize = 14,color = 'yellow')
ylabel = plt.ylabel(u'平均月薪',fontsize = 14,color = 'yellow')
plt.tick_params(colors='cyan')

def filternan(list_temp):
    list = []
    for i in list_temp:
        if str(i) == 'nan':
            list.append(0)
        else:
            list.append(i)
    del list[-1]
    return list

# ylist1~7分别是7种条形图的Y值列表
ylist1 = result7.round(1)[:,'无经验'].reindex(xlist).values
ylist2 = result7.round(1)[:,'1年以下'].reindex(xlist).values
ylist3 = result7.round(1)[:,''].reindex(xlist).values
ylist4 = result7.round(1)[:,'1-3年'].reindex(xlist).values
ylist5 = result7.round(1)[:,'3-5年'].reindex(xlist).values
ylist6 = result7.round(1)[:,'5-10年'].reindex(xlist).values
ylist7 = result7.round(1)[:,'10年以上'].reindex(xlist).values
ylist1 = filternan(ylist1) # nan项替换为0
ylist2 = filternan(ylist2) # nan项替换为0
ylist3 = filternan(ylist3) # nan项替换为0
ylist4 = filternan(ylist4) # nan项替换为0
ylist5 = filternan(ylist5) # nan项替换为0
ylist6 = filternan(ylist6) # nan项替换为0
ylist7 = filternan(ylist7) # nan项替换为0

print(ylist1)
print(ylist2)
print(ylist3)

# img1~img7分别表示7种条形图
ind = np.arange(6) # ind为x轴宽度，用numpy的array形式表示
width = 0.1 # 条形图的宽度，要合理设置否则太宽会摆不下
img1 = ax7.bar(ind,ylist1,width)
img2 = ax7.bar(ind+width,ylist2,width)
img3 = ax7.bar(ind+width*2,ylist3,width)
img4 = ax7.bar(ind+width*3,ylist4,width)
img5 = ax7.bar(ind+width*4,ylist5,width)
img6 = ax7.bar(ind+width*5,ylist6,width)
img7 = ax7.bar(ind+width*6,ylist7,width)

# 设置X轴文本和位置调整
ax7.set_xticklabels(xlist)
ax7.set_xticks(ind + width / 2)

# 设置文字说明
text1 = ax7.text(4.05,52100,u'数据来源:智联招聘',fontsize=13, color='#9F79EE')
text2 = ax7.text(4.05,50200,u'职位关键词：Python',fontsize=13, color='#9F79EE')
text3 = ax7.text(4.05,48200,u'工作城市:全国30座城市',fontsize=13, color='#9F79EE')
text4 = ax7.text(4.05,46200,u'职位数量:共计14791(条)',fontsize=13, color='#9F79EE')

# 设置图例
ax7.legend((img1[0],img2[0],img3[0],img4[0],img5[0],img6[0],img7[0]), (u'无经验',u'1年以下',u'不限',u'1-3年',u'3-5年',u'5-10年',u'10年以上'),fontsize=13,facecolor='black')

# 设置栅格
plt.grid(True)

# plt.show()




# 生成招聘简介和职位名称的词云图

# 过滤掉一些无意义的词
def word_filter(word):
    filterd_re = r"经验|开发|计算机|算机|能力|职位|职责|岗位|计算|学历|本科|服务|任职|专业|熟悉|\
                  熟练|以上|上学|团队|相关|沟通|掌握|使用|以及|互联|数据库|编程|解决|优先|\
                  优先|工作|负责|责任|参与|了解|参与|技术|描述|进行|具有|考虑|良好|至少|一种|\
                  精神|精通|要求|管理|研发|具备|常用|产品|公司|项目"
    if re.search(filterd_re,word):
        return True
    else:
        return False

job_text = ""
for i in df['招聘简介']:
    job_text += str(i)
for j in df['职位名称']:
    job_text += str(j)
# print(job_text)
# print("There are {} jobs".format(len(df['职位名称'])))

# 分词
seg_list = jieba.cut(job_text, cut_all=False)
# search engine mode
# seg_list = jieba.cut_for_search(all_job_text)
seg_list = list(seg_list)
# filter some unwanted word
filterd_list = [word for word in seg_list if not word_filter(word)]
filterd_str =  (' ').join(filterd_list)

# Generate a word cloud image
# wordcloud = wordcloud.WordCloud(width=600, height=600).generate(filterd_list1)
wordcloud = wordcloud.WordCloud(font_path="MSYH.TTF",width=600, height=600).generate(filterd_str)  # 注意：MSYH.TTF要放在程序目录下

# Display the generated image:
# the matplotlib way:
fig8 = plt.figure(8,facecolor = 'black')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

end_time = time.time()
print(end_time - start_time)

