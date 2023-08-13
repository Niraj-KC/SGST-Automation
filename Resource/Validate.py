import datetime, os


def dateFormat(date: str, format: str):
    res = True
    try:
        res = bool(datetime.datetime.strptime(date, format))
    except ValueError:
        res = False
    return res

def dateRange(fromDate: str, toDate: str):
    fromDate = datetime.datetime.strptime(fromDate, '%d/%m/%Y').date()
    toDate = datetime.datetime.strptime(toDate, '%d/%m/%Y').date()
    diff = toDate - fromDate

    if diff < (datetime.datetime.today() - datetime.datetime.today()):
        return False
    else:
        return True

def path(path: str):
    return os.path.exists(path)

def tax(tax: float | int):
    return tax > 0
