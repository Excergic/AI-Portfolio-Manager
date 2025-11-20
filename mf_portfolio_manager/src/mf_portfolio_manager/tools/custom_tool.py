from crewai.tools import tool
from mftool import Mftool
from typing import Dict, List

mf = Mftool()

@tool("Get Mutual Fund Details")
def get_scheme_details(scheme_code: str) -> Dict:
    """
    Get detailed information about a mutual fund scheme including NAV,
    expense ratio, fund house, and category.
    
    Args:
        scheme_code: The AMFI scheme code (e.g., '119551')
    
    Returns:
        Dictionary with scheme details
    """
    try:
        data = mf.get_scheme_quote(scheme_code)
        return {
            "scheme_code": scheme_code,
            "scheme_name": data.get('scheme_name'),
            "nav": data.get('nav'),
            "last_updated": data.get('last_updated'),
            "scheme_type": data.get('scheme_type'),
            "scheme_category": data.get('scheme_category'),
            "fund_house": data.get('fund_house')
        }
    except Exception as e:
        return {"error": f"Failed to fetch scheme details: {str(e)}"}


@tool("Get Historical NAV")
def get_historical_nav(scheme_code: str, days: int = 30) -> Dict:
    """
    Get historical NAV data for a mutual fund scheme.
    
    Args:
        scheme_code: The AMFI scheme code
        days: Number of days of historical data (default 30)
    
    Returns:
        Dictionary with historical NAV data
    """
    try:
        data = mf.get_scheme_historical_nav(scheme_code)
        return {
            "scheme_code": scheme_code,
            "historical_nav": data['data'][:days],
            "fund_house": data.get('fund_house')
        }
    except Exception as e:
        return {"error": f"Failed to fetch historical NAV: {str(e)}"}


@tool("Get Large Cap Funds")
def get_large_cap_funds() -> List[Dict]:
    """
    Get list of all large cap equity mutual funds with performance data.
    
    Returns:
        List of large cap funds with returns data
    """
    try:
        performance = mf.get_open_ended_equity_scheme_performance(as_json=True)
        return performance.get('Large Cap', [])[:15]
    except Exception as e:
        return {"error": f"Failed to fetch large cap funds: {str(e)}"}


@tool("Get Mid Cap Funds")
def get_mid_cap_funds() -> List[Dict]:
    """
    Get list of all mid cap equity mutual funds with performance data.
    
    Returns:
        List of mid cap funds with returns data
    """
    try:
        performance = mf.get_open_ended_equity_scheme_performance(as_json=True)
        return performance.get('Mid Cap', [])[:15]
    except Exception as e:
        return {"error": f"Failed to fetch mid cap funds: {str(e)}"}


@tool("Get Small Cap Funds")
def get_small_cap_funds() -> List[Dict]:
    """
    Get list of all small cap equity mutual funds with performance data.
    
    Returns:
        List of small cap funds with returns data
    """
    try:
        performance = mf.get_open_ended_equity_scheme_performance(as_json=True)
        return performance.get('Small Cap', [])[:15]
    except Exception as e:
        return {"error": f"Failed to fetch small cap funds: {str(e)}"}


@tool("Calculate SIP Returns")
def calculate_sip_returns(
    scheme_code: str,
    monthly_sip: float,
    investment_months: int
) -> Dict:
    """
    Calculate SIP returns with IRR for a mutual fund scheme.
    
    Args:
        scheme_code: The AMFI scheme code
        monthly_sip: Monthly SIP amount in rupees
        investment_months: Number of months of SIP investment
    
    Returns:
        Dictionary with SIP returns data including IRR
    """
    try:
        returns = mf.calculate_returns(
            code=scheme_code,
            monthly_sip=monthly_sip,
            investment_in_months=investment_months
        )
        return {
            "scheme_code": returns.get('scheme_code'),
            "scheme_name": returns.get('scheme_name'),
            "current_nav": returns.get('nav'),
            "total_invested": monthly_sip * investment_months,
            "final_value": returns.get('final_investment_value'),
            "absolute_return": returns.get('absolute_return'),
            "irr_annualized": returns.get('IRR_annualised_return')
        }
    except Exception as e:
        return {"error": f"Failed to calculate SIP returns: {str(e)}"}


@tool("Calculate Lumpsum Returns")
def calculate_lumpsum_returns(
    purchase_nav: float,
    current_nav: float,
    investment_amount: float,
    holding_years: float
) -> Dict:
    """
    Calculate lumpsum investment returns with CAGR.
    
    Args:
        purchase_nav: NAV at time of purchase
        current_nav: Current NAV
        investment_amount: Lumpsum investment amount
        holding_years: Holding period in years
    
    Returns:
        Dictionary with lumpsum returns including CAGR
    """
    try:
        units = investment_amount / purchase_nav
        current_value = units * current_nav
        gain = current_value - investment_amount
        absolute_return = (gain / investment_amount) * 100
        cagr = (((current_value / investment_amount) ** (1 / holding_years)) - 1) * 100
        
        return {
            "invested_amount": investment_amount,
            "units_purchased": round(units, 3),
            "purchase_nav": purchase_nav,
            "current_nav": current_nav,
            "current_value": round(current_value, 2),
            "gain": round(gain, 2),
            "absolute_return_pct": round(absolute_return, 2),
            "cagr_pct": round(cagr, 2)
        }
    except Exception as e:
        return {"error": f"Failed to calculate lumpsum returns: {str(e)}"}


@tool("Calculate Capital Gains Tax")
def calculate_capital_gains_tax(
    gain_amount: float,
    holding_months: int,
    fund_type: str = "equity"
) -> Dict:
    """
    Calculate capital gains tax on mutual fund investments.
    
    Equity Funds:
    - STCG (< 12 months): 20%
    - LTCG (>= 12 months): 12.5% on gains above ₹1.25 lakh
    
    Args:
        gain_amount: Capital gain in rupees
        holding_months: Holding period in months
        fund_type: 'equity' or 'debt' (default: equity)
    
    Returns:
        Dictionary with tax calculation details
    """
    try:
        if fund_type.lower() == "equity":
            if holding_months < 12:
                # Short term capital gains
                tax = gain_amount * 0.20
                return {
                    "fund_type": "Equity",
                    "holding_period_months": holding_months,
                    "gain_type": "Short Term (STCG)",
                    "tax_rate": "20%",
                    "taxable_gain": gain_amount,
                    "tax_amount": round(tax, 2),
                    "post_tax_gain": round(gain_amount - tax, 2)
                }
            else:
                # Long term capital gains
                exempt_amount = 125000
                taxable_gain = max(0, gain_amount - exempt_amount)
                tax = taxable_gain * 0.125
                return {
                    "fund_type": "Equity",
                    "holding_period_months": holding_months,
                    "gain_type": "Long Term (LTCG)",
                    "tax_rate": "12.5%",
                    "total_gain": gain_amount,
                    "exempt_amount": exempt_amount,
                    "taxable_gain": taxable_gain,
                    "tax_amount": round(tax, 2),
                    "post_tax_gain": round(gain_amount - tax, 2)
                }
        else:
            return {"error": "Debt fund taxation requires income tax slab information"}
    except Exception as e:
        return {"error": f"Failed to calculate tax: {str(e)}"}
