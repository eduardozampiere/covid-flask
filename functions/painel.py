from database.database import CaseReport


def handler(body):
    """
        Painel com informações básicas

    """
    state = body.get('state', 0)

    response = list(
        CaseReport.select(CaseReport.date_report, CaseReport.total_cases, CaseReport.total_deaths, CaseReport.new_cases,
                          CaseReport.new_deaths).where(CaseReport.state_id == state).order_by(
            CaseReport.date_report.asc()).dicts().execute())

    first_case_day = response[0].get('date_report', None)
    last_date = response[-1].get('date_report', None)
    total_cases = response[-1].get('total_cases', 0)
    total_deaths = response[-1].get('total_deaths', 0)
    new_cases = response[-1].get('new_deaths', 0)
    new_deaths = response[-1].get('new_deaths', 0)
    lethality = total_deaths / total_cases if total_cases != 0 else None
    first_death_day = next((i for i in response if i.get('total_deaths')), None).get('date_report')
    days_to_double = 0
    for d, i in enumerate(response[::-1]):
        if total_cases >= 2 * i['total_cases']:
            days_to_double = d
            break

    return {
        'first_case_day': first_case_day,
        'first_death_day': first_death_day,
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'new_cases': new_cases,
        'new_deaths': new_deaths,
        'lethality': lethality,
        'days_to_double': days_to_double,
        'last_date': last_date
    }
