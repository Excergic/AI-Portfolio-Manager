# MfPortfolioManager Crew

Welcome to the MfPortfolioManager Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/mf_portfolio_manager/config/agents.yaml` to define your agents
- Modify `src/mf_portfolio_manager/config/tasks.yaml` to define your tasks
- Modify `src/mf_portfolio_manager/crew.py` to add your own logic, tools and specific args
- Modify `src/mf_portfolio_manager/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the mf-portfolio-manager Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Chat UI

You can interact with the crew through a lightweight web chat that wraps the same kickoff flow:

1. Install the dependencies (from this folder):
   ```bash
   uv sync
   ```
2. Start the API + static site:
   ```bash
   uv run uvicorn mf_portfolio_manager.web.server:app --reload
   ```
3. Open [http://localhost:8000](http://localhost:8000) and send prompts. All form fields map directly to the crew input variables so you can tweak budgets, risk profile, and other parameters per run.

## CrewAI Tracking

Every API call executed through the chat (or CLI) is traced via CrewAI’s native tracking system.

1. Log into CrewAI AMP and grab your API key:
   ```bash
   crewai login
   ```
2. Set the key and toggle tracking (already enabled by default) before running the UI or CLI:
   ```bash
   export CREWAI_API_KEY="sk-..."
   export CREWAI_ENABLE_TRACKING=true
   ```
3. Execute the crew (via `crewai run` or the chat UI). Each run now appears inside [https://app.crewai.com](https://app.crewai.com) with tool invocations, prompts, and responses for auditing purposes.

## Understanding Your Crew

The mf-portfolio-manager Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the MfPortfolioManager Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
