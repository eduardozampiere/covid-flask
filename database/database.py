import peewee

database = peewee.PostgresqlDatabase('coviddb',
                                     **{'host': 'localhost', 'port': 5432,
                                        'user': 'postgres', 'password': '123456'},
                                     autorollback=True)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class States(BaseModel):
    id = peewee.IntegerField()
    name = peewee.CharField()

    class Meta:
        table_name = 'states'
        schema = 'public'
        # primary_key = peewee.CompositeKey('id', 'name')


class CaseReport(BaseModel):
    state_id = peewee.ForeignKeyField(model=States)
    epi_week = peewee.IntegerField()
    date_report = peewee.DateField()
    new_deaths = peewee.IntegerField()
    total_deaths = peewee.IntegerField()
    new_cases = peewee.IntegerField()
    total_cases = peewee.IntegerField()
    recovered = peewee.IntegerField()
    suspects = peewee.IntegerField()
    tests = peewee.IntegerField()
    deaths_by_cases = peewee.DoubleField()
    total_deaths_per_100k = peewee.DoubleField()
    total_cases_per_100k = peewee.DoubleField()
    tests_per_100k = peewee.DoubleField()

    class Meta:
        table_name = 'case_reports'
        schema = 'public'
        primary_key = peewee.CompositeKey('state_id', 'date_report')
