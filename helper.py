from lib2to3.pgen2.pgen import DFAState
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head(4)
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

#     def remove_stop_words(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglishMarathi.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def sentiment(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    overall = []
    posarr=[]
    negarr=[]
    neuarr=[]

    for message in temp['message']:        
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(message)

        negarr.append(sentiment_dict['neg']*100)
        neuarr.append(sentiment_dict['neu']*100)
        posarr.append(sentiment_dict['pos']*100)
    
        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05 :
            overall.append("Positive")
    
        elif sentiment_dict['compound'] <= - 0.05 :
            overall.append("Negative")
    
        else :
            overall.append("Neutral")

    dict = {'Message' : temp['message'],
        'Positive':posarr,
        'Negative':negarr,
        'Neutral':neuarr,
        'Overall' :overall
    }
    most_common_df = pd.DataFrame(dict)
    return most_common_df













