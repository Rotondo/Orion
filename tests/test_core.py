
import pytest
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.entities import StoreDNA, Partner, StoreSegment, StoreSize, EcommerceStage
from services.dna_service import DNAService
from services.scoring_service import ScoringService
from services.recommendation_service import OrionOrchestrator
from core.sample_data import create_sample_data

class TestDNAService:
    """Testa serviço de DNA da loja"""

    def test_create_store_dna(self):
        dna_service = DNAService()

        store_data = {
            "store_id": "test_store_001",
            "name": "Test Store",
            "segment": "fashion",
            "size": "pequena",
            "monthly_revenue": 10000,
            "monthly_orders": 100,
            "avg_ticket": 100,
            "conversion_rate": 0.02
        }

        dna = dna_service.create_store_dna(store_data)

        assert dna.store_id == "test_store_001"
        assert dna.name == "Test Store"
        assert dna.segment == StoreSegment.FASHION
        assert dna.size == StoreSize.PEQUENA
        assert dna.monthly_revenue == 10000

    def test_analyze_store_maturity(self):
        dna_service = DNAService()

        store_data = {
            "store_id": "test_store_002",
            "name": "Mature Store",
            "segment": "eletronicos",
            "size": "grande",
            "monthly_revenue": 150000,
            "monthly_orders": 500,
            "avg_ticket": 300,
            "conversion_rate": 0.035
        }

        dna_service.create_store_dna(store_data)
        maturity = dna_service.analyze_store_maturity("test_store_002")

        assert isinstance(maturity, dict)
        assert len(maturity) > 0
        for stage, score in maturity.items():
            assert 1 <= score <= 10

    def test_identify_gaps(self):
        dna_service = DNAService()

        store_data = {
            "store_id": "test_store_003", 
            "name": "Gap Store",
            "segment": "fashion",
            "size": "pequena",
            "monthly_revenue": 5000,
            "monthly_orders": 50,
            "avg_ticket": 100,
            "conversion_rate": 0.01  # Baixa conversão
        }

        dna_service.create_store_dna(store_data)
        gaps = dna_service.identify_gaps("test_store_003")

        assert isinstance(gaps, list)
        if gaps:
            assert "gap_severity" in gaps[0]
            assert "stage" in gaps[0]

class TestScoringService:
    """Testa serviço de scoring"""

    def setup_method(self):
        """Setup para cada teste"""
        self.scoring_service = ScoringService()

        # Store de exemplo
        self.store_dna = StoreDNA(
            store_id="test_store",
            name="Test Store",
            segment=StoreSegment.FASHION,
            size=StoreSize.PEQUENA,
            monthly_revenue=25000,
            monthly_orders=180,
            avg_ticket=138.89,
            conversion_rate=0.022,
            traffic_sources={"organic": 0.3, "paid": 0.7},
            pain_points=["baixa_conversao"],
            current_tools=["google_ads"],
            priorities={"1_atracao": 8},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Partner de exemplo
        self.partner = Partner(
            partner_id="test_partner",
            name="Test Partner",
            category=EcommerceStage.ATRACAO,
            subcategory="Ads",
            description="Test partner",
            pricing_model="percentage",
            min_price=500,
            max_price=2000,
            target_segments=[StoreSegment.FASHION],
            target_sizes=[StoreSize.PEQUENA],
            integration_complexity=3,
            roi_potential=8,
            commission_rate=0.15
        )

    def test_calculate_compatibility_score(self):
        compatibility = self.scoring_service.calculate_compatibility_score(
            self.store_dna, self.partner
        )

        assert compatibility.store_id == "test_store"
        assert compatibility.partner_id == "test_partner"
        assert 0 <= compatibility.total_score <= 1
        assert compatibility.segment_match == 1.0  # Match perfeito
        assert compatibility.size_match == 1.0     # Match perfeito

    def test_calculate_profitability_score(self):
        profitability = self.scoring_service.calculate_profitability_score(
            self.store_dna, self.partner
        )

        assert profitability.store_id == "test_store"
        assert profitability.partner_id == "test_partner"
        assert 0 <= profitability.total_score <= 1
        assert profitability.commission_potential > 0

    def test_calculate_final_recommendation(self):
        compatibility = self.scoring_service.calculate_compatibility_score(
            self.store_dna, self.partner
        )
        profitability = self.scoring_service.calculate_profitability_score(
            self.store_dna, self.partner
        )

        recommendation = self.scoring_service.calculate_final_recommendation(
            compatibility, profitability
        )

        assert recommendation.store_id == "test_store"
        assert recommendation.partner_id == "test_partner"
        assert 0 <= recommendation.final_score <= 1
        assert recommendation.priority in [1, 2, 3]
        assert isinstance(recommendation.reasoning, list)

class TestOrchestrator:
    """Testa orquestrador principal"""

    def test_onboard_store(self):
        orchestrator = OrionOrchestrator()

        store_data = {
            "store_id": "test_onboard_001",
            "name": "Onboard Test Store",
            "segment": "fashion",
            "size": "pequena",
            "monthly_revenue": 15000,
            "monthly_orders": 120,
            "avg_ticket": 125,
            "conversion_rate": 0.02
        }

        result = orchestrator.onboard_store(store_data)

        assert result["store_id"] == "test_onboard_001"
        assert result["dna_created"] is True
        assert "master_agent_id" in result
        assert "initial_maturity" in result
        assert "identified_gaps" in result
        assert "initial_recommendations" in result

    def test_ecosystem_dashboard(self):
        orchestrator = OrionOrchestrator()

        # Adiciona dados de exemplo
        create_sample_data(orchestrator)

        dashboard = orchestrator.get_ecosystem_dashboard()

        assert "ecosystem_overview" in dashboard
        assert "store_distribution" in dashboard
        assert "partner_distribution" in dashboard
        assert "health_metrics" in dashboard

        # Verifica se tem dados
        assert dashboard["ecosystem_overview"]["total_stores"] > 0
        assert dashboard["ecosystem_overview"]["total_partners"] > 0

if __name__ == "__main__":
    pytest.main([__file__])
