#!/usr/bin/env python
from json import load
import sys
from typing_extensions import override
import warnings
from mf_portfolio_manager.crew import MutualFundCrew
from dotenv import load_dotenv

load_dotenv(override=True)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the mutual fund crew with custom inputs
    """
    inputs = {
        # Fund category selection
        'fund_category': 'Large Cap',
        'scheme_codes': '119551,120503',  # Optional: specific schemes
        
        # SIP calculation inputs
        'scheme_code': '119551',  # Axis Bluechip Fund
        'monthly_sip': 10000,
        'investment_months': 60,
        'holding_months': 60,
        
        # Lumpsum calculation inputs
        'lumpsum_amount': 100000,
        'purchase_nav': 45.50,
        'current_nav': 68.75,
        'holding_years': 3,
        
        # Investor profile
        'risk_profile': 'Moderate',
        'investment_horizon': 7,
        'investment_type': 'SIP',
        'monthly_budget': 15000,
        'lumpsum_budget': 0,
        'fund_categories': 'Large Cap, Mid Cap',
        'investment_goal': 'Long-term wealth creation and retirement planning'
    }
    
    result = MutualFundCrew().crew().kickoff(inputs=inputs)
    print("\n\n========================")
    print("## Investment Analysis Report")
    print("========================\n")
    print(result)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'fund_category': 'Large Cap',
        'scheme_code': '119551',
        'monthly_sip': 5000,
        'investment_months': 36,
        'holding_months': 36,
        'risk_profile': 'Moderate',
        'investment_horizon': 5,
        'investment_type': 'SIP',
        'monthly_budget': 10000,
        'fund_categories': 'Large Cap'
    }
    try:
        MutualFundCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    run()