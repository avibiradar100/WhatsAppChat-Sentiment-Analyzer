import re
import pandas as pd

def preprocess(filename):
    def date_time(s):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        result = re.match(pattern, s)
        if result:
            return True
        else:
            pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
            result = re.match(pattern, s)
            if result:
                return True
            else:
                return False
                
    def getDatapoint(line):
        splitline = line.split(' - ')
        dateTime = splitline[0]
        date, time = dateTime.split(", ")
        message = " ".join(splitline[1:])
        splitmessage = message.split(": ")
        if splitmessage[1:]:
            author = splitmessage[0]
            message = " ".join(splitmessage[1:])
        else:
            author = 'group_notification'
            message = splitmessage[0]
        return date, time, author, message
    data = []
    fp=open('C:\Users\Teknath\Desktop\ML projects\whatsapp chat analysis\WhatsApp Chat with Exam time.txt','r',encoding='utf-8');
    fp.readline()
    messageBuffer = []
    date, time, user = None, None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if date_time(line):
            if len(messageBuffer) > 0:
                data.append([date, time, user, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, user, message = getDatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)
    df = pd.DataFrame(data, columns=["date", 'time', 'user', 'message'])
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'])
    df.head()

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute

    return df