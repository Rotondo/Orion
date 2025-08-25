
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from ..models.entities import StoreDNA, Partner, EcommerceStage
from ..services.dna_service import DNAService
from ..services.scoring_service import ScoringService

class BaseAgent(ABC):
    """Classe base para todos os agentes"""

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.created_at = datetime.now()
        self.last_action = None

    @abstractmethod
    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma ação baseada no contexto"""
        pass

    def log_action(self, action: str, details: Dict[str, Any]):
        """Registra ação executada"""
        self.last_action = {
            "action": action,
            "details": details,
            "timestamp": datetime.now()
        }

class MasterStoreAgent(BaseAgent):
    """Agente Mestre da Loja - orquestra ações para uma loja específica"""

    def __init__(self, store_id: str):
        super().__init__(f"master_{store_id}", f"Master Agent - Store {store_id}")
        self.store_id = store_id
        self.dna_service = DNAService()
        self.scoring_service = ScoringService()

    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Orquestra análise completa da loja"""
        store_dna = self.dna_service.get_store_dna(self.store_id)

        if not store_dna:
            return {"error": f"Store DNA not found for {self.store_id}"}

        # Analisa maturidade atual
        maturity = self.dna_service.analyze_store_maturity(self.store_id)

        # Identifica gaps
        gaps = self.dna_service.identify_gaps(self.store_id)

        # Gera insights
        insights = self._generate_insights(store_dna, maturity, gaps)

        result = {
            "agent_id": self.agent_id,
            "store_id": self.store_id,
            "maturity_analysis": maturity,
            "identified_gaps": gaps,
            "insights": insights,
            "recommendations": self._generate_recommendations(gaps),
            "analyzed_at": datetime.now()
        }

        self.log_action("full_store_analysis", result)
        return result

    def _generate_insights(self, dna: StoreDNA, maturity: Dict, gaps: List) -> List[str]:
        """Gera insights baseados na análise"""
        insights = []

        # Insights baseados no faturamento
        if dna.monthly_revenue > 50000:
            insights.append("Loja com faturamento significativo - foco em otimização")
        else:
            insights.append("Loja em crescimento - foco em ferramentas de escala")

        # Insights baseados na conversão
        if dna.conversion_rate < 0.02:
            insights.append("Taxa de conversão abaixo da média - priorizar CRO")
        elif dna.conversion_rate > 0.04:
            insights.append("Excelente taxa de conversão - focar em aumento de tráfego")

        # Insights baseados nos gaps
        if len(gaps) > 5:
            insights.append("Múltiplas oportunidades de melhoria identificadas")

        return insights

    def _generate_recommendations(self, gaps: List) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas nos gaps"""
        recommendations = []

        for gap in gaps[:3]:  # Top 3 gaps
            recommendations.append({
                "stage": gap["stage"],
                "action": f"Implementar solução para {gap['stage']}",
                "priority": gap["gap_severity"],
                "expected_impact": "Melhoria na operação e resultados"
            })

        return recommendations

class SpecialistAgent(BaseAgent):
    """Agente Especialista - focado em uma área específica do e-commerce"""

    def __init__(self, stage: EcommerceStage, agent_id: str = None):
        if not agent_id:
            agent_id = f"specialist_{stage.value}"
        super().__init__(agent_id, f"Specialist Agent - {stage.value}")
        self.specialty = stage

    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa área específica e sugere melhorias"""
        store_id = context.get("store_id")
        partners = context.get("partners", [])

        # Filtra parceiros da sua especialidade
        relevant_partners = [
            p for p in partners 
            if p.category == self.specialty
        ]

        analysis = {
            "agent_id": self.agent_id,
            "specialty": self.specialty.value,
            "store_id": store_id,
            "relevant_partners_count": len(relevant_partners),
            "top_recommendations": []
        }

        # Simula análise especializada
        if relevant_partners:
            # Ordena por ROI potencial
            sorted_partners = sorted(
                relevant_partners, 
                key=lambda x: x.roi_potential, 
                reverse=True
            )

            for partner in sorted_partners[:3]:  # Top 3
                analysis["top_recommendations"].append({
                    "partner_id": partner.partner_id,
                    "partner_name": partner.name,
                    "roi_potential": partner.roi_potential,
                    "why_recommended": self._get_recommendation_reason(partner)
                })

        self.log_action("specialist_analysis", analysis)
        return analysis

    def _get_recommendation_reason(self, partner: Partner) -> str:
        """Gera razão para recomendação"""
        reasons = [
            f"Alto ROI potencial ({partner.roi_potential}/10)",
            f"Baixa complexidade de integração ({11-partner.integration_complexity}/10)",
            f"Modelo de pricing favorável ({partner.pricing_model})"
        ]
        return random.choice(reasons)

class PartnerAgent(BaseAgent):
    """Agente de Parceiro - representa conhecimento sobre soluções de um parceiro"""

    def __init__(self, partner: Partner):
        super().__init__(f"partner_{partner.partner_id}", f"Partner Agent - {partner.name}")
        self.partner = partner

    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia adequação do parceiro para lojas específicas"""
        stores = context.get("stores", [])
        scoring_service = ScoringService()

        evaluations = []

        for store_dna in stores:
            compatibility = scoring_service.calculate_compatibility_score(
                store_dna, self.partner
            )

            evaluation = {
                "store_id": store_dna.store_id,
                "store_name": store_dna.name,
                "compatibility_score": compatibility.total_score,
                "fit_level": self._determine_fit_level(compatibility.total_score),
                "key_matches": []
            }

            # Adiciona detalhes dos matches
            if compatibility.segment_match > 0.8:
                evaluation["key_matches"].append("Segmento ideal")
            if compatibility.size_match > 0.8:
                evaluation["key_matches"].append("Tamanho adequado")

            evaluations.append(evaluation)

        result = {
            "agent_id": self.agent_id,
            "partner_id": self.partner.partner_id,
            "partner_name": self.partner.name,
            "evaluations": evaluations,
            "summary": {
                "total_stores_analyzed": len(stores),
                "high_fit_stores": len([e for e in evaluations if e["fit_level"] == "high"]),
                "medium_fit_stores": len([e for e in evaluations if e["fit_level"] == "medium"])
            }
        }

        self.log_action("partner_evaluation", result)
        return result

    def _determine_fit_level(self, score: float) -> str:
        """Determina nível de adequação"""
        if score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"

class MarketIntelligenceAgent(BaseAgent):
    """Agente de Inteligência de Mercado - analisa o ecossistema como um todo"""

    def __init__(self):
        super().__init__("market_intelligence", "Market Intelligence Agent")

    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tendências e oportunidades de mercado"""
        stores = context.get("stores", [])
        partners = context.get("partners", [])

        # Análise de mercado
        market_analysis = {
            "agent_id": self.agent_id,
            "market_overview": {
                "total_stores": len(stores),
                "total_partners": len(partners),
                "analysis_date": datetime.now()
            },
            "segment_distribution": self._analyze_segment_distribution(stores),
            "size_distribution": self._analyze_size_distribution(stores),
            "partner_coverage": self._analyze_partner_coverage(partners),
            "market_gaps": self._identify_market_gaps(stores, partners),
            "growth_opportunities": self._identify_growth_opportunities(stores)
        }

        self.log_action("market_analysis", market_analysis)
        return market_analysis

    def _analyze_segment_distribution(self, stores: List[StoreDNA]) -> Dict[str, int]:
        """Analisa distribuição por segmento"""
        distribution = {}
        for store in stores:
            segment = store.segment.value
            distribution[segment] = distribution.get(segment, 0) + 1
        return distribution

    def _analyze_size_distribution(self, stores: List[StoreDNA]) -> Dict[str, int]:
        """Analisa distribuição por tamanho"""
        distribution = {}
        for store in stores:
            size = store.size.value
            distribution[size] = distribution.get(size, 0) + 1
        return distribution

    def _analyze_partner_coverage(self, partners: List[Partner]) -> Dict[str, int]:
        """Analisa cobertura de parceiros por categoria"""
        coverage = {}
        for partner in partners:
            category = partner.category.value
            coverage[category] = coverage.get(category, 0) + 1
        return coverage

    def _identify_market_gaps(self, stores: List[StoreDNA], partners: List[Partner]) -> List[str]:
        """Identifica lacunas no mercado"""
        gaps = []

        # Verifica se há categorias com poucos parceiros
        coverage = self._analyze_partner_coverage(partners)
        total_partners = len(partners)

        for stage in EcommerceStage:
            stage_partners = coverage.get(stage.value, 0)
            if stage_partners < total_partners * 0.1:  # Menos de 10% dos parceiros
                gaps.append(f"Poucos parceiros na categoria {stage.value}")

        return gaps

    def _identify_growth_opportunities(self, stores: List[StoreDNA]) -> List[Dict[str, Any]]:
        """Identifica oportunidades de crescimento"""
        opportunities = []

        # Analisa stores com alto potencial
        high_revenue_stores = [s for s in stores if s.monthly_revenue > 50000]
        low_conversion_stores = [s for s in stores if s.conversion_rate < 0.02]

        if high_revenue_stores:
            opportunities.append({
                "type": "premium_services",
                "description": f"{len(high_revenue_stores)} lojas com alto faturamento para serviços premium",
                "potential_stores": len(high_revenue_stores)
            })

        if low_conversion_stores:
            opportunities.append({
                "type": "conversion_optimization", 
                "description": f"{len(low_conversion_stores)} lojas com baixa conversão para CRO",
                "potential_stores": len(low_conversion_stores)
            })

        return opportunities

class AgentOrchestrator:
    """Orquestrador dos agentes - coordena ações dos diferentes agentes"""

    def __init__(self):
        self.agents = {}
        self.master_agents = {}  # Por store_id
        self.specialist_agents = {}  # Por especialidade
        self.partner_agents = {}  # Por partner_id
        self.market_agent = MarketIntelligenceAgent()

    def register_master_agent(self, store_id: str) -> MasterStoreAgent:
        """Registra agente mestre para uma loja"""
        agent = MasterStoreAgent(store_id)
        self.master_agents[store_id] = agent
        self.agents[agent.agent_id] = agent
        return agent

    def register_specialist_agent(self, stage: EcommerceStage) -> SpecialistAgent:
        """Registra agente especialista"""
        agent = SpecialistAgent(stage)
        self.specialist_agents[stage.value] = agent
        self.agents[agent.agent_id] = agent
        return agent

    def register_partner_agent(self, partner: Partner) -> PartnerAgent:
        """Registra agente de parceiro"""
        agent = PartnerAgent(partner)
        self.partner_agents[partner.partner_id] = agent
        self.agents[agent.agent_id] = agent
        return agent

    def execute_full_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise completa usando todos os agentes"""
        results = {
            "orchestration_id": f"orch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "executed_at": datetime.now(),
            "master_agent_results": {},
            "specialist_results": {},
            "partner_results": {},
            "market_intelligence": {}
        }

        # Executa agentes mestres
        for store_id, agent in self.master_agents.items():
            results["master_agent_results"][store_id] = agent.execute_action(context)

        # Executa agentes especialistas
        for specialty, agent in self.specialist_agents.items():
            results["specialist_results"][specialty] = agent.execute_action(context)

        # Executa agentes de parceiros
        for partner_id, agent in self.partner_agents.items():
            results["partner_results"][partner_id] = agent.execute_action(context)

        # Executa inteligência de mercado
        results["market_intelligence"] = self.market_agent.execute_action(context)

        return results
