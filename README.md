# Credit Card Default Analytics

> **Business question:** which credit card customers are most at risk of defaulting next month, and what early signs identify them?
> This project looks at six months of repayment history, bills, payments and customer details to find which signs separate customers who default from those who do not, then turns the findings into a simple high-risk flag the bank could use.

**Live app:** https://credit-card-default578.streamlit.app/ | **Code:** https://github.com/Vighnesh258/Credit-Card-Default-Analytics | **Author:** Vighnesh | **Stack:** Python, Pandas, Plotly, Streamlit, GitHub

---

## My approach

1. **Frame the problem.** Defined default as failing to pay in the month after the data period, and chose one question to answer: who is most at risk and how can the bank spot them early.
2. **Load and check the data.** Loaded the file in Pandas and checked its shape, column types, missing values and duplicates (none found).
3. **Clean and prepare.** Replaced the numeric codes for gender, education, marital status and repayment status with readable labels, then created seven new columns (listed below).
4. **Explore what separates defaulters from non-defaulters.** Compared the default rate across repayment history, credit limit, share of limit used, age, education, gender and marital status.
5. **Build a risk flag.** Flagged customers who were late in two or more of the last six months and tested how well the flag separates defaulters.
6. **Ship it.** Built a Streamlit dashboard with filters, charts, written insights and recommendations, and published it with GitHub.

## Dataset overview

| Item | Detail |
| --- | --- |
| Name | Default of Credit Card Clients |
| Source | UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients |
| Original paper | Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications*, 36(2), 2473-2480 |
| Licence | CC BY 4.0 |
| Downloaded from | https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset?resource=download |
| Content | Real credit card customers of a bank in Taiwan, April to September 2005 |
| Size | 30,000 customers and 25 columns. 6,636 customers (22.1%) defaulted the next month |

This is real data. It is not synthetic or AI-generated. Full column descriptions are in `data/DATA_DICTIONARY.md`.

**Columns used:** credit limit, gender, education, marital status, age, six months of repayment status, six months of bill amounts, six months of payment amounts, and whether the customer defaulted.

## Data preparation

- **Checks:** no missing values, no duplicate rows, and every customer ID is unique.
- **Decoding:** replaced codes such as 1 and 2 with labels (for example Male and Female). Education codes 0, 5 and 6 (345 customers) and marital status code 0 (54 customers) are not explained in the source, so they are labelled Unknown.
- **Repayment status:** the source documents "paid duly" and the months of delay. The codes -2 and 0 are not documented, and they are labelled "No consumption" and "Revolving credit (minimum paid)", following the usual interpretation. Neither counts as late.
- **New columns:** DEFAULTED (1 or 0), AGE_GROUP, LIMIT_GROUP, LIMIT_USED_PCT, LIMIT_USED_GROUP, MONTHS_LATE (months with a delay, 0 to 6) and RISK_FLAG (High risk if late 2 or more months).
- **Overpayments:** a few latest bills are negative because the customer overpaid, so those were set to 0% of the limit used.

## Analysis and key findings

**Overall.** 22.1% of customers (6,636 of 30,000) defaulted the next month.

**Repayment history is the strongest signal.**

| Months late (of 6) | Customers | Default rate |
| --- | --- | --- |
| 0 | 19,931 | 11.7% |
| 1 | 4,426 | 29.8% |
| 2 | 1,899 | 38.8% |
| 3 | 1,154 | 50.9% |
| 4 | 951 | 57.3% |
| 5 | 298 | 57.4% |
| 6 | 1,341 | 70.3% |

One late month already raises the default rate about 2.5 times, from 11.7% to 29.8%.

**The risk flag.** Customers late in 2 or more months make up 18.8% of customers (5,643). 52.8% of them default, against 15.0% of everyone else. The flag catches 44.9% of all defaults. However, 35.2% of defaulters had never been late, so the flag misses a large share.

**Credit limit also matters.**

| Credit limit | Customers | Default rate |
| --- | --- | --- |
| Low (up to 50k) | 7,676 | 31.8% |
| Medium (50k-150k) | 8,724 | 23.7% |
| High (over 150k) | 13,600 | 15.6% |

The gap remains among customers who paid on time: 20.6% for low limits against 12.5% for high limits.

**Share of limit used is a weaker signal.** The default rate rises from 18.3% (under 30% used) to 24.0% (30-70%) and 26.9% (over 70%). Once late months are taken into account, the differences between usage groups are small and inconsistent.

**Customer details differ less.**

- Age: 20.3% for ages 30-39 up to 28.3% for 60 and over, although only 339 customers are 60 or over.
- Education: 19.2% for graduate school, 23.7% for university and 25.2% for high school.
- Gender: 20.8% for women and 24.2% for men.
- Marital status: 20.9% for single customers and 23.5% for married customers.

## Recommendations

1. **Act after the first missed payment.** Customers late once default 29.8% of the time, against 11.7% for on-time customers. A reminder or call after one late month reaches them while the risk is lower.
2. **Give the 2+ late months group priority.** They are 18.8% of customers and 52.8% of them default. Offer payment plans early and review their credit limits.
3. **Watch low-limit customers even when they pay on time.** They default 20.6% of the time, against 12.5% for on-time customers with high limits.
4. **Do not rely on repayment history alone.** 35.2% of defaulters had never been late, so combine the late-month flag with credit limit checks.
5. **Test before using.** Try any new contact rule on a small group first and compare the results.

## What the app does

| Tab | What you can do |
| --- | --- |
| Repayment history | Default rate by number of late months, with an insight box |
| Other risk factors | Default rate by credit limit, share of limit used, age and education |
| Risk flag | High risk and Lower risk compared side by side, and the share of defaults the flag catches |
| Recommendations | Five recommendations tied to the findings |
| Data | Filtered customer table with a CSV download |

The sidebar filters (gender, education, marital status, age group and credit limit) apply to the top numbers and all charts. The written insights and recommendations always use all customers.

## Run locally

```
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```
app.py                       Streamlit dashboard (all code)
requirements.txt             Python packages needed
README.md                    This write-up
data/credit_card_clean.csv   Cleaned data with the seven new columns
data/DATA_DICTIONARY.md      Column descriptions
```

## Limitations

- The data is from Taiwan in 2005, so the patterns may not match customers today or in other countries.
- It covers cards only, with no accounts, loans or digital banking.
- Findings show association, not cause. For example, late payments go with defaults, but this analysis does not prove that contacting customers earlier would prevent them.
- Some groups are small (education Others and Unknown, age 60 and over), so their rates are unreliable.
- The risk flag is a simple rule. It was not tested on separate data, and the thresholds should be checked before use.
