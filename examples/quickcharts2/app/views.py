import random
import logging
import datetime
import calendar
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.views import ModelView
from flask_appbuilder.charts.views import DirectChartView, GroupByChartView
from models import CountryStats, Country, PoliticalType
from app import appbuilder, db
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg

log = logging.getLogger(__name__)

def fill_data():
    countries = ['Portugal', 'Germany', 'Spain', 'France', 'USA', 'China','Russia','Japan']
    politicals = ['Democratic', 'Authorative']
    for country in countries:
        c = Country(name=country)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback()
    for political in politicals:
        c = PoliticalType(name=political)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback()
    try:
        for x in range(1, 100):
            cs = CountryStats()
            cs.population = random.randint(1, 100)
            cs.unemployed = random.randint(1, 100)
            cs.college = random.randint(1, 100)
            year = random.choice(range(1900, 2012))
            month = random.choice(range(1, 12))
            day = random.choice(range(1, 28))
            cs.stat_date = datetime.datetime(year, month, day)
            cs.country_id = random.randint(1, len(countries))
            cs.political_type_id = random.randint(1, len(politicals))
            db.session.add(cs)
            db.session.commit()
    except Exception as e:
        log.error("Update ViewMenu error: {0}".format(str(e)))
        db.session.rollback()


class CountryStatsModelView(ModelView):
    datamodel = SQLAModel(CountryStats)
    list_columns = ['country', 'stat_date', 'population', 'unemployed', 'college']

class CountryModelView(ModelView):
    datamodel = SQLAModel(Country)


class PoliticalTypeModelView(ModelView):
    datamodel = SQLAModel(PoliticalType)


class CountryStatsDirectChart(DirectChartView):
    datamodel = SQLAModel(CountryStats)
    chart_title = 'Statistics'
    chart_type = 'LineChart'
    direct_columns = {'General Stats': ('stat_date', 'population', 'unemployed', 'college')}
    base_order = ('stat_date', 'asc')


def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)


class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAModel(CountryStats)
    chart_title = 'Statistics'
    chart_type = 'ColumnChart'
    #label_columns = {'month_year': 'Month Year', 'country_political': 'Country Political'}
    group_by_columns = ['country', 'political_type', 'country_political', 'month_year']
    # ['<COL NAME>']
    aggregate_by_column = [(aggregate_avg, 'unemployed'), (aggregate_avg, 'population'), (aggregate_avg, 'college')]
    # [{'aggr_func':<FUNC>,'column':'<COL NAME>'}]
    formatter_by_columns = {'month_year': pretty_month_year}



db.create_all()
#fill_data()
appbuilder.add_view(CountryModelView, "List Countries", icon="fa-folder-open-o", category="Statistics")
appbuilder.add_view(PoliticalTypeModelView, "List Political Types", icon="fa-folder-open-o", category="Statistics")
appbuilder.add_view(CountryStatsModelView, "List Country Stats", icon="fa-folder-open-o", category="Statistics")
appbuilder.add_separator("Statistics")
appbuilder.add_view(CountryStatsDirectChart, "Show Country Chart", icon="fa-dashboard", category="Statistics")
appbuilder.add_view(CountryGroupByChartView, "Group Country Chart", icon="fa-dashboard", category="Statistics")

