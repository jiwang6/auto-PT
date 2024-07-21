import requests
from bs4 import BeautifulSoup
import re
import datetime

def get_questions(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    content = soup.body.find_all(text = re.compile('var FB'))
    
    match = re.findall('[,]["][\w\s]+["][,]', str(content))

    question_strings = [x.strip('"') for x in match]
    
    match_ids = re.findall('(?<=\[\[)(\d+)', str(content))

    question_ids = ['entry.' + x for x in match_ids[1:]]

    return question_ids
    


def send_answers(url, name_string = '1st Lt, Wang, Jim', exercise_string = 'hacking', month = None, day = None, year = None):
    ids = [
        'entry.10432257', # name
        'entry.353385772_month',
        'entry.353385772_day',
        'entry.353385772_year',
        'entry.1518571388' # exercise
    ]

    answers = [name_string, month, day, year, exercise_string]
    
    response = dict(zip(ids, answers))
    
    if 'viewform' in url:
        s = url.index('viewform') 
        response_url = url.replace(url[s::], 'formResponse?')
        
    try:
        r = requests.post(response_url, response)
        if r.status_code == 200:
            return '[!] PT posted !'
        #In case an error happens, it will raise an exception
        else:
            raise Exception

    #After raising the exception it will retry to submit using url reconstruction with prefilled values
    except:
        try:
            ans_list = [x + '=' + y for x, y in zip(ids, answers)]
            
            for i in range(0, len(ans_list)):
                response_url += ans_list[i]
                response_url += '&'
                
            response_url.strip("&")    
            r = requests.get(response_url)
            status = r.status_code
            
            if status == 200:
                return '[!] Form sent !'
            else:
                raise Exception
        #If still an error happens, it will print out a message.
        except:
            return '[!] Form not sent !'
                

url = 'https://docs.google.com/forms/d/e/1FAIpQLSf-QN3P25woSyV2FixVXHsxgSczqStO5I5979IzgwbHVpBAqA/viewform'
ranklastfirst = "1st Lt, Wang, Jim"
exercise = "lifting"


#print(send_answers(url, ranklastfirst, exercise))

for i in range (2):
    if i == 0:
        year, month, day = map(int, str(datetime.datetime.now()).split(' ')[0].split('-'))
    else:
        # get tomorrow's date
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        year, month, day = map(int, str(tomorrow).split(' ')[0].split('-'))

    print(send_answers(url, ranklastfirst, exercise, month, day, year))