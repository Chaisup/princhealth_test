# ====================================================================================================
# Python script to run the following actions
# 1) Assume that today is 1997-01-01. So, the current quarter of data is 1996Oct-Dec.
# 2) Pull data from "ProductSalesAmountByMonth" and write Excel file.
# ----------------------------------------------------------------------------------------------------
# Import

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import sqlite3

import var_path
import var_sql_code


# ----------------------------------------------------------------------------------------------------
# Declare

# today = datetime.date.today()
today = datetime.date(1997, 1, 1)

period_m1 = datetime.date.strftime((today-relativedelta(months=1)), '%b')
period_m2 = datetime.date.strftime((today-relativedelta(months=2)), '%b')
period_m3 = datetime.date.strftime((today-relativedelta(months=3)), '%b')
period_y  = datetime.date.strftime((today-relativedelta(months=3)), '%Y')

sql_kwargs = {
	'sql_param_1': datetime.date.strftime((today-relativedelta(months=1)), '%Y-%m'),
	'sql_param_2': datetime.date.strftime((today-relativedelta(months=2)), '%Y-%m'),
	'sql_param_3': datetime.date.strftime((today-relativedelta(months=3)), '%Y-%m')
}
print('sql_kwargs:', sql_kwargs)

xl_filename = var_path.path_folder_2_xlsx.replace('.xlsx', f'{period_y}{period_m3}-{period_m1}.xlsx')


# ----------------------------------------------------------------------------------------------------
# Run

def execute_with_result(sql_code, sql_desc):
	print('Executing SQL:', sql_desc)
	sql_code = sql_code.format(**sql_kwargs)
	con = sqlite3.connect(var_path.path_db)
	cur = con.cursor()
	res = cur.execute(sql_code)
	con.commit()
	print('Executed')
	sql_records = res.fetchall()
	if sql_records:
		df = pd.DataFrame(sql_records)
		df.columns = list(map(lambda x: x[0], res.description))
		print('Result:', df.shape)
		return df
	else:
		return None

print('Preparing DF')
df_data = execute_with_result(var_sql_code.sql_scenario_2_result, 'scenario_2_result')
df_data_m1 = df_data[df_data['yearMonth']==sql_kwargs['sql_param_1']]
df_data_m2 = df_data[df_data['yearMonth']==sql_kwargs['sql_param_2']]
df_data_m3 = df_data[df_data['yearMonth']==sql_kwargs['sql_param_3']]

print('Writing Excel')
xl_writer = pd.ExcelWriter(xl_filename, engine='xlsxwriter')
df_data_m3.to_excel(xl_writer, index=False, sheet_name=period_m3)
df_data_m2.to_excel(xl_writer, index=False, sheet_name=period_m2)
df_data_m1.to_excel(xl_writer, index=False, sheet_name=period_m1)
xl_writer.close()

print('Completed')

