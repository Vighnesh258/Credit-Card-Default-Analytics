# Data dictionary

Source: UCI Machine Learning Repository, *Default of Credit Card Clients* (Yeh & Lien, 2009). One row per credit card customer, 30,000 rows. Amounts are in NT dollars. Months run April to September 2005.

## Original columns (25)

| Column | Meaning |
| --- | --- |
| ID | Customer number |
| LIMIT_BAL | Credit limit (individual plus family credit) |
| SEX | Male or Female (decoded from 1 and 2) |
| EDUCATION | Graduate school, University, High school, Others or Unknown (decoded) |
| MARRIAGE | Married, Single, Others or Unknown (decoded) |
| AGE | Age in years |
| PAY_0 | Repayment status in September 2005 (the source has no PAY_1) |
| PAY_2 to PAY_6 | Repayment status in August, July, June, May and April 2005 |
| BILL_AMT1 to BILL_AMT6 | Bill statement amount, September back to April |
| PAY_AMT1 to PAY_AMT6 | Amount paid, September back to April |
| default.payment.next.month | Yes if the customer defaulted the next month, otherwise No |

Repayment status values: Paid duly, No consumption, Revolving credit (minimum paid), and 1 to 9 months delay. The source documents "paid duly" and the delays. "No consumption" (-2) and "Revolving credit" (0) are not explained in the source, and the labels follow the usual interpretation.

## Columns created for this project (7)

| Column | How it was made |
| --- | --- |
| DEFAULTED | 1 if default.payment.next.month is Yes, otherwise 0 |
| AGE_GROUP | AGE grouped into 21-29, 30-39, 40-49, 50-59, 60+ |
| LIMIT_GROUP | LIMIT_BAL grouped into Low (up to 50k), Medium (50k-150k), High (over 150k) |
| LIMIT_USED_PCT | BILL_AMT1 divided by LIMIT_BAL, as a percentage. Negative bills (overpayments) are set to 0 |
| LIMIT_USED_GROUP | LIMIT_USED_PCT grouped into Low (under 30%), Medium (30-70%), High (over 70%) |
| MONTHS_LATE | How many of the six repayment status columns show a delay (0 to 6) |
| RISK_FLAG | High risk if MONTHS_LATE is 2 or more, otherwise Lower risk |
