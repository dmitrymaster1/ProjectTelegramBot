import sqlite3 as sql

base = sql.connect('expenses_base.db')
cur = base.cursor()

def sql_start():
    base.execute('CREATE TABLE IF NOT EXISTS {}(category, count, date)'.format('spendings'))
    base.commit()
