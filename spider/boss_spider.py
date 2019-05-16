import requests
from fake_useragent import UserAgent
import time
import random
import pandas as pd
from lxml import etree
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


def get_html(url):
    """获取网页请求文件"""

    ua = UserAgent()
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'user-agent': ua.random
               }
    # proxies = {
    #            'https': '121.63.199.40:9999'
    #           }
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    return html


def parse_data(html):
    """解析数据"""

    job_infos = html.xpath('//*[@id="main"]/div/div[2]/ul/li')
    all_job_information = []
    for job_info in job_infos:
        try:
            job_title = job_info.xpath('.//div[@class="info-primary"]/h3/a/div[@class="job-title"]/text()')[0]  # 职位名称
            salary = job_info.xpath('.//div[@class="info-primary"]/h3/a/span/text()')[0]  # 工资
            company_address = job_info.xpath('.//div[@class="info-primary"]/p/text()[1]')[0]  # 公司地址
            working_years = job_info.xpath('.//div[@class="info-primary"]/p/text()[2]')[0]  # 工作年限
            education = job_info.xpath('.//div[@class="info-primary"]/p/text()[3]')[0]  # 学历
            company = job_info.xpath('.//div[@class="info-company"]/div/h3/a/text()')[0]  # 公司名称
            industry = job_info.xpath('.//div[@class="info-company"]/div/p//text()[1]')[0]  # 公司行业
            is_public = job_info.xpath('.//div[@class="info-company"]/div/p//text()[2]')[0]  # 是否上市
            employee_numbers =job_info.xpath('.//div[@class="info-company"]/div/p//text()[3]')[0] # 员工人数
            job_detail_url = 'https://www.zhipin.com' + job_info.xpath('.//div[@class="info-primary"]/h3/a/@href')[0]  #  详情链接
            # 发布日期解析不知道为什么一直为空
            # publish_date = job_info.xpath('.//div[@class="info-publis"]/p/text()')
            job_information = [job_title, salary, working_years, education, company, company_address, industry,
                           is_public, employee_numbers, job_detail_url]
            all_job_information.append(job_information)
        except IndexError:
            pass
    return all_job_information


# def get_job_description():
#     """使用selenium抓取职位描述"""
#     chrome_options = webdriver.ChromeOptions()
#     # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
#     chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--ignore-ssl-errors')
#     driver = webdriver.Chrome(chrome_options=chrome_options)
#     # driver.implicitly_wait(10)
#     driver.get('https://www.zhipin.com/c101280600/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&page=1&ka=page-1')
#     action = ActionChains(driver)
#     tags = driver.find_elements_by_class_name('job-title')
#     job_descriptions = []
#     for tag in tags:
#         print(tag.text)
#         action.move_to_element(tag).perform()
#         # time.sleep(2)
#         # job_description = driver.find_element_by_class_name('detail-bottom-text')
#         wait = WebDriverWait(driver, 5)
#         job_description = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'detail-bottom-text')))
#         print(job_description.text)


def save_data(job_data):
    """保存数据为CSV文件"""

    df = pd.DataFrame(job_data)
    header = ['job_title', 'salary', 'working_years', 'education', 'company', 'company_address', 'industry',
              'is_public', 'employee_numbers', 'job_detail_url']
    df.to_csv(r'C:\Users\KILO\Desktop\python document\boss_hangzhou.csv', header=header, encoding='utf_8_sig')


def main():
    page_num = int(input('请输入需要抓取的页数: '))
    job_data = []
    for i in range(1, page_num+1):
        url = 'https://www.zhipin.com/c101210100/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&page=' + str(
            i) + '&ka=page-' + str(i)
        print('正在抓取第' + str(i) + '页')
        print(url)
        html = get_html(url)
        all_job_information = parse_data(html)
        job_data = job_data + all_job_information
        time.sleep(random.randint(3, 5))
    save_data(job_data)


if __name__ == '__main__':
    main()
