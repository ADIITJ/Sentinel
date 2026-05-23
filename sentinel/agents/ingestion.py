from typing import List, Dict, Any
from sentinel.core.agent import IngestionAgent
from sentinel.core.services import EventStore
import logging

class CodeRepoIngestionAgent(IngestionAgent):
    def __init__(self, event_store: EventStore):
        super().__init__(name="CodeRepoIngestionAgent", role="Ingest public code repository data")
        self.event_store = event_store

    def ingest(self, company_org: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Ingesting code repos for {company_org}")
        # Mock fetching from GitHub API
        signals = [
            {"company_id": company_org, "type": "repo_signal", "repo": "main-api", "velocity": 0.8, "timestamp": "2026-05-23T10:00:00"},
            {"company_id": company_org, "type": "repo_signal", "repo": "ui-dashboard", "velocity": 0.5, "timestamp": "2026-05-23T11:00:00"}
        ]
        self.event_store.write_signals("repo_signals", signals)
        return signals

class JobPostingIngestionAgent(IngestionAgent):
    def __init__(self, event_store: EventStore):
        super().__init__(name="JobPostingIngestionAgent", role="Ingest job postings")
        self.event_store = event_store

    def ingest(self, company_id: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Ingesting job postings for {company_id}")
        # Logic to fetch from LinkedIn/Career page
        postings = [
            {"company_id": company_id, "title": "Senior Software Engineer", "dept": "Engineering", "is_ghost": False},
            {"company_id": company_id, "title": "VP Strategy", "dept": "Executive", "is_ghost": True}
        ]
        self.event_store.write_signals("job_postings", postings)
        return postings

class FinancialDataIngestionAgent(IngestionAgent):
    def __init__(self, event_store: EventStore):
        super().__init__(name="FinancialDataIngestionAgent", role="Ingest financial filings")
        self.event_store = event_store

    def ingest(self, ticker: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Ingesting financial data for {ticker}")
        # Logic for SEC EDGAR
        signals = [
            {"company_id": ticker, "type": "financial_signal", "metric": "revenue_growth", "value": 0.15}
        ]
        self.event_store.write_signals("financial_signals", signals)
        return signals
