import re , socket
from datetime import timedelta,datetime

INPUT_LOG = 'access.log'
CLEANED_BOT_LOG =  'access_without_bot.txt'
CLEANED_LOG = 'access_cleaned.txt'
current_blocked_IP = open("demofile.txt").readlines()
Data = open("access_cleaned.txt").readlines()

def clear_blocked_list(input_log):
    new_blocked_list = []
    pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

    for line in input_log:
        new_line = line.split("\n").pop(0)
        new_blocked_list.append(new_line)

    for old_data in new_blocked_list:
        find_registed_time = re.findall(pattern, str(old_data))
        check_datetime = datetime.strptime(find_registed_time[0], '%Y-%m-%d %H:%M:%S')
        if check_datetime + timedelta(days=7) <= datetime.now().replace(microsecond=0):
            new_blocked_list.remove(old_data)

    with open("blocked_IP_list.txt", 'w') as f:
        f.writelines(entry if entry.endswith('\n') else entry + '\n' for entry in new_blocked_list)


def clean_log_file(input_log, output_log):
    BLOCKED_KEYWORDS = ['google', 'bing', 'facebook']
    pattern = re.compile('|'.join(BLOCKED_KEYWORDS), re.IGNORECASE)
    removed_count = 0
    with open(input_log, 'r') as infile, open(output_log, 'w') as outfile:
        for line in infile:
            if pattern.search(line):
                removed_count += 1
                continue
            outfile.write(line)

def filter_fake_bots_from_log(input_log,output_log,
    overwrite=False
):
    CRAWLERS = {
        'Googlebot': '.googlebot.com',
        'Bingbot': '.search.msn.com',
        'facebookexternalhit': '.facebook.com'
    }

    log_pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})(.*)"(.*?)"$')
    cleaned_lines = []

    with open(input_log, 'r') as log:
        for line in log:
            match = log_pattern.search(line)
            if not match:
                cleaned_lines.append(line)
                continue

            ip, middle, ua = match.groups()
            is_fake = False

            for bot, domain in CRAWLERS.items():
                if bot.lower() in ua.lower():
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                        if not hostname.endswith(domain):
                            is_fake = True
                            break
                        resolved_ips = socket.gethostbyname_ex(hostname)[2]
                        if ip not in resolved_ips:
                            is_fake = True
                            break
                    except:
                        is_fake = True
                        break

            if not is_fake:
                cleaned_lines.append(line)

    output_path = input_log if overwrite else output_log
    with open(output_path, 'w') as out:
        out.writelines(cleaned_lines)

def get_ip_address_datetime(data):
    res = []
    split_num = 6

    for line in data:
        log_list = line.split(' ')
        cleaning_list = ' '.join(log_list[:split_num]).replace("[","")
        final_res = cleaning_list.replace("]","")
        res.append(final_res)

    return res

def check_spam_requests(data):
    pattern_datetime = r"\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}"
    pattern_IP = r'[0-9]+(?:\.[0-9]+){3}'
    target_value = 5
    format_date = "%d/%b/%Y:%H:%M:%S"
    count_list = []
    v = []
    test = {}

    for counting in get_ip_address_datetime(data):
        keys = re.findall(pattern_IP, str(counting))
        count_list.append(keys[0])

    counted = {i: count_list.count(i) for i in count_list}

    for spam_requests in get_ip_address_datetime(data):
        values = re.findall(pattern_datetime,str(spam_requests))
        v.append(values)

    fixed_time = datetime.strptime(v[0][0], format_date) + timedelta(minutes=1)

    for time in v:
        if datetime.strptime(time[0], format_date) >= fixed_time:
            for key, val in counted.items():
                if val > target_value:
                    if not key in test.keys():
                        test[key] = str(datetime.now().replace(microsecond=0))

    with open("demofile.txt", "w") as f:
        string_key_dict = {str(key): value for key, value in test.items()}
        for k in string_key_dict:
            f.write(k + " " + string_key_dict.get(k) + "\n")

if __name__ == '__main__':
    filter_fake_bots_from_log(INPUT_LOG,CLEANED_BOT_LOG)
    clean_log_file(CLEANED_BOT_LOG,CLEANED_LOG)
    clear_blocked_list(current_blocked_IP)
    check_spam_requests(Data)
