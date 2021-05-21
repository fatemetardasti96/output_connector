import datetime

def hour_iterator(start_year, start_month, start_day, start_hour, start_min, end_year, end_month, end_day, end_hour, end_min):
    time_dic = {}
    start_time = datetime.datetime(start_year, start_month, start_day, start_hour, start_min)
    end_time = datetime.datetime(end_year, end_month, end_day, end_hour, end_min)
    
    i = 0
    while (start_time < end_time):
        time_dic[start_time.strftime("%Y-%-m-%-d_%-H:%-M")] = i
        minutes_added = datetime.timedelta(minutes= 60)
        start_time = start_time + minutes_added
        i +=1
    
    return time_dic


