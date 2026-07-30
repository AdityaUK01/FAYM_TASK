-- ===========================================
-- FAYM PRODUCT MANAGEMENT INTERN ASSIGNMENT
-- Name: Aditya Rawat
-- ===========================================

USE faym_assignment;

-- ===========================================
-- Q1: 7th Highest Debit Amount Through IMPS
-- ===========================================

SELECT DISTINCT transaction_amt
FROM transactions
WHERE transaction_type = 'DEBIT'
  AND narration = 'IMPS'
ORDER BY transaction_amt DESC
LIMIT 1 OFFSET 6;

-- ===========================================
-- Q2: Number of Transactions Category-wise
-- ===========================================

SELECT
    narration AS transaction_category,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY narration
ORDER BY total_transactions DESC;

-- ===========================================
-- Q3: Statistical Summary
-- ===========================================

SELECT
    COUNT(*) AS Total_Transactions,
    MIN(transaction_amt) AS Minimum,
    MAX(transaction_amt) AS Maximum,
    ROUND(AVG(transaction_amt),2) AS Mean,
    ROUND(STDDEV(transaction_amt),2) AS Std_Deviation,
    ROUND(VARIANCE(transaction_amt),2) AS Variance
FROM transactions;

-- ===========================================
-- ===========================================
-- Q4: Monthly Cohort View (Users doing DEBIT transactions)
-- ===========================================

WITH first_month AS (
    SELECT
        user_id,
        DATE_FORMAT(
            MIN(STR_TO_DATE(transaction_time,'%m/%d/%Y')),
            '%Y-%m'
        ) AS cohort_month
    FROM transactions
    WHERE transaction_type='DEBIT'
    GROUP BY user_id
)

SELECT
    f.cohort_month AS First_Month,
    DATE_FORMAT(
        STR_TO_DATE(t.transaction_time,'%m/%d/%Y'),
        '%Y-%m'
    ) AS Activity_Month,
    COUNT(DISTINCT t.user_id) AS Active_Users
FROM transactions t
JOIN first_month f
ON t.user_id=f.user_id
WHERE t.transaction_type='DEBIT'
GROUP BY
    f.cohort_month,
    Activity_Month
ORDER BY
    f.cohort_month,
    Activity_Month;

-- ===========================================
-- Q5: Top 10 Percentile Users
-- (Highest Net Amount = DEBIT - CREDIT)
-- ===========================================

WITH net_amount AS (
    SELECT
        user_id,
        SUM(
            CASE
                WHEN transaction_type = 'DEBIT' THEN transaction_amt
                WHEN transaction_type = 'CREDIT' THEN -transaction_amt
                ELSE 0
            END
        ) AS net_amount
    FROM transactions
    GROUP BY user_id
)

SELECT
    user_id,
    net_amount
FROM net_amount
ORDER BY net_amount DESC
LIMIT 1;