from time import mktime
from database.database import CaseReport
from peewee import fn
from helpers.date import get_period


def handler(body) -> dict:
    """
        Serie temporal de testes

        type -> 'day' or 'week'
        period -> None, 'ytd', 'mtd' ...
        init_date -> data inicial or None
        end_date -> data final or None
        state -> id do estado or 0 para total

    """
    type = body.get('type', 'day')
    period = body.get('period', None)
    init_date = body.get('init_date', None)
    end_date = body.get('end_date', None)
    state = body.get('state', 0)
    where = []
    if period:
        init_date, end_date = get_period(period)

    if init_date and end_date:
        where = [CaseReport.date_report >= init_date, CaseReport.date_report <= end_date]

    if type == 'day':
        response = CaseReport.select(CaseReport.date_report, CaseReport.tests).where(
            CaseReport.state_id == state, *where).order_by(CaseReport.date_report.asc()).dicts().execute()
    else:
        response = CaseReport.select(fn.MAX(CaseReport.date_report).alias('date_report'),
                                     fn.SUM(CaseReport.tests).alias('tests')).where(
            CaseReport.state_id == state, *where).order_by(fn.MAX(CaseReport.date_report).asc()).group_by(
            CaseReport.epi_week).dicts().execute()
    tests = [[mktime(i.get('date_report').timetuple()), i.get('tests')] for i in response]

    return {
        'dataSeries': [
            {
                'id': 0,
                'name': 'Total de Testes',
                'data': tests,
                'type': 'spline'
            },
        ]
    }
