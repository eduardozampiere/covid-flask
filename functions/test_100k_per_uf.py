from database.database import CaseReport, States
from peewee import fn


def handler():
    """
        Tabela com dados por estado por estado

    """
    sub = CaseReport.select().order_by(CaseReport.date_report.desc()).limit(1)
    response = list(
        CaseReport.select(States.name, CaseReport.tests_per_100k).join(sub, on=(
                sub.c.date_report == CaseReport.date_report)).join(
            States, on=(States.id == CaseReport.state_id)).order_by(CaseReport.date_report.asc()).dicts().execute())

    tests = [i['tests_per_100k'] for i in response]

    return {
        'categories': [i['name'] for i in response],
        'series': [
            {
                'name': 'Testes por 100 Mil habitantes',
                'data': tests,
                'type': 'column'
            }
        ]
    }
