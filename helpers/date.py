import numpy as np


def tomorrow(date: str) -> str:
    return str(np.datetime64(date, 'D') + np.timedelta64(1, 'D'))[:10]


def get_period(period: str, end_date: str = None) -> (str, str):
    if not end_date:
        end_date = str(np.datetime64('today', 'D'))[:10]

    if period == 'mtd':
        init_date = f'{str(np.datetime64(end_date, "M"))}-01'

    elif period == 'ytd':
        init_date = f'{str(np.datetime64(end_date, "Y"))}-01-01'

    else:
        try:
            months = int(period[:-1])
            init_date = str(np.datetime64(end_date, 'D') - np.timedelta64(int(months / 12 * 365)))[:10]
        except Exception as e:
            print(e)
            return end_date, end_date

    return init_date, end_date
