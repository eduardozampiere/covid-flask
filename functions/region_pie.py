from database.database import CaseReport, States
from peewee import fn
from functools import reduce
def define_region(state: str) -> int:
    if state in ['RJ', 'SP', 'ES', 'MG']:
        return 0

    elif state in ['RS', 'SC', 'PR']:
        return 1

    elif state in ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC']:
        return 2

    elif state in ['MA', 'PI', 'CE', 'RN', 'PE', 'PB', 'SE', 'AL', 'BA']:
        return 3

    return 4


def handler(body):
    """
        Tabela com dados por estado por estado
        type -> case or death

    """
    _type = body.get('type', 'case')
    field = CaseReport.total_cases if _type == 'case' else CaseReport.total_deaths
    sub = CaseReport.select().order_by(CaseReport.date_report.desc()).limit(1)
    response = list(
        CaseReport.select(States.name, field.alias('total_data')).join(sub, on=(
                sub.c.date_report == CaseReport.date_report)).join(
            States, on=(States.id == CaseReport.state_id)).order_by(CaseReport.date_report.asc()).dicts().execute())
    names = ['Sudeste', 'Sul', 'Norte', 'Nordeste', 'Centro-Oeste']
    arr = [0, 0, 0, 0, 0]
    for i in response:
        region = define_region(i['name'])
        arr[region] +=  i['total_data']

    total = reduce(lambda a, b: a + b, arr)
    return {
        'dataseries': [{
            'name': name,
            'y': arr[i] / total,
            'value': arr[i]
        } for i, name in enumerate(names)]
    }
