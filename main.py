import asyncio
import logging
from sentinel.core.orchestrator import SentinelOrchestrator
from sentinel.core.llm import router

logging.basicConfig(level=logging.INFO)

async def main():
    print("Project Sentinel - Multi-Agent Intelligence System")
    orchestrator = SentinelOrchestrator()
    
    # Example: Register a company
    # This would normally connect to Postgres
    print("Initializing components...")
    
    # Test LLM Router (Optional, requires GCP credentials)
    # response = router.generate("Hello Sentinel", task_type="reasoning")
    # print(f"LLM Response: {response.content}")

    print("Sentinel ready.")

if __name__ == "__main__":
    asyncio.run(main())
