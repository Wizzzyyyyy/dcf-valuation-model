import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Title ---
st.title("📊 Dr Lal PathLabs — DCF Valuation Model")
st.markdown("An interactive discounted cash flow model estimating fair value per share, with sensitivity analysis on WACC and growth assumptions.")

# --- Sidebar Inputs ---
st.sidebar.header("Assumptions")
current_revenue = st.sidebar.number_input("Current Revenue (Cr)", value=2763.0)
growth_rate = st.sidebar.slider("Growth Rate", 0.0, 0.30, 0.10)
operating_margin = st.sidebar.slider("Operating Margin", 0.0, 0.50, 0.28)
tax_rate = st.sidebar.slider("Tax Rate", 0.0, 0.40, 0.25)
wacc = st.sidebar.slider("WACC", 0.05, 0.20, 0.11)
terminal_growth_rate = st.sidebar.slider("Terminal Growth Rate", 0.01, 0.08, 0.045)
num_years = st.sidebar.slider("Projection Years", 5, 15, 10)
net_debt = st.sidebar.number_input("Net Debt (Cr)", value=0.0)
shares_outstanding = st.sidebar.number_input("Shares Outstanding (Cr)", value=16.8)
market_price = st.sidebar.number_input("Current Market Price (₹)", value=1878.0)

# --- Core Functions ---
def calculate_revenue(current_rev, growth, year):
    return current_rev * ((1 + growth) ** year)

def calculate_fcf(revenue_val, margin, tax):
    return revenue_val * margin * (1 - tax)

def calculate_discounted_fcf(fcf_val, wacc_val, year):
    return fcf_val / ((1 + wacc_val) ** year)

def terminal_value(last_year_fcf, terminal_growth, wacc_val):
    return last_year_fcf * (1 + terminal_growth) / (wacc_val - terminal_growth)

def calculate_enterprise_value(current_revenue, growth_rate, operating_margin, tax_rate, wacc, terminal_growth_rate, num_years, verbose=False):
    dfcflist = []
    last_fcf = None

    for year in range(1, num_years + 1):
        rev = calculate_revenue(current_revenue, growth_rate, year)
        fcf = calculate_fcf(rev, operating_margin, tax_rate)
        dfcf = calculate_discounted_fcf(fcf, wacc, year)
        dfcflist.append(dfcf)
        last_fcf = fcf
        if verbose:
            print(f"Year {year}: Revenue = {rev:.2f}, FCF = {fcf:.2f}, Discounted FCF = {dfcf:.2f}")

    tv = terminal_value(last_fcf, terminal_growth_rate, wacc)
    discounted_tv = calculate_discounted_fcf(tv, wacc, num_years)
    enterprise_value = round(sum(dfcflist) + discounted_tv, 2)
    equity_value = enterprise_value - net_debt
    share_price = equity_value / shares_outstanding

    return {"enterprise_value": enterprise_value, "equity_value": equity_value, "share_price": share_price}

# --- Run Base Case ---
result = calculate_enterprise_value(current_revenue, growth_rate, operating_margin, tax_rate, wacc, terminal_growth_rate, num_years)
diff_pct = ((result['share_price'] - market_price) / market_price) * 100

# --- Valuation Summary ---
st.subheader("Valuation Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Implied Share Price", f"₹{result['share_price']:.2f}")
col2.metric("Enterprise Value (Cr)", f"₹{result['enterprise_value']:.2f}")
col3.metric("vs Market Price", f"{diff_pct:+.1f}%")

with st.expander("How this model works"):
    st.markdown("""
    This model projects Free Cash Flow (Revenue × Operating Margin × (1 - Tax Rate)) for each year,
    discounts it back to present value using WACC, adds a terminal value (Gordon Growth method),
    and derives Enterprise Value → Equity Value → Implied Share Price.
    Adjust the assumptions in the sidebar to see how the valuation changes.
    """)

# --- Sensitivity Analysis ---
st.subheader("Sensitivity Analysis")

WACCrange = [7, 9, 11, 13, 15]
growrange = [6, 8, 10, 12, 14]

dictwa = {}
for wad in WACCrange:
    dictwa[wad] = {}
    for gre in growrange:
        r = calculate_enterprise_value(current_revenue, gre / 100, operating_margin, tax_rate, wad / 100, terminal_growth_rate, num_years)
        dictwa[wad][gre] = r["enterprise_value"]

df_sensitivity = pd.DataFrame.from_dict(dictwa, orient='index')
df_sensitivity.index.name = "WACC (%)"
df_sensitivity.columns.name = "Growth Rate (%)"

st.dataframe(df_sensitivity.round(2))

fig, ax = plt.subplots()
im = ax.imshow(df_sensitivity.values, cmap='viridis', origin='lower')
ax.set_xticks(range(len(df_sensitivity.columns)))
ax.set_xticklabels(df_sensitivity.columns)
ax.set_yticks(range(len(df_sensitivity.index)))
ax.set_yticklabels(df_sensitivity.index)
ax.set_xlabel("Growth Rate (%)")
ax.set_ylabel("WACC (%)")
fig.colorbar(im, label="Enterprise Value")
st.pyplot(fig)