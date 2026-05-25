from typing import List, Dict, Any, Optional
import asyncio
from sentinel.core.agent import SentinelAgent, IngestionAgent, AnalysisAgent
from sentinel.models.schemas import CompanyHealthScore
from sentinel.core.services import EventStore, CompanyRegistry
from sentinel.agents.ingestion import CodeRepoIngestionAgent, JobPostingIngestionAgent, FinancialDataIngestionAgent
from sentinel.agents.analysis import DigitalExhaustAgent, TalentDynamicsAgent, HiringAuthenticityAgent
from sentinel.agents.synthesis import CompanyHealthScoringAgent
import logging

class SentinelOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger("sentinel.orchestrator")
        self.event_store = EventStore()
        self.registry = CompanyRegistry()
        
        # Initialize and register agents
        self.ingestion_agents = [
            CodeRepoIngestionAgent(self.event_store),
            JobPostingIngestionAgent(self.event_store),
            FinancialDataIngestionAgent(self.event_store)
        ]
        self.analysis_agents = [
            DigitalExhaustAgent(),
            TalentDynamicsAgent(),
            HiringAuthenticityAgent()
        ]
        self.synthesis_agent = CompanyHealthScoringAgent()
        
    async def trigger_ingestion(self, company_id: str) -> List[Dict[str, Any]]:
        """Run Ingestion Swarm (Parallel)."""
        self.logger.info(f"Triggering ingestion for company: {company_id}")
        company = self.registry.get_company(company_id)
        if not company:
            # Register if not exists (minimal for demo)
            self.registry.register_company(company_id, company_id.capitalize(), "Technology")
            company = self.registry.get_company(company_id)

        tasks = [asyncio.to_thread(agent.ingest, company_id) for agent in self.ingestion_agents]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_signals = [signal for sublist in results for signal in sublist]
        return all_signals

    async def run_analysis_pipeline(self, company_id: str) -> CompanyHealthScore:
        """Run the full analysis pipeline for a company."""
        self.logger.info(f"Starting analysis pipeline for: {company_id}")
        
        # 1. Ingestion
        signals = await self.trigger_ingestion(company_id)
        
        # 2. Domain Analysis
        # Normally each agent would filter signals relevant to its domain
        profiles = {}
        for agent in self.analysis_agents:
            profile = await asyncio.to_thread(agent.analyze, signals)
            profiles[agent.name] = profile
        
        # 3. Synthesis
        health_score = await asyncio.to_thread(self.synthesis_agent.run, profiles)
        
        self.logger.info(f"Pipeline complete for {company_id}")
        return health_score

    def handle_query(self, query: str):
        """Routes user query to appropriate sequence."""
        self.logger.info(f"Handling query: {query}")
        pass

