import re
from user_agents import parse

List = open("gistfile1.txt").readlines()

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

def check_browser_percentage(browser):
    result = {i:round(total_browser.count(i)/len(res)*100,2) for i in total_browser}
    print(result)

if __name__ == '__main__':
    check_browser_percentage(res)