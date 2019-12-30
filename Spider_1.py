from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from lxml import etree
import xlwt
import time
import csv

class Spider:
    def __init__(self):
        self.runtime = None
        self.url = 'https://www.xiaomiyoupin.com/goodsbycategory?firstId=446&secondId=446&title=%E6%9C%89%E5%93%81%E6%8E%A8%E8%8D%90&spmref=YouPinPC.$Home$.list.0.94804387'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
  
  
        self.csvfilename = 'data_mi.csv'
        self.csvfilenamegbk= 'data_mi-gbk.csv'

    def run(self):
        for item in self.parse_page(self.get_page(self.url)):
            self.save_data(item)
            self.u8togbk(self.csvfilename, self.csvfilenamegbk)


    def get_page(self, url):
        self.browser.get(url)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div[1]/div[1]/img')))
        # 模拟下拉
        for i in range(50):
            js_to_buttom = "window.scrollBy(0,1000)"
            self.browser.execute_script(js_to_buttom)
            time.sleep(0.2)
        # 等待网页加载
        time.sleep(5)
        return self.browser.page_source

    def parse_page(self, text):
     #   workbook = xlwt.Workbook()  # 定义workbook
     #   sheet = workbook.add_sheet('xmyp')  # 添加sheet
     #   head = ['商品分类', '商品名称', '介绍', '价格', '图片地址']  # 表头
     #  for h in range(len(head)):
     #       sheet.write(0, h, head[h])  # 把表头写到Excel里面去
        html = etree.HTML(text)
       # j = 1
        for index in range(2,17):
            names = html.xpath('//*[@id="root"]/div/div[3]/div/div[{}]/div/div/p[1]/text()'.format(index))
            classes = html.xpath('//*[@id="root"]/div/div[3]/div/div[{}]/h2/text()'.format(index))[0]
            introduces = html.xpath('//*[@id="root"]/div/div[3]/div/div[{}]/div/div/p[2]/text()'.format(index))
            prices = html.xpath('//*[@id="root"]/div/div[3]/div/div[{}]/div/div/p[3]/span[2]/text()'.format(index))
            imgs = html.xpath('//*[@id="root"]/div/div[3]/div/div[{}]/div/div/div[1]/img/@src'.format(index))
            if len(names) != len(introduces) != len(prices) != len(imgs):
                raise Exception
            print(len(names),len(introduces),len(prices),len(imgs))
            for i in range(len(names)):
                yield [classes, names[i], introduces[i], prices[i], imgs[i]]
            #sheet.write(j, 0, names)  # 第i行，第1列
            # sheet.write(j, 1, classes)  # 第i行，第2列
            # sheet.write(j, 2, introduces)  # 第i行，第3列
            #sheet.write(j, 3, prices)  # 第i行，第4列
            #sheet.write(j, 4, imgs)  # 第i行，第5列
            #j += 1
            # 保存Excel表
      #  workbook.save(r'C:/Users/Administrator/Desktop/xmyp.xls')
      # print('写入excel成功')
      #  print("文件位置：")
      #  print("C:/Users/Administrator/Desktop/xmyp.xls")
      # print('\n')
    def save_data(self, item):
        with open(self.csvfilename, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(item)


    def u8togbk(self,infn,outfn):
        #这段是借来的
        with open(infn, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            results = list(reader)
        with open(outfn, 'w', encoding='gbk', newline='') as f:
            writer = csv.writer(f)
            for result in results:
                try:
                    writer.writerow(result)
                except Exception:
                    pass

    def mkxls(self, out_filename):
        #这段也是借来的
        def csv_to_xlsx(csvfile, outfile):
            with open(csvfile) as fc:
                r_csv = csv.reader(fc)
                workbook = xlwt.Workbook()
                sheet = workbook.add_sheet('sheet1')  # 创建一个sheet表格
                i = 0
                j = 0
                for line in r_csv:
                    j = 0
                    for v in line:
                        sheet.write(i, j, v)
                        j = j + 1
                    i = i + 1
                workbook.save(outfile)  # 保存Excel
        csv_to_xlsx(self.csvfilenamegbk, out_filename)

if __name__ == '__main__':
    spider = Spider()
    spider.run()  # 运行爬虫
    spider.mkxls('data_mi.xls')


