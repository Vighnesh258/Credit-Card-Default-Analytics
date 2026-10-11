"""Credit Card Default Analytics - Streamlit dashboard.
Run it with:  streamlit run app.py
Business question: which credit card customers are most at risk of defaulting
next month, and what early signs identify them?
"""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Credit Card Default Analytics", layout="wide")


# ------------------------------------------------------------------ load data
@st.cache_data
def load_data():
    # The cleaned file made in Google Colab (one row per customer)
    return pd.read_csv("data/credit_card_clean.csv")


df = load_data()

# The order we want groups to appear in on the charts
ORDERS = {
    "AGE_GROUP": ["21-29", "30-39", "40-49", "50-59", "60+"],
    "LIMIT_GROUP": ["Low (up to 50k)", "Medium (50k-150k)", "High (over 150k)"],
    "LIMIT_USED_GROUP": ["Low (under 30%)", "Medium (30-70%)", "High (over 70%)"],
    "EDUCATION": ["Graduate school", "University", "High school", "Others", "Unknown"],
}

# -------------------------------------------------------------------- sidebar
st.sidebar.title("Filters")
st.sidebar.caption("Leave a filter empty to include everyone.")

filtered = df
filters = [("SEX", "Gender"), ("EDUCATION", "Education"), ("MARRIAGE", "Marital status"),
           ("AGE_GROUP", "Age group"), ("LIMIT_GROUP", "Credit limit")]
for column, label in filters:
    options = ORDERS.get(column, sorted(df[column].unique()))
    chosen = st.sidebar.multiselect(label, options)
    if chosen:
        filtered = filtered[filtered[column].isin(chosen)]

st.sidebar.markdown(f"**{len(filtered):,}** of {len(df):,} customers selected")
st.sidebar.divider()
st.sidebar.caption("Data: UCI 'Default of Credit Card Clients' (Yeh & Lien, 2009). "
                   "Real customers of a bank in Taiwan, April to September 2005. "
                   "Amounts are in NT dollars.")

# ----------------------------------------------------------------------- title
st.title("Credit Card Default Analytics")
st.write("**Business question:** which credit card customers are most at risk of "
         "defaulting next month, and what early signs identify them?")

if filtered.empty:
    st.warning("No customers match these filters. Remove a filter to see data.")
    st.stop()

# ------------------------------------------------------------------ top numbers
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{len(filtered):,}")
col2.metric("Default rate", f"{filtered['DEFAULTED'].mean() * 100:.1f}%")
col3.metric("Flagged high risk", f"{(filtered['RISK_FLAG'] == 'High risk').mean() * 100:.1f}%")
col4.metric("Average credit limit", f"NT$ {filtered['LIMIT_BAL'].mean():,.0f}")


# ---------------------------------------------------------------- chart helper
def default_rate_chart(data, column, title, axis_label):
    """Works out the default rate for each group in `column` and draws a bar chart."""
    table = data.groupby(column)["DEFAULTED"].agg(["mean", "size"])
    table["rate"] = (table["mean"] * 100).round(1)
    if column in ORDERS:  # put the groups in a sensible order
        table = table.reindex([g for g in ORDERS[column] if g in table.index])
    fig = px.bar(x=table.index.astype(str), y=table["rate"], text=table["rate"], title=title)
    fig.update_layout(xaxis_title=axis_label, yaxis_title="Default rate (%)")
    fig.update_traces(customdata=table["size"],
                      hovertemplate="%{x}<br>Default rate: %{y}%<br>Customers: %{customdata:,}<extra></extra>")
    st.plotly_chart(fig, width="stretch")


# --------------------------------------------------------- numbers for the text
# These use ALL customers (not the filtered ones) so the written findings stay fixed
on_time = df[df["MONTHS_LATE"] == 0]
late_once = df[df["MONTHS_LATE"] == 1]
flagged = df[df["RISK_FLAG"] == "High risk"]
rate_on_time = on_time["DEFAULTED"].mean() * 100
rate_late_once = late_once["DEFAULTED"].mean() * 100
rate_flagged = flagged["DEFAULTED"].mean() * 100
rate_not_flagged = df[df["RISK_FLAG"] == "Lower risk"]["DEFAULTED"].mean() * 100
share_customers_flagged = len(flagged) / len(df) * 100
share_defaults_caught = flagged["DEFAULTED"].sum() / df["DEFAULTED"].sum() * 100
share_defaults_missed = on_time["DEFAULTED"].sum() / df["DEFAULTED"].sum() * 100
limit_rates = df.groupby("LIMIT_GROUP")["DEFAULTED"].mean() * 100
ontime_low = df[(df["LIMIT_GROUP"] == "Low (up to 50k)") & (df["RISK_FLAG"] == "Lower risk")]["DEFAULTED"].mean() * 100
ontime_high = df[(df["LIMIT_GROUP"] == "High (over 150k)") & (df["RISK_FLAG"] == "Lower risk")]["DEFAULTED"].mean() * 100

# ------------------------------------------------------------------------ tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Repayment history", "Other risk factors", "Risk flag", "Recommendations", "Data"])

with tab1:
    st.subheader("Does a customer's repayment history show who will default?")
    st.write("Each customer's last six months of repayment status were counted to see "
             "how many months they were late. The more months late, the higher the default rate.")
    default_rate_chart(filtered, "MONTHS_LATE", "Default rate by number of late months (out of 6)",
                       "Months late")
    st.info(f"**Insight:** customers who were never late default {rate_on_time:.1f}% of the time. "
            f"Being late even once raises that to {rate_late_once:.1f}%, so the first missed "
            "payment is the earliest warning the bank has.")

with tab2:
    st.subheader("Do credit limit, card usage, age or education also matter?")
    left, right = st.columns(2)
    with left:
        default_rate_chart(filtered, "LIMIT_GROUP", "Default rate by credit limit", "Credit limit (NT$)")
    with right:
        default_rate_chart(filtered, "LIMIT_USED_GROUP", "Default rate by share of limit used",
                           "Latest bill as % of limit")
    left, right = st.columns(2)
    with left:
        default_rate_chart(filtered, "AGE_GROUP", "Default rate by age group", "Age group")
    with right:
        default_rate_chart(filtered, "EDUCATION", "Default rate by education", "Education")
    st.caption("Hover over a bar to see how many customers it covers. Groups with few "
               "customers (for example education 'Others' or age 60+) give unreliable rates.")
    st.info(f"**Insight:** customers with low credit limits default {limit_rates['Low (up to 50k)']:.1f}% "
            f"of the time, against {limit_rates['High (over 150k)']:.1f}% for high limits. "
            "Age, education and gender show smaller differences.")

with tab3:
    st.subheader("Which customers should the bank watch most closely?")
    st.write("A customer is flagged **High risk** if they were late in 2 or more of the last 6 months.")
    summary = filtered.groupby("RISK_FLAG").agg(
        Customers=("ID", "count"),
        Default_rate=("DEFAULTED", "mean"),
        Average_limit=("LIMIT_BAL", "mean"))
    summary["Default rate (%)"] = (summary["Default_rate"] * 100).round(1)
    summary["Average credit limit (NT$)"] = summary["Average_limit"].round(0).astype(int)
    st.dataframe(summary[["Customers", "Default rate (%)", "Average credit limit (NT$)"]],
                 width="stretch")

    defaults_total = filtered["DEFAULTED"].sum()
    caught = filtered[filtered["RISK_FLAG"] == "High risk"]["DEFAULTED"].sum()
    if defaults_total > 0:
        st.metric("Share of all defaults that the flag catches", f"{caught / defaults_total * 100:.1f}%")
    st.info(f"**Insight:** the flag covers {share_customers_flagged:.1f}% of customers but "
            f"{rate_flagged:.1f}% of them default, against {rate_not_flagged:.1f}% for everyone else. "
            f"It catches {share_defaults_caught:.1f}% of all defaults, but {share_defaults_missed:.1f}% "
            "of defaulters had never been late, so repayment history alone is not enough.")

with tab4:
    st.subheader("Recommendations")
    st.caption("Based on all 30,000 customers, not the filters.")
    st.markdown(f"""
1. **Act after the first missed payment.** Customers late once default {rate_late_once:.1f}% of the time,
   against {rate_on_time:.1f}% for on-time customers. A reminder or call after one late month reaches
   customers while the risk is still lower.
2. **Give the 2+ late months group priority.** They are {share_customers_flagged:.1f}% of customers but
   default {rate_flagged:.1f}% of the time. Offer payment plans early and review their credit limits.
3. **Watch low-limit customers even when they pay on time.** On-time customers with low limits default
   {ontime_low:.1f}% of the time, against {ontime_high:.1f}% for on-time customers with high limits.
4. **Do not rely on repayment history alone.** {share_defaults_missed:.1f}% of defaulters had never been
   late, so combine the late-month flag with credit limit checks.
5. **Test before using.** These findings show links, not causes. Try any new contact rule on a small group
   first and compare results.
""")

with tab5:
    st.subheader("Customer data")
    st.write(f"{len(filtered):,} customers match the filters.")
    st.dataframe(filtered, width="stretch")
    st.download_button("Download these customers as CSV", filtered.to_csv(index=False),
                       file_name="filtered_customers.csv", mime="text/csv")
