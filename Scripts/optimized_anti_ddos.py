import re , socket
from datetime import datetime, timedelta

INPUT_LOG = 'access.log'
CLEANED_LOG = 'access_cleaned.txt'
CLEANED_BOT_LOG = 'access_without_bot.txt'
SPAM_IP_LOG = 'spam_IP_list.txt'
BLOCKED_IP_LOG = 'blocked_IP_list.txt'


def clear_blocked_list(input_log, output_log):
    date_format = "%Y-%m-%d %H:%M:%S"
    cutoff = datetime.now() - timedelta(days=7)

    with open(input_log, "r") as infile, open(output_log, "w") as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            timestamp_str = f"{parts[1]} {parts[2]}"

            try:
                log_time = datetime.strptime(timestamp_str, date_format)
                if log_time >= cutoff:
                    outfile.write(line)
            except ValueError:
                continue

def clean_log_file(input_log, output_log):
    blocked_keywords = ['google', 'bing', 'facebook']
    pattern = re.compile('|'.join(blocked_keywords), re.IGNORECASE)

    with open(input_log, 'r') as infile, open(output_log, 'w') as outfile:
        for line in infile:
            if not pattern.search(line):
                outfile.write(line)

def filter_fake_bots_from_log(input_log, output_log, overwrite=False):
    crawlers = {
        'Googlebot': '.googlebot.com',
        'Bingbot': '.search.msn.com',
        'facebookexternalhit': '.facebook.com'
    }

    log_pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})(.*?)"(.*?)"$')
    cleaned_lines = []

    with open(input_log, 'r') as log:
        for line in log:
            match = log_pattern.search(line)
            if not match:
                cleaned_lines.append(line)
                continue

            ip, _, user_agent = match.groups()
            is_fake = False

            for bot, domain in crawlers.items():
                if bot.lower() in user_agent.lower():
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                        if not hostname.endswith(domain) or ip not in socket.gethostbyname_ex(hostname)[2]:
                            is_fake = True
                            break
                    except Exception:
                        is_fake = True
                        break

            if not is_fake:
                cleaned_lines.append(line)

    output_path = input_log if overwrite else output_log
    with open(output_path, 'w') as out:
        out.writelines(cleaned_lines)


def get_ip_datetime_pairs(lines):
    results = []
    for line in lines:
        parts = line.split(' ')
        ip_time = ' '.join(parts[:6]).replace('[', '').replace(']', '')
        results.append(ip_time)
    return results


def check_spam_requests(lines):
    datetime_pattern = r"\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}"
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'
    target_limit = 120
    time_format = "%d/%b/%Y:%H:%M:%S"

    ip_datetime = get_ip_datetime_pairs(lines)
    ip_list = [re.search(ip_pattern, entry).group(0) for entry in ip_datetime if re.search(ip_pattern, entry)]
    ip_counts = {ip: ip_list.count(ip) for ip in set(ip_list)}

    timestamps = [re.search(datetime_pattern, entry).group(0) for entry in ip_datetime if re.search(datetime_pattern, entry)]
    if not timestamps:
        return

    base_time = datetime.strptime(timestamps[0], time_format) + timedelta(minutes=1)
    offenders = {}

    for i, time_str in enumerate(timestamps):
        if datetime.strptime(time_str, time_format) >= base_time:
            for ip, count in ip_counts.items():
                if count > target_limit and ip not in offenders:
                    offenders[ip] = datetime.now().replace(microsecond=0).isoformat(' ')

    with open("spam_IP_list.txt", "w") as f:
        for ip, ts in offenders.items():
            f.write(f"{ip} {ts}\n")


if __name__ == '__main__':
    filter_fake_bots_from_log(INPUT_LOG, CLEANED_BOT_LOG)
    clean_log_file(CLEANED_BOT_LOG, CLEANED_LOG)

    with open("access_cleaned.txt") as f:
        data = f.readlines()

    check_spam_requests(data)

    with open("spam_IP_list.txt") as f:
        current_blocked_IP = f.readlines()

    clear_blocked_list(SPAM_IP_LOG, BLOCKED_IP_LOG)
