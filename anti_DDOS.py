import re, ast
from urllib.parse import urlparse

Data = open("test.txt").readlines()

def get_url_list(data):
    res = []
    split_num = 5
    pattern = r'https?://\S+|www\.\S+'

    for line in data:
        log_list = line.split('"')
        res.append(' '.join(log_list[:split_num]))
    url_list = re.findall(pattern, str(res))

    return url_list

def get_ip_address_datetime(data):
    res = []
    split_num = 6

    for line in data:
        log_list = line.split(' ')
        res.append(' '.join(log_list[:split_num]))

    return res

def check_if_urls_is_not_blocked(data):
    ignored_list = ['google.com','.google.com','bing.com','.bing.com','facebook.com','.facebook.com']
    parsed_url = urlparse(data)
    netloc = parsed_url.netloc.lower()

    for check in ignored_list:
        if netloc == check or netloc.endswith(str(check)):
            return True
        else:
            return False

def check_spam_requests(data):
    pattern_IP = r'[0-9]+(?:\.[0-9]+){3}'
    pattern_datetime = r"\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4}"

    k = []
    v = []

    for spam_requests in get_ip_address_datetime(data):
        keys = re.findall(pattern_IP,str(spam_requests))
        values = re.findall(pattern_datetime,str(spam_requests))
        k.append(str(keys))
        v.append(str(values))

    test = dict(zip(k,v))

if __name__ == '__main__':
    check_spam_requests(Data)
