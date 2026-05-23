from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

class SignalRef(BaseModel):
    signal_id: str
    source_type: str
    timestamp: datetime

class EvidenceRef(BaseModel):
    claim: str
    source_ids: List[str]
    confidence: float

class DimensionScore(BaseModel):
    score: float                   # 0.0 - 1.0
    trend: Literal['improving', 'stable', 'declining']
    confidence: float
    key_signals: List[SignalRef]

class TrajectoryDist(BaseModel):
    growth_prob: float
    stable_prob: float
    pivot_prob: float
    decline_prob: float
    collapse_prob: float

class CompanyHealthScore(BaseModel):
    company_id: str
    timestamp: datetime
    strategic_coherence: DimensionScore
    org_vitality: DimensionScore
    tech_foundation: DimensionScore
    financial_resilience: DimensionScore
    talent_dynamics: DimensionScore
    competitive_position: DimensionScore
    dependency_robustness: DimensionScore
    composite_score: float         # 0.0 - 1.0
    trajectory_1yr: TrajectoryDist
    trajectory_5yr: TrajectoryDist
    confidence: float
    evidence_summary: List[EvidenceRef]
    assumptions: List[str]
    shelf_life_days: int

class CompanyRef(BaseModel):
    company_id: str
    name: str

class TalentDynamicsProfile(BaseModel):
    company_id: str
    net_talent_flow: float         # positive = gaining
    senior_attrition_rate: float
    junior_attrition_rate: float
    replacement_quality_delta: float  # positive = upgrades
    top_destinations: List[CompanyRef]
    top_sources: List[CompanyRef]
    employer_brand_trend: Literal['rising', 'stable', 'falling']
    offer_acceptance_rate: Optional[float] = None
    magnetism_score: float         # 0.0 - 1.0
    confidence: float

class HiringAuthenticityReport(BaseModel):
    company_id: str
    total_postings: int
    genuine_pct: float
    ghost_pct: float
    defensive_pct: float
    aspirational_pct: float
    indeterminate_pct: float
    confidence: float

class VulnerabilityRef(BaseModel):
    id: str
    description: str
    severity: float

class Dependency(BaseModel):
    dep_id: str
    type: Literal['tech_vendor', 'oss', 'supply_chain',
                   'customer', 'regulatory', 'key_person']
    name: str
    criticality: float            # 0.0 - 1.0
    substitutability: float
    counterparty_risk: float
    disruption_prob_1yr: float

class DependencyRiskMap(BaseModel):
    company_id: str
    dependencies: List[Dependency]
    overall_fragility: float
    top_vulnerabilities: List[VulnerabilityRef]

class NarrativeDivergenceScore(BaseModel):
    company_id: str
    divergence_level: float       # 0.0 (aligned) - 1.0 (max divergence)
    classification: Literal['aligned', 'opacity', 'deception', 'indeterminate']
    top_divergence_areas: List[str]
    confidence: float

class StealthPivotAlert(BaseModel):
    company_id: str
    detected_at: datetime
    pivot_direction: str           # inferred new strategic direction
    evidence_signals: List[SignalRef]
    signal_types_count: int        # must be >= 2
    confidence: float

class SuitabilityRecommendation(BaseModel):
    company_id: str
    user_id: str
    recommendation: Literal['apply', 'avoid', 'monitor']
    reasons: List[str]
    risk_factors: List[str]
    change_conditions: List[str]   # what would flip the recommendation
    confidence: float
    role_context: Optional[str] = None
