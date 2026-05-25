from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sentinel.models.schemas import CompanyHealthScore, SuitabilityRecommendation, DependencyRiskMap
from sentinel.core.orchestrator import SentinelOrchestrator
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentinel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = SentinelOrchestrator()

@app.get("/")

def read_root():
    return {"status": "Sentinel Active", "timestamp": datetime.now()}

@app.get("/api/v1/company/{company_id}/health", response_model=CompanyHealthScore)
async def get_company_health(company_id: str):
    try:
        score = await orchestrator.run_analysis_pipeline(company_id)
        if not score:
            raise HTTPException(status_code=500, detail="Failed to generate health score")
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/query/suitability", response_model=SuitabilityRecommendation)
async def get_suitability(company_id: str, user_id: str, role_context: Optional[str] = None):
    # Logic for suitability
    return SuitabilityRecommendation(
        company_id=company_id,
        user_id=user_id,
        recommendation="apply",
        reasons=["Strong tech foundation", "Strategic coherence is high"],
        risk_factors=["High dependency fragility"],
        change_conditions=["Revenue growth stalls"],
        confidence=0.85,
        role_context=role_context
    )

@app.get("/api/v1/company/{company_id}/fragility", response_model=DependencyRiskMap)
async def get_fragility(company_id: str):
    return DependencyRiskMap(
        company_id=company_id,
        dependencies=[],
        overall_fragility=0.4,
        top_vulnerabilities=[]
    )
