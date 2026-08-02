 Dr Lal PathLabs — DCF Valuation Model

An interactive discounted cash flow (DCF) model built in Python and Streamlit, estimating fair value per share for Dr Lal PathLabs (NSE: LALPATHLAB), with live sensitivity analysis on key valuation assumptions.

Link to the app :- https://dcf-valuation-model-qy3nsob2tbweb7k4hmghxj.streamlit.app/

What can it do?

- Projects free cash flows over a configurable time horizon based on revenue growth, operating margin, and tax assumptions
- Discounts projected cash flows back to present value using WACC
- Calculates terminal value using the Gordon Growth (perpetuity) method
- Derives Enterprise Value → Equity Value → Implied Share Price
- Compares the model's implied value against the current market price
- Includes a live sensitivity analysis (heatmap + table) showing how valuation shifts across a range of WACC and growth rate assumptions
- All inputs are adjustable via an interactive sidebar — no code changes needed to test different scenarios


The model uses a simplified DCF approach to give out seven outcomes:

1. **Free Cash Flow** = Revenue × Operating Margin × (1 − Tax Rate)
2. **Discounted FCF** = FCF ÷ (1 + WACC)^year, for each projected year
3. **Terminal Value** = Final Year FCF × (1 + Terminal Growth Rate) ÷ (WACC − Terminal Growth Rate)
4. **Enterprise Value** = Sum of Discounted FCFs + Discounted Terminal Value
5. **Equity Value** = Enterprise Value − Net Debt
6. **Implied Share Price** = Equity Value ÷ Shares Outstanding

This is a streamlined model — it does not account for working capital changes or capex separately, and uses assumed (not derived) WACC and terminal growth rate. Built as a portfolio project to demonstrate applied valuation logic rather than as investment advice.

## Key Finding

Using a conservative 10% revenue growth assumption, the model implies a fair value of ~₹836/share, versus a market price of ~₹1,880/share at time of writing. This gap likely reflects the market pricing in more aggressive growth expectations than the model's base case — consistent with the company's recent ~19% YoY revenue growth and ongoing expansion (new labs, M&A activity in South India, Gujarat, and international markets).

## Tech Stack

- Python
- Streamlit (interactive UI)
- Pandas (data handling)
- Matplotlib (sensitivity heatmap)

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

Built for educational and portfolio purposes only. Not investment advice. Assumptions are simplified and should not be relied upon for actual investment decisions.
