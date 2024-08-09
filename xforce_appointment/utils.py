from datetime import datetime


def format_time_obj(date_obj):
    date_str = datetime.strftime(date_obj, "%m/%d/%y %H:%M")
    return date_str


def parse_str_to_tome_obj(date_str):
    date_obj = datetime.strptime(date_str, "%m/%d/%y %H:%M")
    return date_obj



