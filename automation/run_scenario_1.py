# ====================================================================================================
# Python script to run the following actions
# 1) Assume that today is 1997-01-01. So, the current month of data is 1996-12.
# 2) Update data in the table "ProductSalesAmountByMonth".
# ----------------------------------------------------------------------------------------------------
# Import

import datetime
import dateutil.relativedelta
import pandas as pd
import sqlite3

import var_path
import var_sql_code


# ----------------------------------------------------------------------------------------------------
# Declare

# today = datetime.date.today()
today = datetime.date(1997, 1, 1)


# ----------------------------------------------------------------------------------------------------
# Run

print('Getting Variables')
path_db = var_path.path_db
sql_kwargs = {
	'sql_param_1': datetime.date.strftime((today-dateutil.relativedelta.relativedelta(months=1)), '%Y-%m'),
	'sql_param_2': datetime.date.strftime((today-dateutil.relativedelta.relativedelta(months=2)), '%Y-%m')
}
print('sql_kwargs:', sql_kwargs)

def execute(sql_code, sql_desc):
	print('Executing SQL:', sql_desc)
	sql_code = sql_code.format(**sql_kwargs)
	con = sqlite3.connect(path_db)
	cur = con.cursor()
	res = cur.execute(sql_code)
	con.commit()
	print('Executed')
	sql_records = res.fetchall()
	if sql_records:
		df = pd.DataFrame(sql_records)
		df.columns = list(map(lambda x: x[0], res.description))
		print('Result:')
		print(df)

execute(var_sql_code.sql_scenario_1_delete, 'scenario_1_delete')
execute(var_sql_code.sql_scenario_1_insert, 'scenario_1_insert')
execute(var_sql_code.sql_scenario_1_result, 'scenario_1_result')

print('Completed')

