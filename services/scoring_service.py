
import math
from datetime import datetime
from typing import Dict, List, Optional
from ..models.entities import (
    StoreDNA, Partner, CompatibilityScore, 
    ProfitabilityScore, FinalRecommendation
)

class ScoringService:
    """Serviço responsável por calcular scores de compatibilidade e rentabilidade"""

    def __init__(self):
        self.compatibility_weights = {
            "segment_match": 0.3,
            "size_match": 0.25,
            "pain_point_match": 0.25,
            "priority_match": 0.2
        }

        self.profitability_weights = {
            "commission_potential": 0.4,
            "implementation_cost": 0.3,
            "retention_probability": 0.3
        }

    def calculate_compatibility_score(
        self, 
        store_dna: StoreDNA, 
        partner: Partner
    ) -> CompatibilityScore:
        """Calcula score de compatibilidade entre loja e parceiro"""

        # 1. Compatibilidade de segmento
        segment_match = 1.0 if store_dna.segment in partner.target_segments else 0.3

        # 2. Compatibilidade de tamanho
        size_match = 1.0 if store_dna.size in partner.target_sizes else 0.5

        # 3. Match com pain points (simulado)
        pain_point_match = self._calculate_pain_point_match(store_dna.pain_points, partner)

        # 4. Match com prioridades da loja
        priority_match = self._calculate_priority_match(store_dna.priorities, partner)

        # Score total ponderado
        total_score = (
            segment_match * self.compatibility_weights["segment_match"] +
            size_match * self.compatibility_weights["size_match"] +
            pain_point_match * self.compatibility_weights["pain_point_match"] +
            priority_match * self.compatibility_weights["priority_match"]
        )

        return CompatibilityScore(
            store_id=store_dna.store_id,
            partner_id=partner.partner_id,
            segment_match=segment_match,
            size_match=size_match,
            pain_point_match=pain_point_match,
            priority_match=priority_match,
            total_score=min(1.0, total_score),
            calculated_at=datetime.now()
        )

    def calculate_profitability_score(
        self, 
        store_dna: StoreDNA, 
        partner: Partner
    ) -> ProfitabilityScore:
        """Calcula score de rentabilidade para a plataforma"""

        # 1. Potencial de comissão baseado no faturamento da loja
        revenue_factor = min(1.0, store_dna.monthly_revenue / 100000)  # Normaliza até R$ 100k
        commission_potential = partner.commission_rate * revenue_factor

        # 2. Custo de implementação (inverso da complexidade)
        implementation_cost = 1.0 - (partner.integration_complexity / 10.0)

        # 3. Probabilidade de retenção baseada no ROI potencial
        retention_probability = partner.roi_potential / 10.0

        # Score total ponderado
        total_score = (
            commission_potential * self.profitability_weights["commission_potential"] +
            implementation_cost * self.profitability_weights["implementation_cost"] +
            retention_probability * self.profitability_weights["retention_probability"]
        )

        return ProfitabilityScore(
            store_id=store_dna.store_id,
            partner_id=partner.partner_id,
            commission_potential=commission_potential,
            implementation_cost=implementation_cost,
            retention_probability=retention_probability,
            total_score=min(1.0, total_score),
            calculated_at=datetime.now()
        )

    def calculate_final_recommendation(
        self,
        compatibility: CompatibilityScore,
        profitability: ProfitabilityScore,
        compatibility_weight: float = 0.7,
        profitability_weight: float = 0.3
    ) -> FinalRecommendation:
        """Calcula recomendação final balanceando compatibilidade e rentabilidade"""

        final_score = (
            compatibility.total_score * compatibility_weight +
            profitability.total_score * profitability_weight
        )

        # Determina prioridade
        if final_score >= 0.8:
            priority = 1  # Alta
        elif final_score >= 0.6:
            priority = 2  # Média
        else:
            priority = 3  # Baixa

        # Gera reasoning
        reasoning = []
        if compatibility.segment_match > 0.8:
            reasoning.append("Forte compatibilidade com segmento da loja")
        if profitability.commission_potential > 0.6:
            reasoning.append("Alto potencial de receita para a plataforma")
        if compatibility.pain_point_match > 0.7:
            reasoning.append("Resolve pain points identificados")

        return FinalRecommendation(
            store_id=compatibility.store_id,
            partner_id=compatibility.partner_id,
            compatibility_score=compatibility.total_score,
            profitability_score=profitability.total_score,
            final_score=final_score,
            reasoning=reasoning,
            priority=priority,
            estimated_roi=profitability.retention_probability * 100,  # Estimativa simplificada
            implementation_timeline="2-4 semanas" if final_score > 0.7 else "4-8 semanas",
            created_at=datetime.now()
        )

    def _calculate_pain_point_match(self, pain_points: List[str], partner: Partner) -> float:
        """Calcula match com pain points (simulado)"""
        if not pain_points:
            return 0.5

        # Simulação: alguns pain points matcham com categorias de parceiros
        category_matches = {
            "baixa_conversao": ["3_navegacao", "4_produto", "5_carrinho"],
            "alto_cac": ["1_atracao"],
            "logistica_cara": ["7_fulfillment", "8_entrega"],
            "pagamentos": ["6_pagamento"],
            "atendimento": ["9_pos_venda"]
        }

        matches = 0
        for pain_point in pain_points:
            for pain_type, categories in category_matches.items():
                if pain_point in pain_type and partner.category.value in categories:
                    matches += 1

        return min(1.0, matches / len(pain_points)) if pain_points else 0.5

    def _calculate_priority_match(self, priorities: Dict, partner: Partner) -> float:
        """Calcula match com prioridades da loja"""
        if not priorities:
            return 0.5

        partner_stage = partner.category.value
        priority_score = priorities.get(partner_stage, 5) / 10.0  # Normaliza para 0-1

        return priority_score
