from datetime import datetime


def percentage(curr, total):
    if not (isinstance(curr, (int, float)) and isinstance(total, (int, float))):
        raise ValueError("Both curr and total should be numerical values")
    if total == 0:
        raise ValueError("Total can not be zero")
    num = curr / total
    return f"{num:.2%}"


def get_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_folder_time():
    now = datetime.now()
    return now.strftime("%d%m%Y%H%M%S")
