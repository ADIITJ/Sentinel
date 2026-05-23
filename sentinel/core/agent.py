from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from sentinel.core.llm import router, LLMResponse
from pydantic import BaseModel
import logging

class SentinelAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.logger = logging.getLogger(f"sentinel.agent.{name}")
    
    @abstractmethod
    def run(self, input_data: Any) -> Any:
        pass

    def ask_llm(self, prompt: str, task_type: str = "reasoning") -> LLMResponse:
        self.logger.info(f"Asking LLM for task: {task_type}")
        return router.generate(prompt, task_type=task_type)

class IngestionAgent(SentinelAgent):
    """Base class for Layer 1 agents."""
    @abstractmethod
    def ingest(self, source_info: Any) -> List[Dict[str, Any]]:
        pass
    
    def run(self, input_data: Any) -> List[Dict[str, Any]]:
        return self.ingest(input_data)

class AnalysisAgent(SentinelAgent):
    """Base class for Layer 2 agents."""
    @abstractmethod
    def analyze(self, signals: List[Dict[str, Any]]) -> BaseModel:
        pass
    
    def run(self, input_data: List[Dict[str, Any]]) -> BaseModel:
        return self.analyze(input_data)
