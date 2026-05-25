from typing import List, Dict, Any
from sentinel.core.agent import SentinelAgent
from sentinel.models.schemas import CompanyHealthScore, DimensionScore, TrajectoryDist, SignalRef
from datetime import datetime


class CompanyHealthScoringAgent(SentinelAgent):
    def __init__(self):
        super().__init__(name="CompanyHealthScoringAgent", role="Aggregate domain profiles into health score")

    def aggregate(self, profiles: Dict[str, Any]) -> CompanyHealthScore:
        self.logger.info("Aggregating profiles into composite health score")
        
        # Extract profiles from the orchestrator's dictionary
        exhaust = profiles.get("DigitalExhaustAgent")
        talent = profiles.get("TalentDynamicsAgent")
        
        company_id = exhaust.company_id if exhaust else "unknown"

        # Tech Foundation comes from DigitalExhaust
        tech_score = DimensionScore(
            score=exhaust.dev_velocity if exhaust else 0.5,
            trend="stable",
            confidence=0.9,
            key_signals=[SignalRef(signal_id=p, source_type="repo", timestamp=datetime.now()) for p in (exhaust.key_patterns if exhaust else [])]
        )
        
        # Org Vitality influenced by Talent
        vitality_score = 0.7
        if talent:
            vitality_score = (talent.magnetism_score + (1 - talent.senior_attrition_rate)) / 2
            
        org_vitality = DimensionScore(
            score=vitality_score,
            trend="improving" if vitality_score > 0.6 else "declining",
            confidence=0.8,
            key_signals=[]
        )

        # Build composite score
        composite = (tech_score.score + org_vitality.score) / 2
        
        return CompanyHealthScore(
            company_id=company_id,
            timestamp=datetime.now(),
            strategic_coherence=DimensionScore(score=0.8, trend="stable", confidence=0.7, key_signals=[]),
            org_vitality=org_vitality,
            tech_foundation=tech_score,
            financial_resilience=DimensionScore(score=0.6, trend="stable", confidence=0.6, key_signals=[]),
            talent_dynamics=DimensionScore(score=talent.magnetism_score if talent else 0.5, trend="stable", confidence=0.8, key_signals=[]),
            competitive_position=DimensionScore(score=0.75, trend="stable", confidence=0.7, key_signals=[]),
            dependency_robustness=DimensionScore(score=0.85, trend="stable", confidence=0.9, key_signals=[]),
            composite_score=composite,
            trajectory_1yr=TrajectoryDist(growth_prob=0.7, stable_prob=0.2, pivot_prob=0.05, decline_prob=0.04, collapse_prob=0.01),
            trajectory_5yr=TrajectoryDist(growth_prob=0.5, stable_prob=0.3, pivot_prob=0.1, decline_prob=0.1, collapse_prob=0.0),
            confidence=0.85,
            evidence_summary=[],
            assumptions=["Maintains talent moat"],
            shelf_life_days=14
        )


    def run(self, profiles: Dict[str, Any]) -> CompanyHealthScore:
        return self.aggregate(profiles)

