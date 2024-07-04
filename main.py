from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def get_year():
    now = datetime.datetime.now()
    number = now.year - 1920

    if number % 10 == 1 and number % 100 != 11:
        return str(number) + " год"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return str(number) + " года"
    else:
        return str(number) + " лет"


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    excel_data_wines = pandas.read_excel(
        'wine3.xlsx',
        keep_default_na=False,
        na_values=['N/A', 'NA']
    ).to_dict(orient='records')

    group_wines = collections.defaultdict(list)

    for wine in excel_data_wines:
        group_wines[wine["Категория"]].append(wine)


    template = env.get_template('template.html')

    rendered_page = template.render(
        date_company = get_year(),
        group_wines = group_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()