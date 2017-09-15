class TVSeries:
    '''
    电视剧的类


    '序号',	'电视剧名称',	'电视剧类别',	'电视剧又名',	'类型',	'年份',	'片头',	'片尾',	'单集时长',	'集数',	'总时长',	'成品完成时间',	'压片人员',	'编辑人员',	'分辨率'
    '''
    def __init__(self):
        self.name = '电视剧名称'
        self.area_type = '电视剧类别'
        self.alias = '电视剧又名'
        self.type = '类型'
        self.year = 9999                #'年份'
        self.duration_title = 0          #'片头'
        self.duration_trailer = 0        #'片尾'
        self.duration = 0                #'单集时长'
        self.episodes = 0                #'集数'

if __name__ == '__main__':
    tv = TVSeries()
    print(tv.__dict__)