# ====================================================================================================
# Python script to define SQL scripts of each scenario
# ----------------------------------------------------------------------------------------------------
# Test

sql_test_1 = '''
SELECT strftime('%Y-%m', OrderDate) AS order_month, COUNT(1) AS cnt_order
FROM Orders
GROUP BY 1
ORDER BY 1
'''

sql_test_2 = '''
SELECT COUNT(1) AS cnt
FROM ProductSalesAmountByMonth
WHERE yearMonth = '1996-11'
'''



# ----------------------------------------------------------------------------------------------------
# Real

sql_scenario_1_delete = '''
DELETE FROM ProductSalesAmountByMonth
WHERE yearMonth = '{sql_param_1}'
;
'''

sql_scenario_1_insert = '''
INSERT INTO ProductSalesAmountByMonth

WITH q_sales AS (
	SELECT
		strftime('%Y-%m', t1.OrderDate) AS yearMonth
		, t0.ProductID
		, MAX(t2.ProductName) AS ProductName
		, SUM((t0.UnitPrice * t0.Quantity) - t0.Discount) AS salesAmount
	FROM "Order Details" AS t0
	LEFT JOIN "Orders" AS t1
		ON t0.OrderID = t1.OrderID
	LEFT JOIN "Products" AS t2
		ON t0.ProductID = t2.ProductID
	WHERE strftime('%Y-%m', t1.OrderDate)
		BETWEEN '{sql_param_2}'
			AND '{sql_param_1}'
	GROUP BY 1,2
	ORDER BY 1,2
)

SELECT q1.*
	, ((q1.salesAmount / q2.salesAmount) - 1) * 100 AS percentage_change
FROM q_sales AS q1 -- Current Month [t]
LEFT JOIN q_sales AS q2 -- Previous Month [t-1]
	ON q1.ProductID = q2.ProductID
	AND q2.yearMonth = '{sql_param_2}'
WHERE q1.yearMonth = '{sql_param_1}'
;
'''

sql_scenario_1_result = '''
SELECT yearMonth, COUNT(1) AS cnt_record
FROM ProductSalesAmountByMonth
WHERE yearMonth = '{sql_param_1}'
GROUP BY 1
'''


