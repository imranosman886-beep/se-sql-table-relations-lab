import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

# STEP 1
df_boston = pd.read_sql_query("""
    SELECT
        e.firstName,
        e.lastName
    FROM employees AS e
    JOIN offices AS o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 2
df_zero_emp = pd.read_sql_query("""
    SELECT o.officeCode
    FROM offices AS o
    LEFT JOIN employees AS e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
df_employee = pd.read_sql_query("""
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees AS e
    LEFT JOIN offices AS o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
df_contacts = pd.read_sql_query("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers AS c
    LEFT JOIN orders AS ord
        ON c.customerNumber = ord.customerNumber
    WHERE ord.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
df_payment = pd.read_sql_query("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        CAST(p.amount AS REAL) AS amount,
        p.paymentDate
    FROM payments AS p
    JOIN customers AS c
        ON p.customerNumber = c.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
df_credit = pd.read_sql_query("""
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS n_customers
    FROM employees AS e
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        e.employeeNumber,
        e.firstName,
        e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY n_customers DESC
    LIMIT 4
""", conn)

# STEP 7
df_product_sold = pd.read_sql_query("""
    SELECT
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
df_total_customers = pd.read_sql_query("""
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT ord.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    JOIN orders AS ord
        ON od.orderNumber = ord.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
df_customers = pd.read_sql_query("""
    SELECT
        o.officeCode,
        o.city,
        COUNT(c.customerNumber) AS n_customers
    FROM offices AS o
    JOIN employees AS e
        ON o.officeCode = e.officeCode
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10
df_under_20 = pd.read_sql_query("""
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        e.officeCode
    FROM employees AS e
    JOIN offices AS o
        ON e.officeCode = o.officeCode
    WHERE e.employeeNumber IN (
        SELECT c.salesRepEmployeeNumber
        FROM customers AS c
        JOIN orders AS ord
            ON c.customerNumber = ord.customerNumber
        JOIN orderdetails AS od
            ON ord.orderNumber = od.orderNumber
        WHERE od.productCode IN (
            SELECT od2.productCode
            FROM orderdetails AS od2
            JOIN orders AS ord2
                ON od2.orderNumber = ord2.orderNumber
            GROUP BY od2.productCode
            HAVING COUNT(DISTINCT ord2.customerNumber) < 20
        )
    )
    ORDER BY e.lastName, e.firstName
""", conn)

conn.close()