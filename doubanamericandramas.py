'''
name : //h1/span[@property="v:itemreviewed"  
year : //h1/span[@class="year"]   (2017)    year.lstrip('(').rstrip(')')
type : //div[@id="info"]/span[@property="v:genre"]
time ：//div[@id="info"]/span[@property="v:runtime"]   123分钟 
area ：//div[@id="info"]//span[@class="pl"][2]

待考虑情况：
片长: 137分钟 / 140分钟(加长版)

待解决：
<span class="pl">又名:</span> 解氷 / 化冰 / Bluebeard<br>


'''

'''
表头

序号	电视剧名称	电视剧类别	电视剧又名	类型	年份	片头	片尾	单集时长	集数	总时长	成品完成时间	压片人员	编辑人员	分辨率
'''




import requests
from lxml import etree
import re
import xlwt
import time
from tvseries import TVSeries

def gen_xls_from_urls(urls=None,work_name='于孟孟',editor_name = '朱恒',resolution =720,program_type = '电视剧'):
    '''

    :param urls:        节目的链接列表
    :param work_name:   压片人
    :param editor_name: 编辑
    :param resolution:  默认分辨率
    :param program_type:节目类型
    :return:
    
    '序号',	'电视剧名称',	'电视剧类别',	'电视剧又名',	'类型',	'年份',	'片头',	'片尾',	'单集时长',	'集数',	'总时长',	'成品完成时间',	'压片人员',	'编辑人员',	'分辨率'
    
    '''
    # 表格的标题
    title = ['序号',	'电视剧名称',	'电视剧类别',	'电视剧又名',	'类型',	'年份',	'片头',	'片尾',	'单集时长',	'集数',	'总时长',	'成品完成时间',	'压片人员',	'编辑人员',	'分辨率']

    program_type = program_type
    #今天的日期
    date = int(time.strftime('%Y%m%d', time.localtime()))

    # 创建Excel文件
    xls = xlwt.Workbook()
    sheet = xls.add_sheet(program_type)

    #起始列数
    column = -1
    # 起始行列数
    row = 0
    # 当前正处理的电视剧数
    count = 0
    #第一行写标题
    for t in title:
        column += 1
        sheet.write(0, column, t)

    # 电影成品部数
    total = len(urls)


    for url in urls:
        column = -1
        #记录每行信息
        info = []

        #电视剧的对象
        tv_serices = TVSeries()
        response = requests.get(url)
        html = response.text  # html type is string
        page = etree.HTML(html.encode('utf-8'))

        # 根据url获取节目信息
        # 电视剧名
        names = page.xpath('//h1/span[@property="v:itemreviewed"]/text()')[0]
        #正则表达式切割字符串，可以分割多个空格的情况
        names = re.split(r' +',names)  
        print('names',names)
        if len(names) > 1:
            if re.match(r'第.+季',names[1]):
                tv_serices.name = names[0] + names[1]
            else:
                tv_serices.name = names[0]
        else:
            tv_serices.name = names[0]

        # 年份
        year = page.xpath('//h1/span[@class="year"]/text()')[0].lstrip('(').rstrip(')')
        tv_serices.year = int(year)
        typelist = page.xpath('//div[@id="info"]/span[@property="v:genre"]/text()')
        # 类型列表字符串
        tv_serices.type = '/'.join(typelist)
        #电视剧类别
        areas = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', html)

        if re.search(r'英国|美国|加拿大', areas[0]):
            tv_serices.area_type = '美剧'
        elif re.search(r'韩国', areas[0]):
            tv_serices.area_type = '韩剧'
        elif re.search(r'日本', areas[0]):
            tv_serices.area_type = '日剧'
        elif re.search(r'香港', areas[0]):
            tv_serices.area_type = '港剧'
        elif re.search(r'台湾', areas[0]):
            tv_serices.area_type = '台剧'
        elif re.search(r'中国', areas[0]):
            tv_serices.area_type = '中剧'


        # 别名
        alias = re.findall('<span class="pl">又名:</span>(.*?)<br/>', html)
        if alias:
            tv_serices.alias = alias[0].strip(' ')
        else:
            tv_serices.alias = ''

        print(tv_serices.name,tv_serices.year,tv_serices.type,tv_serices.area_type,tv_serices.alias )

        #单集时长
        duration = re.findall('<span class="pl">单集片长:</span>(.*?)<br/>', html)
        if duration:
            tv_serices.duration= int(duration[0].strip(' ').rstrip('分钟'))


        #集数
        episodes = re.findall('<span class="pl">集数:</span>(.*?)<br/>', html)
        if episodes:
            tv_serices.episodes = int(episodes[0].strip(' '))

        print(duration,episodes)

        row += 1
        column += 1
        count += 1


        info.append(count)
        info.append(tv_serices.name)
        info.append(tv_serices.area_type)
        info.append(tv_serices.alias)
        info.append(tv_serices.type)
        info.append(tv_serices.year)
        info.append(0)
        info.append(0)
        info.append(tv_serices.duration)
        info.append(tv_serices.episodes)
        info.append(0)
        info.append(date)
        info.append(work_name)
        info.append(editor_name)
        info.append(resolution)
        print(info)

        for i in info:
            sheet.write(row,column,i)
            column +=1

    xls.save(str(date) + work_name + '（' + program_type + str(total) + '）' + '.xls')

def gen_xls_from_file(file):
    f = open(file, 'r')
    urls = []
    for line in f:
        line = line.strip('\n')
        urls.append(line)
    print(urls)
    gen_xls_from_urls(urls=urls)

if __name__ == '__main__':
    gen_xls_from_file(r'americandramas.txt')
    
    #成品的豆瓣链接
    urls = ['https://movie.douban.com/subject/26870087/','https://movie.douban.com/subject/26776350/','https://movie.douban.com/subject/26302614/','https://movie.douban.com/subject/27046252/','https://movie.douban.com/subject/4317602/','https://movie.douban.com/subject/26926437/','https://movie.douban.com/subject/26388908/']
    #gen_xls_from_urls(urls=urls)
   