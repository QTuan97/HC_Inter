import re
from user_agents import parse

List = open("gistfile1.txt").readlines()

def convert_log_data(List):
    res = []
    total_browser = []
    for item in List:
        num = 5
        char = '"'
        pattern = f"({re.escape(char)})"
        parts = re.split(pattern, item, maxsplit=num)
        res.append(parts[-1])

    for browser in res:
        parsed_ua = parse(browser)
        total_browser.append(parsed_ua.browser.family)
    return total_browser

def check_browser_percentage(browser):
    result = {i:browser.count(i) for i in browser}
    print(result)

if __name__ == '__main__':
    check_browser_percentage(convert_log_data(List))