import urllib.request, csv 
import datetime

URL_CONFIRMED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
URL_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def parse_csv(url):
    csv_file = download_csv(url)

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    colnames = []
    rows = []

    countries = {}

    for row in csv_reader:
        if line_count == 0:
            colnames = row
        elif len(row) > 0:
            country_name = row[1]
            if country_name not in countries:
                countries[country_name] = parse_int_row(row[4:])
            else:
                countries[country_name] = add_rows(countries[country_name], parse_int_row(row[4:]))
            rows.append(row)
        line_count += 1

    dates = colnames[4:]

    return dates, countries

def parse_int_row(row):
    parsed = []
    for figure in row:
        if len(figure) > 0:
            parsed.append(int(figure))
        else:
            parsed.append(0)
    return parsed

def add_rows(row1, row2):
    if len(row1) != len(row2):
        print('Rows do not have the same length.')
        return None
    else:
        return [figure + row2[i] for i, figure in enumerate(row1)]

def download_csv(url):
    with urllib.request.urlopen(url) as req:
        csv_file = req.read().decode().split('\n')
    return csv_file

def get_data_by_type(type):
    if type == 'deaths':
        dates_d, deaths = parse_csv(URL_DEATHS)
        return deaths
    if type == 'confirmed':
        dates_c, confirmed = parse_csv(URL_CONFIRMED)
        return confirmed
    else:
        print('no data found with type ', type)
        return None

def get_dates_by_type(type):
    if type == 'deaths':
        dates_d, deaths = parse_csv(URL_DEATHS)
        dates_deaths = [datetime.datetime.strptime(date, "%m/%d/%y") for date in dates_d]
        return [date.strftime('%d.%m.') for date in dates_deaths]
    if type == 'confirmed':
        dates_c, confirmed = parse_csv(URL_CONFIRMED)
        dates_confirmed = [datetime.datetime.strptime(date, "%m/%d/%y") for date in dates_c]
        return [date.strftime('%d.%m.') for date in dates_confirmed]
    else:
        print('no data found with type ', type)
        return None

def today(data_type, country=None, offset=-1):
    data = get_data_by_type(data_type)  
    if country:
        return data[country][offset]
    else:
        return sum([country[offset] for country in data.values()])    

def increase_daily(data_type, country=None):
    t = today(data_type, country)
    yesterday = today(data_type, country, -2)
    if yesterday == 0: return '~'
    return round( (t * 100 / yesterday) - 100 )

def countries():
    dates_d, deaths = parse_csv(URL_DEATHS)
    return deaths.keys()
