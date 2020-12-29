from database.database import CaseReport, States
from peewee import fn


def handler():
    """
        Tabela com dados por estado por estado

    """
    sub = CaseReport.select().order_by(CaseReport.date_report.desc()).limit(1)
    response = list(
        CaseReport.select(States.name, CaseReport.total_deaths_per_100k, CaseReport.total_cases_per_100k).join(sub, on=(
                sub.c.date_report == CaseReport.date_report)).join(
            States, on=(States.id == CaseReport.state_id)).order_by(CaseReport.date_report.asc()).dicts().execute())

    cases = [i['total_cases_per_100k'] for i in response]
    deaths = [i['total_deaths_per_100k'] for i in response]

    return {
        'categories': [i['name'] for i in response],
        'series': [
            {
                'name': 'Casos por 100 Mil habitantes',
                'data': cases,
                'type': 'column'
            },
            {
                'name': 'Mortes por 100 Mil habitantes',
                'data': deaths,
                'type': 'column'
            }
        ]
    }
