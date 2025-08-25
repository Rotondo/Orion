
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..models.entities import (
    StoreDNA, Partner, FinalRecommendation, 
    EcommerceStage, StoreSegment, StoreSize
)
from ..services.dna_service import DNAService
from ..services.scoring_service import ScoringService
from ..agents.autonomous_agents import AgentOrchestrator

class RecommendationService:
    """Serviço responsável por gerar recomendações personalizadas"""

    def __init__(self):
        self.dna_service = DNAService()
        self.scoring_service = ScoringService()
        self.agent_orchestrator = AgentOrchestrator()
        self.partners_db = {}  # Simulação do catálogo de parceiros

    def add_partner(self, partner: Partner):
        """Adiciona parceiro ao catálogo"""
        self.partners_db[partner.partner_id] = partner
        # Registra agente do parceiro
        self.agent_orchestrator.register_partner_agent(partner)

    def get_recommendations_for_store(
        self, 
        store_id: str, 
        limit: int = 10,
        min_score: float = 0.3
    ) -> List[FinalRecommendation]:
        """Gera recomendações personalizadas para uma loja"""

        # Recupera DNA da loja
        store_dna = self.dna_service.get_store_dna(store_id)
        if not store_dna:
            return []

        recommendations = []

        # Para cada parceiro, calcula scores
        for partner in self.partners_db.values():
            # Score de compatibilidade
            compatibility = self.scoring_service.calculate_compatibility_score(
                store_dna, partner
            )

            # Score de rentabilidade
            profitability = self.scoring_service.calculate_profitability_score(
                store_dna, partner
            )

            # Recomendação final
            recommendation = self.scoring_service.calculate_final_recommendation(
                compatibility, profitability
            )

            # Filtra por score mínimo
            if recommendation.final_score >= min_score:
                recommendations.append(recommendation)

        # Ordena por score final
        recommendations.sort(key=lambda x: x.final_score, reverse=True)

        return recommendations[:limit]

    def get_priority_recommendations(
        self, 
        store_id: str,
        focus_areas: List[EcommerceStage] = None
    ) -> Dict[str, List[FinalRecommendation]]:
        """Gera recomendações priorizadas por áreas de foco"""

        if not focus_areas:
            # Identifica gaps automaticamente
            gaps = self.dna_service.identify_gaps(store_id)
            focus_areas = [EcommerceStage(gap["stage"]) for gap in gaps[:3]]

        priority_recommendations = {}

        for stage in focus_areas:
            # Filtra parceiros da categoria
            stage_partners = [
                p for p in self.partners_db.values() 
                if p.category == stage
            ]

            stage_recommendations = []
            store_dna = self.dna_service.get_store_dna(store_id)

            if store_dna:
                for partner in stage_partners:
                    compatibility = self.scoring_service.calculate_compatibility_score(
                        store_dna, partner
                    )
                    profitability = self.scoring_service.calculate_profitability_score(
                        store_dna, partner
                    )
                    recommendation = self.scoring_service.calculate_final_recommendation(
                        compatibility, profitability
                    )

                    if recommendation.final_score >= 0.4:  # Filtro mais permissivo
                        stage_recommendations.append(recommendation)

                # Ordena por score
                stage_recommendations.sort(key=lambda x: x.final_score, reverse=True)
                priority_recommendations[stage.value] = stage_recommendations[:3]

        return priority_recommendations

    def generate_market_opportunities(self) -> Dict[str, Any]:
        """Gera análise de oportunidades de mercado"""
        all_stores = list(self.dna_service.stores_db.values())
        all_partners = list(self.partners_db.values())

        context = {
            "stores": all_stores,
            "partners": all_partners
        }

        return self.agent_orchestrator.market_agent.execute_action(context)

    def get_partner_performance_analysis(self, partner_id: str) -> Dict[str, Any]:
        """Analisa performance de um parceiro específico"""
        partner = self.partners_db.get(partner_id)
        if not partner:
            return {"error": f"Partner {partner_id} not found"}

        all_stores = list(self.dna_service.stores_db.values())
        context = {"stores": all_stores}

        partner_agent = self.agent_orchestrator.partner_agents.get(partner_id)
        if partner_agent:
            return partner_agent.execute_action(context)

        return {"error": f"Partner agent for {partner_id} not found"}

class OrionOrchestrator:
    """Orquestrador Central do Sistema Órion"""

    def __init__(self):
        self.dna_service = DNAService()
        self.scoring_service = ScoringService()
        self.recommendation_service = RecommendationService()
        self.agent_orchestrator = AgentOrchestrator()

    def onboard_store(self, store_data: Dict[str, Any]) -> Dict[str, Any]:
        """Faz onboarding completo de uma nova loja"""

        # 1. Cria DNA da loja
        store_dna = self.dna_service.create_store_dna(store_data)

        # 2. Registra agente mestre para a loja
        master_agent = self.agent_orchestrator.register_master_agent(store_dna.store_id)

        # 3. Análise inicial de maturidade
        maturity = self.dna_service.analyze_store_maturity(store_dna.store_id)

        # 4. Identifica gaps iniciais
        gaps = self.dna_service.identify_gaps(store_dna.store_id)

        # 5. Gera recomendações iniciais
        initial_recommendations = self.recommendation_service.get_recommendations_for_store(
            store_dna.store_id, limit=5
        )

        onboarding_result = {
            "store_id": store_dna.store_id,
            "onboarding_date": datetime.now(),
            "dna_created": True,
            "master_agent_id": master_agent.agent_id,
            "initial_maturity": maturity,
            "identified_gaps": gaps,
            "initial_recommendations": [
                {
                    "partner_id": rec.partner_id,
                    "score": rec.final_score,
                    "priority": rec.priority,
                    "reasoning": rec.reasoning
                }
                for rec in initial_recommendations
            ],
            "next_steps": [
                "Revisar recomendações iniciais",
                "Definir prioridades estratégicas",
                "Implementar soluções de alta prioridade"
            ]
        }

        return onboarding_result

    def run_full_analysis(self, store_id: str) -> Dict[str, Any]:
        """Executa análise completa de uma loja usando todos os agentes"""

        store_dna = self.dna_service.get_store_dna(store_id)
        if not store_dna:
            return {"error": f"Store {store_id} not found"}

        # Contexto para os agentes
        all_stores = list(self.dna_service.stores_db.values())
        all_partners = list(self.recommendation_service.partners_db.values())

        context = {
            "store_id": store_id,
            "stores": all_stores,
            "partners": all_partners
        }

        # Executa análise completa via agentes
        agent_results = self.agent_orchestrator.execute_full_analysis(context)

        # Gera recomendações atualizadas
        current_recommendations = self.recommendation_service.get_recommendations_for_store(
            store_id, limit=8
        )

        # Recomendações priorizadas por área
        priority_recommendations = self.recommendation_service.get_priority_recommendations(
            store_id
        )

        full_analysis = {
            "store_id": store_id,
            "analysis_date": datetime.now(),
            "agent_analysis": agent_results,
            "current_recommendations": [
                {
                    "partner_id": rec.partner_id,
                    "final_score": rec.final_score,
                    "priority": rec.priority,
                    "reasoning": rec.reasoning,
                    "estimated_roi": rec.estimated_roi,
                    "implementation_timeline": rec.implementation_timeline
                }
                for rec in current_recommendations
            ],
            "priority_recommendations_by_area": {
                area: [
                    {
                        "partner_id": rec.partner_id,
                        "final_score": rec.final_score,
                        "reasoning": rec.reasoning
                    }
                    for rec in recs
                ]
                for area, recs in priority_recommendations.items()
            },
            "summary": {
                "total_recommendations": len(current_recommendations),
                "high_priority_count": len([r for r in current_recommendations if r.priority == 1]),
                "areas_analyzed": len(priority_recommendations)
            }
        }

        return full_analysis

    def add_partner_to_ecosystem(self, partner_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona novo parceiro ao ecossistema"""

        partner = Partner(
            partner_id=partner_data["partner_id"],
            name=partner_data["name"],
            category=EcommerceStage(partner_data["category"]),
            subcategory=partner_data.get("subcategory", ""),
            description=partner_data.get("description", ""),
            pricing_model=partner_data.get("pricing_model", "fixed"),
            min_price=partner_data.get("min_price", 0),
            max_price=partner_data.get("max_price"),
            target_segments=[StoreSegment(s) for s in partner_data.get("target_segments", [])],
            target_sizes=[StoreSize(s) for s in partner_data.get("target_sizes", [])],
            integration_complexity=partner_data.get("integration_complexity", 5),
            roi_potential=partner_data.get("roi_potential", 5),
            commission_rate=partner_data.get("commission_rate", 0.1)
        )

        # Adiciona ao catálogo
        self.recommendation_service.add_partner(partner)

        # Analisa impacto no mercado
        market_impact = self._analyze_partner_market_impact(partner)

        return {
            "partner_id": partner.partner_id,
            "added_at": datetime.now(),
            "category": partner.category.value,
            "market_impact": market_impact,
            "status": "active"
        }

    def _analyze_partner_market_impact(self, partner: Partner) -> Dict[str, Any]:
        """Analisa impacto de um novo parceiro no mercado"""
        all_stores = list(self.dna_service.stores_db.values())

        potential_matches = 0
        high_compatibility_stores = []

        for store_dna in all_stores:
            compatibility = self.scoring_service.calculate_compatibility_score(
                store_dna, partner
            )

            if compatibility.total_score >= 0.6:
                potential_matches += 1

            if compatibility.total_score >= 0.8:
                high_compatibility_stores.append({
                    "store_id": store_dna.store_id,
                    "store_name": store_dna.name,
                    "compatibility_score": compatibility.total_score
                })

        return {
            "total_stores_analyzed": len(all_stores),
            "potential_matches": potential_matches,
            "match_percentage": (potential_matches / len(all_stores)) * 100 if all_stores else 0,
            "high_compatibility_stores": high_compatibility_stores,
            "market_opportunity": "high" if potential_matches > len(all_stores) * 0.3 else "medium"
        }

    def get_ecosystem_dashboard(self) -> Dict[str, Any]:
        """Gera dashboard do ecossistema completo"""

        all_stores = list(self.dna_service.stores_db.values())
        all_partners = list(self.recommendation_service.partners_db.values())

        # Estatísticas básicas
        total_revenue = sum(store.monthly_revenue for store in all_stores)
        avg_conversion = sum(store.conversion_rate for store in all_stores) / len(all_stores) if all_stores else 0

        # Distribuições
        segment_dist = {}
        size_dist = {}
        for store in all_stores:
            segment_dist[store.segment.value] = segment_dist.get(store.segment.value, 0) + 1
            size_dist[store.size.value] = size_dist.get(store.size.value, 0) + 1

        partner_category_dist = {}
        for partner in all_partners:
            cat = partner.category.value
            partner_category_dist[cat] = partner_category_dist.get(cat, 0) + 1

        return {
            "ecosystem_overview": {
                "total_stores": len(all_stores),
                "total_partners": len(all_partners),
                "total_monthly_revenue": total_revenue,
                "average_conversion_rate": avg_conversion,
                "last_updated": datetime.now()
            },
            "store_distribution": {
                "by_segment": segment_dist,
                "by_size": size_dist
            },
            "partner_distribution": {
                "by_category": partner_category_dist
            },
            "health_metrics": {
                "stores_with_recommendations": len([s for s in all_stores if s.store_id in self.dna_service.stores_db]),
                "active_agents": len(self.agent_orchestrator.agents),
                "ecosystem_maturity": "growing" if len(all_stores) < 100 else "mature"
            }
        }
