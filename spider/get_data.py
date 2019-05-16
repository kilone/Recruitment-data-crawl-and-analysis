import requests
from fake_useragent import UserAgent
import time
import pandas as pd


def get_data(url, data):
    ua = UserAgent()
    headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://www.lagou.com',
                'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
                'User-Agent': ua.random,
                }
    time.sleep(5)
    session = requests.session()
    session.headers.update(headers)
    session.get('https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=sug&fromSearch=true&suginput=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90')
    r = session.post(url, data=data)  # 获取此次文本
    content = r.json()
    info = content['content']['positionResult']['result']
    info_list = []
    for job in info:
        information = []
        information.append(job['positionId'])  # 岗位对应ID
        information.append(job['city'])  # 岗位对应城市
        information.append(job['companyFullName'])  # 公司全名
        information.append(job['companyLabelList'])  # 福利待遇
        information.append(job['companySize'])    # 公司规模
        information.append(job['industryField'])  # 公司行业
        information.append(job['financeStage'])   # 融资阶段
        information.append(job['district'])  # 工作地点
        information.append(job['education'])  # 学历要求
        information.append(job['firstType'])  # 工作类型
        information.append(job['formatCreateTime'])  # 发布时间
        information.append(job['positionName'])  # 职位名称
        information.append(job['salary'])  # 薪资
        information.append(job['workYear'])  # 工作年限
        info_list.append(information)
    return info_list


def save_data(info_result):
    df = pd.DataFrame(info_result)
    df.to_csv(r'C:\Users\KILO\Desktop\python document\lagou_hangzhou.csv', encoding='utf_8_sig')


def main():
    page = int(input("请输入要抓取的页码总数："))
    info_result = []
    title = ['岗位id', '城市', '公司全名', '福利待遇', '公司规模', '公司行业', '融资阶段', '工作地点', '学历要求', '工作类型', '发布时间', '职位名称', '薪资', '工作年限']
    info_result.append(title)
    for x in range(1, page+1):
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false'
        data = {
            'first': 'true',
            'pn': x,
            'kd': '数据分析'
        }
        try:
            info = get_data(url, data)
            info_result = info_result + info
            print("第%s页正常采集" % x)
        except Exception as msg:
            print("第%s页出现问题" % x)
    save_data(info_result)


if __name__ == '__main__':
    main()
