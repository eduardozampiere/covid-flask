from database.database import CaseReport, States
from peewee import fn


def handler():
    """
        Tabela com dados por estado por estado

    """
    sub = CaseReport.select().order_by(CaseReport.date_report.desc()).limit(1)
    response = list(
        CaseReport.select(States.name, CaseReport.total_cases, CaseReport.new_cases, CaseReport.total_deaths,
                          CaseReport.new_deaths, CaseReport.tests, CaseReport.tests_per_100k, CaseReport.suspects,
                          CaseReport.total_deaths_per_100k, CaseReport.total_cases_per_100k,
                          CaseReport.deaths_by_cases).join(sub, on=(sub.c.date_report == CaseReport.date_report)).join(
            States, on=(States.id == CaseReport.state_id)).order_by(CaseReport.date_report.asc()).dicts().execute())

    return {
        'data': response
    }
