from io import StringIO
import requests
import pandas as pd
from database.database import States, CaseReport


def handler() -> dict:
    """
        Função responsável por salvar o csv com os dados diarios na base

    """
    data = requests.get('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv').content

    df = pd.read_csv(StringIO(data.decode('utf-8')), sep=',', encoding='utf-8')
    states_response = States.select().dicts().execute()
    states = {i.get('name'): i.get('id') for i in states_response}

    df['state_id'] = df['state'].apply(lambda x: states.get(x, 0))
    df['tests'] = df['tests'].fillna(0)
    df['newDeaths'] = df['newDeaths'].fillna(0)
    df['deaths'] = df['deaths'].fillna(0)
    df['totalCases'] = df['totalCases'].fillna(0)
    df['newCases'] = df['newCases'].fillna(0)
    df['recovered'] = df['recovered'].fillna(0)
    df['suspects'] = df['suspects'].fillna(0)
    df['tests_per_100k_inhabitants'] = df['tests_per_100k_inhabitants'].fillna(0)
    df = df.rename(columns={
        'date': 'date_report',
        'newDeaths': 'new_deaths',
        'deaths': 'total_deaths',
        'totalCases': 'total_cases',
        'newCases': 'new_cases',
        'deaths_per_100k_inhabitants': 'total_deaths_per_100k',
        'totalCases_per_100k_inhabitants': 'total_cases_per_100k',
        'tests_per_100k_inhabitants': 'tests_per_100k',
        'deaths_by_totalCases': 'deaths_by_cases',
    })
    df = df.drop(['state', 'country', 'city', 'deathsMS', 'totalCasesMS'], 1)
    df = df.dropna(subset=['state_id'])
    df = df.drop_duplicates(subset=['state_id', 'date_report'], keep='last')
    dataset = df.to_dict(orient="records")

    try:
        CaseReport.insert_many(dataset).on_conflict(conflict_target=[CaseReport.state_id, CaseReport.date_report],
                                                    preserve=[CaseReport.new_cases, CaseReport.new_deaths,
                                                              CaseReport.total_deaths, CaseReport.total_cases,
                                                              CaseReport.total_cases_per_100k,
                                                              CaseReport.total_deaths_per_100k,
                                                              CaseReport.tests_per_100k, CaseReport.tests,
                                                              CaseReport.suspects, CaseReport.recovered],
                                                    action="update").execute()
    except Exception as e:
        print(e)
        return {'status': 500}

    return {'status': 400}
