import imp
from importlib.resources import contents
import json
from tkinter import Listbox, Variable
from django.shortcuts import render, HttpResponse
import os
import datetime
from matplotlib.font_manager import json_dump
from matplotlib.style import context
import pandas as pd
from django.template.response import TemplateResponse
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
# from datetime import date, timedelta
# from datetime import datetime
import calendar
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os


# Create your views here.

df = pd.read_csv('media/AutoInventoryData.csv')


def testa(request):

    import json

    mylistraw_a = ['a', 'b', 'c', 'd']
    mylist_a = json.dumps(mylistraw_a)

    context = {'mylistjson2': mylist_a}

    return render(request, 'est.html', context)


def test(request):

    CM = df.groupby('Month').get_group('Mar')
    CM.reset_index(inplace=True, drop=True)

    print('Regular Item')
    Most_Sale_Category_CM = CM.groupby(["MenuCateogry"])
    Most_Sale_Category_CM = Most_Sale_Category_CM[['ItemQty']]
    Most_Sale_Category_CM = Most_Sale_Category_CM.sum(
    ).sort_values(by='ItemQty', ascending=False)
    Most_Sale_Category_CM = Most_Sale_Category_CM.head(5)

    Most_Sale_Category_CM.reset_index(level=0, inplace=True)

    Most_Sale_Category_CM.rename(
        columns={'MenuCateogry': 'Item', 'ItemQty': 'Sales'}, inplace=True)

    x = Most_Sale_Category_CM.Sales.tolist()

    import json

    mylistraw = x
    mylist = json.dumps(mylistraw)

    context = {'mylistjson': mylist }

    return render(request, 'demo1/base.html', context)


def dashboard(request):
    import pandas as pd
    indian_rupee = u"\u20B9"
# df = pd.read_csv('media/Inventory_Data.csv')

    month_last_date = {
        "month": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        "LastDate": [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]}

    month_last_date = pd.DataFrame(month_last_date)

    Week_Table = {
        "weekday": ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}

    Week_Table = pd.DataFrame(Week_Table)

    Item_Table = {}

    Item_Table = pd.DataFrame(Item_Table)

    current_time = datetime.datetime.now()
    #TodayMonth = current_time.strftime("%b")  # get the current month
    TodayMonth = 'Jun'
    print("This is Errror here",TodayMonth)   
    #TodayDate = current_time.day  # get the current date
    TodayDate = 14
    TodayMonth_data = df.groupby('Month').get_group(TodayMonth)

    print(TodayMonth_data)

    #TodayMonth_data = df.groupby('Month').get_group(TodayMonth)
    TodayDate_data = TodayMonth_data.groupby('Day').get_group(TodayDate)
    todayttl = TodayDate_data.Total.sum()  # sum of current date total revvenue

    # get the yesterday date and print the data
    yesterdayDate = int(datetime.date.fromordinal(
        datetime.date.today().toordinal()-1).strftime("%d"))
    yesterdayDate_data = TodayMonth_data.groupby(
        'Day').get_group(yesterdayDate)
    yesterdayttl = yesterdayDate_data.Total.sum()
    # yesterdayttl = 1500

    diff = abs(todayttl - yesterdayttl)

    TodayMS = {}  # create dataframe to store today data about most slae prodcts
    TodayMS = pd.DataFrame(TodayMS)

    # code to fetch the most sale item
    TodaySaleProduct = TodayDate_data.groupby(["MenuItem"])
    TodaySaleProduct = TodaySaleProduct[['ItemQty']]
    TodaySaleProduct = TodaySaleProduct.sum().sort_values(by='ItemQty', ascending=False)
    MS_item = TodaySaleProduct.head(7)

    tms = list(MS_item.index)  # today most sale item
    TodayMS['MostSaleItem'] = tms

    df_tms = TodayMS
    json_records_a = df_tms.reset_index().to_json(orient='records')
    MSIarr = []
    MSIarr = json.loads(json_records_a)

    # fetch the most sold category
    TodayMonth_data = df.groupby('Month').get_group(TodayMonth)
    TodayDate_cat = TodayMonth_data.groupby('Day').get_group(TodayDate)
    todaycatttl = TodayDate_cat.Total.sum()  # sum of current date total revvenue

# display(TodayDate_data)

 # Total Party comes per day on weekend is 14

    TodayCat = {
    }

    TodayCat = pd.DataFrame(TodayCat)
    # display(TodayCat)

    TodaySaleCat = TodayDate_cat.groupby(["MenuCateogry"])
    TodaySaleCat = TodaySaleCat[['ItemQty']]
    TodaySaleCat = TodaySaleCat.sum().sort_values(
        by='ItemQty', ascending=False).head()

# display(TodaySaleProduct)

    Mscat = list(TodaySaleCat.index)
    TodayCat['MSC'] = Mscat
    TodayCat = pd.DataFrame(TodayCat)
# display(TodayCat)

    json_records_cat = TodayCat.reset_index().to_json(orient='records')
    data = []
    catdata = json.loads(json_records_cat)


# -----------------------------------------------------------------------------------------------------------------------------

    # total customer
   # TodayMxS
    x = df.groupby('Month').get_group(TodayMonth)
    y = x.groupby('Day').get_group(TodayDate)
    JanID = y[['OrderId', 'PartySize']]
    SoP = JanID.drop_duplicates()
    Sop = SoP.PartySize.sum()  # Sum of people come to resto today
    OrTty = SoP.OrderId.count()  # Sum of Order come to resto today
    NoP_MostSale = y.MenuItem.mode().values[0]
    itemqty = y.ItemQty.sum()
    #leastsaleitem = TodayMxS.tail(1)
    #leastsaleitem = leastsaleitem.MostSaleItem.mode().values[0]

# ------------------------------------------------------------------------------------------------------------------------
    # from datetime import date
    # from datetime import datetime
    # datetime.datetime.now()
    # from dateutil.relativedelta import relativedelta

    today = date.today()
    lastmonth = date.today().replace(day=1) - timedelta(1)
    last_Month = lastmonth.strftime("%b")

    d2 = today.strftime("%B %d, %Y")
    # Date = int(today.strftime("%d"))   #DEMO SAY ITS - 10
    Date = 24
    # Month = today.strftime("%b")
    Month = TodayMonth
# print(Date, Month)
   # Weekday_name = datetime.today().strftime('%A')

    month_data = df.groupby('Month').get_group(Month)  # current data month
    previous_month_data = df.groupby('Month').get_group(last_Month)
    # display('current month',month_data)
    # display('last month',previous_month_data)

    Week_To = Date - 1
# if(Weekday_name == 'Sunday'):
    if(Week_To <= 7):
        # Tab 3  #currentmonth
        Month_Half_1st = month_data.loc[(month_data.Day <= Week_To)]
        # display(Month_Half_1st)
        last_date_pevious_month = df.groupby('Month').get_group(
            last_Month).tail(1).Day.values[0]  # last day of previous month
        # display(last_date_pevious_month)
        Day_left = 7 - Week_To
        # display(Day_left)
        Week_from = last_date_pevious_month - (Day_left - 1)
        # display(Week_from)
        Last_Month_Half_2nd = previous_month_data.loc[(previous_month_data.Day >= Week_from) & (
            previous_month_data.Day <= last_date_pevious_month)]  # lastmonth
        # display(Last_Month_Half_2nd)
        Mergeframes = [Last_Month_Half_2nd, Month_Half_1st]
        Previous_Week_Data = pd.concat(Mergeframes)
        # display(Previous_Week_Data)  #Merge data of last and current data
        # display(Previous_Week_Data['WeekDay'].unique())

    else:
        Week_from = abs(Week_To - 6)
        Previous_Week_Data = month_data.loc[(
            month_data.Day >= Week_from) & (month_data.Day <= Week_To)]
        # display(Previous_Week_Data)
        # display(Previous_Week_Data['WeekDay'].unique())

    for i in range(0, 7):
        weekday = str(Week_Table.loc[[i], 'weekday'].values[0])
        weekday_data = Previous_Week_Data.groupby('WeekDay').get_group(
            weekday)  # Total Party comes per day on weekend is 14
        Top_Qty = weekday_data.groupby(["MenuItem"])
        Top_Qty = Top_Qty[['ItemQty']]
        Top_Qty = Top_Qty.sum().sort_values(by='ItemQty', ascending=False).head(10)

        if(weekday == 'Sunday'):
            Sunday = list(Top_Qty.index)
            Item_Table['Sunday'] = Sunday
        # display(Sunday)

        elif(weekday == 'Monday'):
            Monday = list(Top_Qty.index)
            Item_Table['Monday'] = Monday
        # display(Monday)

        elif(weekday == 'Tuesday'):
            Tuesday = list(Top_Qty.index)
            Item_Table['Tuesday'] = Tuesday
        # display(Tuesday)

        elif(weekday == 'Wednesday'):
            Wednesday = list(Top_Qty.index)
            Item_Table['Wednesday'] = Wednesday
        # display(Wednesday)

        elif(weekday == 'Thursday'):
            Thursday = list(Top_Qty.index)
            Item_Table['Thursday'] = Thursday
        # display(Thursday)

        elif(weekday == 'Friday'):
            Friday = list(Top_Qty.index)
            Item_Table['Friday'] = Friday
        # display(Friday)

        elif(weekday == 'Saturday'):
            Saturday = list(Top_Qty.index)
            Item_Table['Saturday'] = Saturday
        # display(Saturday)
    # display(Item_Table[['Friday','Saturday','Sunday']])
    weekend_data = Item_Table
    weekend_data = pd.DataFrame(weekend_data)

    json_records = weekend_data.reset_index().to_json(orient='records')
    weekdaydata = []
    wddata = json.loads(json_records)

    # -----------------------------------------------------------------------------------------------------------------------------

    CM = df.groupby('Month').get_group('Mar')
    CM.reset_index(inplace=True, drop=True)

    print('Regular Categoery')
    Most_Sale_Category_CM = CM.groupby(["MenuCateogry"])
    Most_Sale_Category_CM = Most_Sale_Category_CM[['ItemQty']]
    Most_Sale_Category_CM = Most_Sale_Category_CM.sum(
    ).sort_values(by='ItemQty', ascending=False)
    Most_Sale_Category_CM = Most_Sale_Category_CM.head(5)

    Most_Sale_Category_CM.reset_index(level=0, inplace=True)

    Most_Sale_Category_CM.rename(
        columns={'MenuCateogry': 'Item', 'ItemQty': 'Sales'}, inplace=True)

    CatM = Most_Sale_Category_CM.Sales.tolist()

    mylistrawcatm = CatM
    mylistcatm = json.dumps(mylistrawcatm)

    json_records_CM = Most_Sale_Category_CM.reset_index().to_json(orient='records')
    Cat_CM = []
    Cat_CM = json.loads(json_records_CM)

    # -------------------------------------------------------------------------------------------------------------------------

    IM = df.groupby('Month').get_group('Mar')
    IM.reset_index(inplace=True, drop=True)

    print('Regular Item')
    Most_Sale_Item_IM = IM.groupby(["MenuItem"])
    Most_Sale_Item_IM = Most_Sale_Item_IM[['ItemQty']]
    Most_Sale_Item_IM = Most_Sale_Item_IM.sum(
    ).sort_values(by='ItemQty', ascending=False)
    Most_Sale_Item_IM = Most_Sale_Item_IM.head(10)

    Most_Sale_Item_IM.reset_index(level=0, inplace=True)

    Most_Sale_Item_IM.rename(
        columns={'MenuItem': 'Item', 'ItemQty': 'Sales'}, inplace=True)

    ItemIM = Most_Sale_Item_IM.Sales.tolist()

    mylistrawitemim = ItemIM
    mylistitemim = json.dumps(mylistrawitemim)

    json_records_IM = Most_Sale_Item_IM.reset_index().to_json(orient='records')
    ItemM = []
    ItemM = json.loads(json_records_IM)

    # -------------------------------------------------------------------------------------------------------------------------

    # specialist
    print('specialist Product sale of prevous week')
# -------------------------------------------------------------------------------------------------------------

    Specialist_Item = {
        'Item': ['Butter chicken', 'Chicken korma', 'Vegetable pakora', 'Fish curry', 'Chicken saag', 'Rasmalai', 'Gulabjamun', 'Malpura', 'Kheer', 'Chicken biryani'],
        'Sales': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    }

    Specialist_Item = pd.DataFrame(Specialist_Item)

# display(Specialist_Item)


# -------------------------------------------------------------------------------------------------------------

# SI = Specialist_Item.iloc[3,0]
# x = Previous_Week_Data[Previous_Week_Data.MenuItem == SI]

# x.count().values[0]

# -------------------------------------------------------------------------------------------------------------

    for i in range(0, len(Specialist_Item)):
        SI = Specialist_Item.iloc[i, 0]
        DataFetch_SI = Previous_Week_Data[Previous_Week_Data.MenuItem == SI]
        DataFetch_SI_count = DataFetch_SI.count().values[0]
    # print(DataFetch_SI_count)
        Specialist_Item.iloc[i, 1] = DataFetch_SI_count

    print('Special Item Sale')
    # Specialist_Item
    json_records_SP = Specialist_Item.reset_index().to_json(orient='records')
    ItemSP = []
    ItemSP = json.loads(json_records_SP)

    # -------------------------------------------------------------------------------------------------------------------------

    # Expensive Product
    print('Expensive Product sale of prevous week')
# -------------------------------------------------------------------------------------------------------------

    Expensive_Item = {
        'Item': ['Cocktail chicken samosas', 'Kadahi paneer', 'Hara bhara kabob', 'Shrimp strips', 'Spicy chicken bites'],
        'Sales': [np.nan, np.nan, np.nan, np.nan, np.nan]
    }

    Expensive_Item = pd.DataFrame(Expensive_Item)


# display(Specialist_Item)


# -------------------------------------------------------------------------------------------------------------

# SI = Specialist_Item.iloc[3,0]
# x = Previous_Week_Data[Previous_Week_Data.MenuItem == SI]

# x.count().values[0]

# -------------------------------------------------------------------------------------------------------------

    for i in range(0, len(Expensive_Item)):
        EI = Expensive_Item.iloc[i, 0]
        DataFetch_EI = Previous_Week_Data[Previous_Week_Data.MenuItem == EI]
        DataFetch_EI_count = DataFetch_EI.count().values[0]
    # print(DataFetch_SI_count)
        Expensive_Item.iloc[i, 1] = DataFetch_EI_count

   # Expensive_Item  = Expensive_Item.sort_values(by='Sales', ascending=False)

    print('Expensive Item Sale')
    json_records_EP = Expensive_Item.reset_index().to_json(orient='records')
    ItemEP = []
    ItemEP = json.loads(json_records_EP)

    # Expensive_Item

 # -------------------------------------------------------------------------------------------------------------------------

    CM = df.groupby('Month').get_group('Mar')
    CM.reset_index(inplace=True, drop=True)
    CMSum = CM.groupby(["Day"]).sum()
    MonthAve = CMSum['Total'].mean()
    MonthAve = round(MonthAve, 2)
 # -------------------------------------------------------------------------------------------------------------------------
# GETTing the list of product which we broughy

# weekday
    


    print('')
    print('Weekend Data')
    Weekend_Data = weekend_data[['Friday', 'Saturday', 'Sunday']]
    # display(Weekend_Data)

    print('')
    print('Weekday Data')
    Weekday_Data = weekend_data[['Monday', 'Tuesday', 'Wednesday', 'Thursday']]
    # display(Weekday_Data)

    WeekdayAllData = {}
    WeekdayAllData = pd.DataFrame(WeekdayAllData)

    Weekday_Add1 = Weekday_Data['Monday'].append(Weekday_Data['Tuesday'])
    Weekday_Add2 = Weekday_Add1.append(Weekday_Data['Wednesday'])
    Weekday_Add = Weekday_Add2.append(Weekday_Data['Thursday'])
    WeekdayAllData['Data'] = Weekday_Add

    WeekdayD = WeekdayAllData.drop_duplicates()
    WeekdayD.reset_index(inplace=True, drop=True)

   # WeekdayD

    # Weekdend prediction

    WeekendAllData = {}
    WeekendAllData = pd.DataFrame(WeekendAllData)

    Weekend_Add1 = Weekend_Data['Friday'].append(Weekend_Data['Saturday'])
    Weekend_Add2 = Weekend_Add1.append(Weekend_Data['Sunday'])
    WeekendAllData['Data'] = Weekend_Add2

    WeekendD = WeekendAllData.drop_duplicates()
    WeekendD.reset_index(inplace=True, drop=True)


# weekday-------------------------------------------------------------------------------------------
    # Max - Intersect between Weekday and Weekend
# print('Max')
    MWe = WeekendD
    MWd = WeekdayD
    Max_Product_Brought_Weekday = MWd.merge(MWe)
    Max_Product_Brought_Weekday.reset_index(inplace=True, drop=True)  # This is brought is max quantiy
# display(Max_Product_Brought_Weekday)

# Normal - #Only weekday
# print('Normal')
    Normal_Product_Brought_weekday_only = WeekdayD[WeekdayD.Data.isin(WeekendD.Data) == False]
    Normal_Product_Brought_weekday_only.reset_index(inplace=True, drop=True)
# display(Normal_Product_Brought_weekday_only)

# print('Min')
# Mininum product Only weekend
    Min_Product_Brought_weekday_only = WeekendD[WeekendD.Data.isin(WeekdayD.Data) == False]
    Min_Product_Brought_weekday_only.reset_index(inplace=True, drop=True)
# display(Min_Product_Brought_weekday_only)

# WeekendD

    Previous_Week_Data_WeekdayInfo = Previous_Week_Data.groupby('Day Type').get_group('Weekday')
    Previous_Week_Data_WeekdayInfo_Monday = Previous_Week_Data.groupby('WeekDay').get_group('Monday')
    Previous_Week_Data_WeekdayInfo_Tuesday = Previous_Week_Data.groupby('WeekDay').get_group('Tuesday')
    Previous_Week_Data_WeekdayInfo_Wednesday = Previous_Week_Data.groupby('WeekDay').get_group('Wednesday')
    Previous_Week_Data_WeekdayInfo_Thursday = Previous_Week_Data.groupby('WeekDay').get_group('Thursday')
    x1 = Previous_Week_Data_WeekdayInfo_Monday.append(Previous_Week_Data_WeekdayInfo_Tuesday)
    x2 = x1.append(Previous_Week_Data_WeekdayInfo_Wednesday)
    x3 = x2.append(Previous_Week_Data_WeekdayInfo_Thursday)
    Weekday_CountGame = x3
# display(Weekday_CountGame)

# display(Weekend_CountGame)
    wkd = Weekday_CountGame[['MenuItem', 'ItemPrice', 'ItemQty', 'Total']]
    # Total item sale per day on weekend is 143
    wkdRND = wkd.groupby(["MenuItem"])
    wkdRND = wkdRND[['ItemQty']]
    # Per day 43 different product sales
    wkdRND = wkdRND.sum().sort_values(by='ItemQty', ascending=False)
    wkRND = wkdRND['ItemQty'].sum()
    wkdRND = wkdRND.reset_index()


# weekday
# Bring Product list of Weekday
# Max product
    maxItem = []
    maxqty = []
    Item_Bring_Max_List_weekday = {}
    Item_Bring_Max_List_weekday = pd.DataFrame(Item_Bring_Max_List_weekday)

    for i in range(0, len(Max_Product_Brought_Weekday)):
      Max_Item = Max_Product_Brought_Weekday.iloc[i, 0]

      for j in range(0, len(wkdRND)):
            Main_Item = wkdRND.iloc[j, 0]
            Main_qty = wkdRND.iloc[j, 1]

            if(Main_Item == Max_Item):
                maxItem.append(Main_Item)
                maxqty.append(Main_qty)

    Item_Bring_Max_List_weekday['Items'] = maxItem
    Item_Bring_Max_List_weekday['Qty'] = maxqty

# print('Team 2 Score of best batsmen score is ',T2_batting_score)

# print('')
# display(Item_Bring_Max_List_weekday)


# weekday
# Bring Product list of Weekday
# Normal product
    normalItem = []
    normalqty = []
    Item_Bring_normal_List_weekday = {}
    Item_Bring_normal_List_weekday = pd.DataFrame(
    Item_Bring_normal_List_weekday)

    for i in range(0, len(Normal_Product_Brought_weekday_only)):
          Normal_Item = Normal_Product_Brought_weekday_only.iloc[i, 0]

          for j in range(0, len(wkdRND)):
            Main_Item = wkdRND.iloc[j, 0]
            Main_qty = wkdRND.iloc[j, 1]

            if(Main_Item == Normal_Item):
                normalItem.append(Main_Item)
                normalqty.append(Main_qty)

    Item_Bring_normal_List_weekday['Items'] = normalItem
    Item_Bring_normal_List_weekday['Qty'] = normalqty

# print('Team 2 Score of best batsmen score is ',T2_batting_score)
# display(Item_Bring_normal_List_weekday)
# print('')


# weekday
# Bring Product list of Weekday
# Min product
    minItem = []
    minqty = []
    Item_Bring_Min_List_weekday = {}
    Item_Bring_Min_List_weekday = pd.DataFrame(Item_Bring_Min_List_weekday)

    for i in range(0, len(Min_Product_Brought_weekday_only)):
          Min_Item = Min_Product_Brought_weekday_only.iloc[i, 0]

          for j in range(0, len(wkdRND)):
            Main_Item = wkdRND.iloc[j, 0]
            Main_qty = wkdRND.iloc[j, 1]

            if(Main_Item == Min_Item):
                minItem.append(Main_Item)
                minqty.append(Main_qty)

    Item_Bring_Min_List_weekday['Items'] = minItem
    Item_Bring_Min_List_weekday['Qty'] = minqty

# print('Team 2 Score of best batsmen score is ',T2_batting_score)
# display(Item_Bring_Min_List_weekday)
# print('')

    x1 = Item_Bring_Max_List_weekday.append(Item_Bring_normal_List_weekday)
    WEEKDAY_LIST = x1.append(Item_Bring_Min_List_weekday)
    WEEKDAY_LIST = WEEKDAY_LIST.sort_values(by='Qty', ascending=False)
    WEEKDAY_LIST.reset_index(inplace=True, drop=True)
    WEEKDAY_LIST.to_csv('WEEKDAY_LIST.csv', encoding='utf-8')
# display(WEEKDAY_LIST)
        

 #-------------------------------------------------------------------------------------------------------------------
        #store and generate csv file and delete the previous one
        #weekday
#weekday mail

    
       
# first check whether file exists or not
# calling remove method to delete the csv file
# in remove method you need to pass file name and type
    curr_date = date.today()
    TWeekday = calendar.day_name[curr_date.weekday()]
   # TWeekday ='Sunday'
    if(TWeekday == 'Sunday'):
        a = TWeekday 

        fileW = 'WEEKDAY_LIST.csv'
        if(os.path.exists(fileW) and os.path.isfile(fileW)):
          os.remove(fileW)
          print("file deleted")
          WEEKDAY_LIST.to_csv('WEEKDAY_LIST.csv', encoding='utf-8')
        else:
          print("file not found")
          WEEKDAY_LIST.to_csv('WEEKDAY_LIST.csv', encoding='utf-8')


        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        

# this is python 2 and 3 compatible

      #  COMMASPACE = ', '

      #  sender = 'vsonar321@gmail.com'
      #  recipients = ['vsonar61@gmail.com', 'vishalsonar554@gmail.com']
      #  subject = 'Weekday Product list'
      #  body = """Hello sir/maam,
       # This CSV file contain the list of product thats should be brought on Monday Morning, Thank You"""

      #  msg = MIMEMultipart()
        #msg['Subject'] = subject
      ##  msg['To'] = COMMASPACE.join(recipients)
        #msg.preamble = subject # for clients without multipart support

# attachment file(s)
      #  filename = "WEEKDAY_LIST.csv"
      #  with open(filename, "r") as text_file:
      #   attachment = MIMEText(text_file.read())
      #   attachment.add_header('Content-Disposition', 'attachment', filename=filename)
       #  msg.attach(attachment)

#body
      #  msg.attach(MIMEText(body, 'plain'))


      #  s = smtplib.SMTP('smtp.gmail.com', 587)
      #  s.starttls()
      #  s.login("vsonar321@gmail.com", "hoovyyyleoerupgi")
      #  s.sendmail(sender, recipients, msg.as_string())
      #  s.quit()

# -------------------------------------------------------------------------------------------------------------------------



    print('Weekday Brough item')
    json_records_WEEKDAY_LIST = WEEKDAY_LIST.reset_index().to_json(orient='records')
    WEEKDAY_LIST = []
    WEEKDAY_LIST = json.loads(json_records_WEEKDAY_LIST)
# -------------------------------------------------------------------------------------------------------------------------
          

# -------------------------------------------------------------------------------------------------------------------------
# wweekenddd
# GETTing the list of product which we broughy
    curr_date = date.today()
    TWeekday = calendar.day_name[curr_date.weekday()]
    if(TWeekday == 'Friday'):
        a = TWeekday

# Max - Intersect between Weekday and Weekend
# print('Max')
    MWe = WeekendD
    MWd = WeekdayD
    Max_Product_Brought_Weekend = MWe.merge(MWd)
# display(Max_Product_Brought_Weekend)  #This is brought is max quantiy


# Normal - #Only Weekend
# print('Normal')
    Normal_Product_Brought_weekend_only = WeekendD[WeekendD.Data.isin(WeekdayD.Data) == False]
# display(Normal_Product_Brought_weekend_only)

# print('Min')
# Mininum product Only weekday
    Min_Product_Brought_weekend_only = WeekdayD[WeekdayD.Data.isin(WeekendD.Data) == False]
# display(Min_Product_Brought_weekend_only)

    Previous_Week_Data_WeekendInfo = Previous_Week_Data.groupby('Day Type').get_group('Weekend')
    Previous_Week_Data_WeekendInfo_Friday = Previous_Week_Data.groupby('WeekDay').get_group('Friday')
    Previous_Week_Data_WeekendInfo_Saturday = Previous_Week_Data.groupby('WeekDay').get_group('Saturday')
    Previous_Week_Data_WeekendInfo_Sunday = Previous_Week_Data.groupby('WeekDay').get_group('Sunday')
    y1 = Previous_Week_Data_WeekendInfo_Friday.append(Previous_Week_Data_WeekendInfo_Saturday)
    y2 = y1.append(Previous_Week_Data_WeekendInfo_Sunday)

    Weekend_CountGame = y2
# display(Weekend_CountGame)
    wnd = Weekend_CountGame[['MenuItem', 'ItemPrice', 'ItemQty', 'Total']]
    # Total item sale per day on weekend is 143
    wndRND = wnd.groupby(["MenuItem"])
    wndRND = wndRND[['ItemQty']]
    # Per day 43 different product sales
    wndRND = wndRND.sum().sort_values(by='ItemQty', ascending=False)
    wndRND = wndRND.reset_index()
# display(wndRND)

    LWND_OD_PS = Weekend_CountGame[['OrderId', 'PartySize']]
    LWND_OD_PS = LWND_OD_PS.drop_duplicates()
    print('Total No of people come on last week weekend is',
    LWND_OD_PS.PartySize.sum())


# weekend
# Bring Product list of Weekend+

# Max product
    maxItemE = []
    maxqtyE = []
    Item_Bring_Max_List_weekend = {}
    Item_Bring_Max_List_weekend = pd.DataFrame(Item_Bring_Max_List_weekend)

    for i in range(0, len(Max_Product_Brought_Weekend)):
          Max_ItemE = Max_Product_Brought_Weekend.iloc[i, 0]

          for j in range(0, len(wndRND)):
            Main_ItemE = wndRND.iloc[j, 0]
            Main_qtyE = wndRND.iloc[j, 1]

            if(Main_ItemE == Max_ItemE):
                maxItemE.append(Main_ItemE)
                maxqtyE.append(Main_qtyE)

    Item_Bring_Max_List_weekend['Items'] = maxItemE
    Item_Bring_Max_List_weekend['Qty'] = maxqtyE

# print('Team 2 Score of best batsmen score is ',T2_batting_score)

# print('')
# display(Item_Bring_Max_List_weekday)


# weekday
# Bring Product list of Weekday
# Normal product
    normalItemE = []
    normalqtyE = []
    Item_Bring_normal_List_weekend = {}
    Item_Bring_normal_List_weekend = pd.DataFrame(Item_Bring_normal_List_weekend)

    for i in range(0, len(Normal_Product_Brought_weekend_only)):
          Normal_ItemE = Normal_Product_Brought_weekend_only.iloc[i, 0]

          for j in range(0, len(wndRND)):
            Main_ItemE = wndRND.iloc[j, 0]
            Main_qtyE = wndRND.iloc[j, 1]

            if(Main_ItemE == Normal_ItemE):
                normalItemE.append(Main_ItemE)
                normalqtyE.append(Main_qtyE)

    Item_Bring_normal_List_weekend['Items'] = normalItemE
    Item_Bring_normal_List_weekend['Qty'] = normalqtyE

# print('Team 2 Score of best batsmen score is ',T2_batting_score)
# display(Item_Bring_normal_List_weekday)
# print('')


# weekday
# Bring Product list of Weekday
# Min product
    minItemE = []
    minqtyE = []
    Item_Bring_Min_List_weekend = {}
    Item_Bring_Min_List_weekend = pd.DataFrame(Item_Bring_Min_List_weekend)

    for i in range(0, len(Min_Product_Brought_weekend_only)):
         Min_ItemE = Min_Product_Brought_weekend_only.iloc[i, 0]

         for j in range(0, len(wndRND)):
            Main_ItemE = wndRND.iloc[j, 0]
            Main_qtyE = wndRND.iloc[j, 1]

            if(Main_ItemE == Min_ItemE):
                minItemE.append(Main_ItemE)
                minqtyE.append(Main_qtyE)

    Item_Bring_Min_List_weekend['Items'] = minItemE
    Item_Bring_Min_List_weekend['Qty'] = minqtyE

# print('Team 2 Score of best batsmen score is ',T2_batting_score)
# display(Item_Bring_Min_List_weekday)
# print('')

    y1 = Item_Bring_Max_List_weekend.append(Item_Bring_normal_List_weekend)
    WEEKEND_LIST = y1.append(Item_Bring_Min_List_weekend)
    WEEKEND_LIST = WEEKEND_LIST.sort_values(by='Qty', ascending=False)
    WEEKEND_LIST.reset_index(inplace=True, drop=True)
    WEEKEND_LIST.to_csv('WEEKEND_LIST.csv', encoding='utf-8')
   #-------------------------------------------------------------------------------------------------------------------
        #store and generate csv file and delete the previous one
        
    if(TWeekday == 'Thursday'):
        a = TWeekday 

        file = 'WEEKEND_LIST.csv'
        if(os.path.exists(file) and os.path.isfile(file)):
          os.remove(file)
          print("file deleted")
          WEEKEND_LIST.to_csv('WEEKEND_LIST.csv', encoding='utf-8')
        else:
          print("file not found")
          WEEKEND_LIST.to_csv('WEEKEND_LIST.csv', encoding='utf-8')

        
# -------------------------------------------------------------------------------------------------------------------------
#mail the csv file to the supplier 


        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        

# this is python 2 and 3 compatible

        #COMMASPACE = ', '

       # sender = 'vsonar321@gmail.com'
       # recipients = ['vsonar61@gmail.com', 'vishalsonar554@gmail.com']
       # subject = 'Weekend Product list'
       # body = """Hello sir/maam,
       # This CSV file contain the list of product thats should be brought on Friday Morning, Thank You"""

       # msg = MIMEMultipart()
       # msg['Subject'] = subject
      #  msg['From'] = sender
       # msg['To'] = COMMASPACE.join(recipients)
      #  msg.preamble = subject # for clients without multipart support

# attachment file(s)
      #  filename = "WEEKEND_LIST.csv"
      #  with open(filename, "r") as text_file:
      #   attachment = MIMEText(text_file.read())
       #  attachment.add_header('Content-Disposition', 'attachment', filename=filename)
       #  msg.attach(attachment)

#body
     #   msg.attach(MIMEText(body, 'plain'))


     #   s = smtplib.SMTP('smtp.gmail.com', 587)
     #   s.starttls()
     #   s.login("vsonar321@gmail.com", "hoovyyyleoerupgi")
     #   s.sendmail(sender, recipients, msg.as_string())
     #   s.quit()



    print('Weekend Brough item')
    json_records_WEEKDEND_LIST = WEEKEND_LIST.reset_index().to_json(orient='records')
    WEEKDEND_LIST = []
    WEEKDEND_LIST = json.loads(json_records_WEEKDEND_LIST)
# -------------------------------------------------------------------------------------------------------------------------

    context = {
        'TodayRevenue': todayttl,
        'YesterdayRevenue': yesterdayttl,
        'diff': diff,
        'indian_rupee': indian_rupee,
        'MSI': MSIarr,  # Most sale Item
        'MSC': catdata,  # Most sale Item
        'TC': Sop,
        'OT': OrTty,
        'Iqty': itemqty,
        'v1': last_Month,
        'data': wddata,
        'MoCatToday': NoP_MostSale,
        #'xy': leastsaleitem,
        'CatM':  mylistcatm,
        'Cat_CM': Cat_CM,
        'ItemM': mylistitemim,
        'Item_M': ItemM,
        'ItemSP': ItemSP,
        'ItemEP': ItemEP,
        'MonthAve': MonthAve,
        'WEEKDAY_LIST': WEEKDAY_LIST,
        'WEEKDEND_LIST': WEEKDEND_LIST,
       
    }

    # return render(request,'demo1/index.html',context)
    return render(request, 'demo1/index.html', context)
