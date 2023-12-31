import xml.etree.ElementTree as ET
import requests
import time
from openpyxl import Workbook


# The given XML parameters
xml_params = '''
<params>
  <URL>https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY</URL>
  <excelName>南亞</excelName>
  <startYear>2020</startYear>
  <startMonth>01</startMonth>
  <endYear>2023</endYear>
  <endMonth>06</endMonth>
  <StockNo>1303</StockNo>
</params>
'''

def print_params(params):
    for key, value in params.items():
        print(f"{key}: {value}")
def fillSheet(sheet,data,row):#建立這個來存參數
    for column, value in enumerate(data,1):# 讀取資料
        sheet.cell(row=row,column=column,value=value)
        #將資料放置在row行column列上，其格子裡填寫value資料
def returnStrDayList(startYear,startMonth,endYear,endMonth,day="01"):
    result=[]
    if startYear==endYear:
        for month in range(startMonth,endMonth+1):
            month=str(month)
            if len(month)==1:
                month="0"+month
            result.append(str(year)+month+day)
        return result
    for year in range(startYear,endYear+1):
        if year == startYear:
            for month in range(startMonth,13):
                month=str(month)
                if len(month)==1:
                    month="0"+month
                result.append(str(year)+month+day)
        elif year == endYear:
            for month in range(1,endMonth+1):
                month=str(month)
                if len(month)==1:
                    month="0"+month
                result.append(str(year)+month+day)
        else:
            for month in range(1,13):
                month=str(month)
                if len(month)==1:
                    month="0"+month
                result.append(str(year)+month+day)
    return result

# Parse the XML string
root = ET.fromstring(xml_params)

# Convert XML to dictionary
params_dict = {}
for element in root:
    params_dict[element.tag] = element.text

# Print the resulting dictionary
print_params(params_dict)
fields=["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
wb=Workbook()#建立excel
sheet=wb.active#make excel start
sheet.title="fields"
fillSheet(sheet,fields,1)
startYear,startMonth=int(params_dict["startYear"]),int(params_dict["startMonth"])
endYear,endMonth=int(params_dict["endYear"]),int(params_dict["endMonth"])
#上兩行讀取字典內容並順便變成正整數
yearlist=returnStrDayList(startYear,startMonth,endYear,endMonth)#執行
#print(yearlist)
row=2
for YearMonth in yearlist:
    rq=requests.get(params_dict["URL"],params={
        "response":"json",
        "data": YearMonth,
        "stockNo":params_dict["StockNo"]
    })
    jsonData=rq.json()
    dailyPriceList=jsonData.get("data",[])
    for dailyPrice in dailyPriceList:
        fillSheet(sheet,dailyPrice,row)
        row+=1
    time.sleep(3)
name=params_dict["excelName"]
wb.save(name+".xlsx")#save


