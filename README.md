# AI DAX Generator — E-commerce Example

This repository is preloaded with an e-commerce Power BI schema derived from the supplied workbook.

## Included model tables

- Orders
- Returns
- Products
- Customers
- Region Info

## Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Gemini key to `.env`:

```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Run:

```powershell
python -m streamlit run app.py
```

## Example prompts

- Calculate total sales after discount.
- Calculate total revenue including shipping.
- Calculate gross profit using the related product unit cost.
- Calculate return rate as returned orders divided by total orders.
- Calculate average order value.
- Count distinct customers by region.
- Calculate year-to-date net sales.
- Rank products by gross profit.
