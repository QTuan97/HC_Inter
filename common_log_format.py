import sys

def get_input():
    split_num = 3
    for line in sys.stdin:
        log_list = line.split('"')
        common_log_format_list = ' '.join(log_list[:split_num])
        print(common_log_format_list)


if __name__ == '__main__':
    get_input()

