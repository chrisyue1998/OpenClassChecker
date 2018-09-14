from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.vendored import requests
from bs4 import BeautifulSoup

import sys
import os
import smtplib

username = str(os.environ['username'])
password = str(os.environ['password'])

def lambda_handler(event, context):
    for course in event.keys():
        course_id = course.split('_')[0]
        print(event)
        section_num = course.split('_')[1]
        
        url = 'https://app.testudo.umd.edu/soc/search?' \
                'courseId={}&' \
                'sectionId={}&' \
                'termId=201808&' \
                '_openSectionsOnly=on&' \
                'creditCompare=&' \
                'credits=&' \
                'courseLevelFilter=ALL&' \
                'instructor=&' \
                '_facetoface=on&' \
                '_blended=on&' \
                '_online=on&' \
                'courseStartCompare=&' \
                'courseStartHour=&' \
                'courseStartMin=&' \
                'courseStartAM=&' \
                'courseEndHour=&' \
                'courseEndMin=&' \
                'courseEndAM=&' \
                'teachingCenter=ALL&' \
                '_classDay1=on&' \
                '_classDay2=on&' \
                '_classDay3=on&' \
                '_classDay4=on&' \
                '_classDay5=on'.format(course_id, section_num)
    
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}
    
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        open_seats = soup.find(attrs={'class': 'open-seats-count'})
        open_seats = list(open_seats)
        open_seats = int(open_seats[0])
    
        if open_seats > 0:
            msg_txt = 'Subject: ' + course_id + ' (section ' + section_num + ') has a spot available!'
            msg = MIMEMultipart()
            msg['Subject'] = course + ' Waitlist'
            txt = MIMEText(msg_txt)
            msg.attach(txt)
    
            # setup the email server,
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
    
            # send the email
            server.sendmail(username, event[course], msg.as_string())
            # disconnect from the server
            server.quit()
