from datetime import datetime
from database.database import CaseReport
from helpers.date import tomorrow


def handler(body) -> dict:
    """
        Serie temporal de Letalidade
        days -> dias da simulacao
        state -> id do estado or 0 para total

    """
    days = body.get('days', 15)
    state = body.get('state', 0)

    response = CaseReport.select(CaseReport.date_report, CaseReport.total_cases, CaseReport.total_deaths).where(
        CaseReport.state_id == state).order_by(CaseReport.date_report.asc()).dicts().execute()

    total_deaths = response[-1].get('total_deaths', 0)
    total_cases = response[-1].get('total_cases', 0)
    last_day = response[-1].get('date_report', 0)

    days_to_double_cases = 0
    days_to_double_deaths = 0
    for d, i in enumerate(response[::-1]):
        if total_cases >= 2 * i['total_cases']:
            days_to_double_cases = d
            break

    for d, i in enumerate(response[::-1]):
        if total_deaths >= 2 * i['total_deaths']:
            days_to_double_deaths = d
            break

    cases = []
    deaths = []
    date = tomorrow(last_day)

    for i in range(1, days + 1):
        date_time = datetime.timestamp(datetime.strptime(date, '%Y-%m-%d'))
        future_total_cases = total_cases * (2 ** (i / days_to_double_cases))
        future_total_deaths = total_deaths * (2 ** (i / days_to_double_deaths))
        cases.append([date_time, future_total_cases])
        deaths.append([date_time, future_total_deaths])
        date = tomorrow(date)

    return {
        'dataSeries': [
            {
                'id': 0,
                'name': 'Casos',
                'data': cases,
                'type': 'spline'
            },

            {
                'id': 1,
                'name': 'Mortes',
                'data': deaths,
                'type': 'spline'
            },
        ]
    }
