from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List

from mf_portfolio_manager.tools.custom_tool import (
    get_scheme_details,
    get_historical_nav,
    get_large_cap_funds,
    get_mid_cap_funds,
    get_small_cap_funds,
    calculate_sip_returns,
    calculate_lumpsum_returns,
    calculate_capital_gains_tax
)

@CrewBase
class MutualFundCrew:
    """MfPortfolioManager crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def mf_data_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['mf_data_researcher'],
            tools = [
                get_scheme_details,
                get_historical_nav,
                get_large_cap_funds,
                get_mid_cap_funds,
                get_small_cap_funds
            ],
            verbose=True
        )

    @agent
    def returns_calculator(self) -> Agent:
        return Agent(
            config=self.agents_config['returns_calculator'],
            tools = [
                calculate_sip_returns,
                calculate_lumpsum_returns,
                calculate_capital_gains_tax
            ],
            verbose=True
        )
    
    @agent
    def investment_advisor(self) -> Agent:
        return Agent(
            config = self.agents_config['investment_advisor'],
            allow_delegation = True,
        )

    @task
    def collect_fund_data(self) -> Task:
        return Task(
            config=self.tasks_config['collect_fund_data'],
        )

    @task
    def calculate_sip_returns(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_sip_returns'],
        )

    @task
    def calculate_lumpsum_returns_task(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_lumpsum_returns']
        )

    @task
    def provide_investment_advice(self) -> Task:
        return Task(
            config=self.tasks_config['provide_investment_advice'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MfPortfolioManager crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
