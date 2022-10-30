import sqlite3
import numpy as np
import csv

connection = sqlite3.connect(':memory:')

table = """CREATE TABLE IF NOT EXISTS BusinessStats(
                          area_id                            INTEGER PRIMARY KEY,
                          num_businesses                     INTEGER,
                          retail_trade                       INTEGER,
                          accommodation_and_food_services    INTEGER,
                          health_care_and_social_assistance  INTEGER,
                          education_and_training             INTEGER,
                          arts_and_recreation_services       INTEGER
                   )"""
cursor = connection.cursor()
cursor.execute(table)
connection.commit()

data_BusinessStats = list(csv.DictReader(open('BusinessStats.csv')))

DEFAULT_VALUE = np.nan

def clean(data, column_key, convert_function, default_value):
    special_values= {}
    for row in data:
        old_value = row[column_key]
        new_value = default_value
        try:
            if old_value in special_values.keys():
                new_value = special_values[old_value]
            else:
                new_value = convert_function(old_value)
        except (ValueError, TypeError):
            print('Replacing {} with {} in column {}'.format(row[column_key], new_value, column_key))
        row[column_key] = new_value

clean(data_BusinessStats, "area_id", int, DEFAULT_VALUE)
clean(data_BusinessStats, "num_businesses", int, "0")
clean(data_BusinessStats, "retail_trade", int, "0")
clean(data_BusinessStats, "accommodation_and_food_services", int, "0")
clean(data_BusinessStats, "health_care_and_social_assistance", int, "0")
clean(data_BusinessStats, "education_and_training", int, "0")
clean(data_BusinessStats, "arts_and_recreation_services", int, "0")


for row in data_BusinessStats:
    query = "INSERT INTO BusinessStats(area_id, num_businesses, retail_trade, accommodation_and_food_services, health_care_and_social_assistance, education_and_training, arts_and_recreation_services) "
    "VALUES (%(area_id)s, %(num_businesses)s, %(retail_trade)s, %(accommodation_and_food_services)s, %(health_care_and_social_assistance)s, %(education_and_training)s, %(arts_and_recreation_services)s)"
    # the execute() method accepts a query and optionally a tuple with values 
    # corresponding to the question marks in VALUES
    cursor.execute(query, row)
    connection.commit()

query = 'SELECT * from files LIMIT(10)'
for i in cursor.execute(query):
    print(i)