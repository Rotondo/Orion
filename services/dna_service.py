
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
from ..models.entities import StoreDNA, StoreSize, StoreSegment, EcommerceStage

class DNAService:
    """Serviço responsável por gerenciar o DNA das lojas"""

    def __init__(self):
        self.stores_db = {}  # Simulação de banco de dados

    def create_store_dna(self, store_data: Dict) -> StoreDNA:
        """Cria o DNA inicial de uma loja"""
        dna = StoreDNA(
            store_id=store_data["store_id"],
            name=store_data["name"],
            segment=StoreSegment(store_data["segment"]),
            size=StoreSize(store_data["size"]),
            monthly_revenue=store_data.get("monthly_revenue", 0),
            monthly_orders=store_data.get("monthly_orders", 0),
            avg_ticket=store_data.get("avg_ticket", 0),
            conversion_rate=store_data.get("conversion_rate", 0.02),
            traffic_sources=store_data.get("traffic_sources", {"organic": 0.4, "paid": 0.6}),
            pain_points=store_data.get("pain_points", []),
            current_tools=store_data.get("current_tools", []),
            priorities=store_data.get("priorities", {}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.stores_db[dna.store_id] = dna
        return dna

    def get_store_dna(self, store_id: str) -> Optional[StoreDNA]:
        """Recupera o DNA de uma loja"""
        return self.stores_db.get(store_id)

    def update_store_dna(self, store_id: str, updates: Dict) -> Optional[StoreDNA]:
        """Atualiza o DNA de uma loja"""
        if store_id in self.stores_db:
            dna = self.stores_db[store_id]
            for key, value in updates.items():
                if hasattr(dna, key):
                    setattr(dna, key, value)
            dna.updated_at = datetime.now()
            return dna
        return None

    def analyze_store_maturity(self, store_id: str) -> Dict[str, Any]:
        """Analisa a maturidade da loja em cada etapa do e-commerce"""
        dna = self.get_store_dna(store_id)
        if not dna:
            return {}

        # Algoritmo simplificado de análise de maturidade
        maturity = {}

        # Baseado no faturamento e conversão
        if dna.monthly_revenue > 100000:  # R$ 100k+
            base_maturity = 7
        elif dna.monthly_revenue > 50000:  # R$ 50k+
            base_maturity = 5
        elif dna.monthly_revenue > 10000:  # R$ 10k+
            base_maturity = 3
        else:
            base_maturity = 1

        # Ajusta baseado na conversão
        if dna.conversion_rate > 0.03:
            base_maturity += 1
        elif dna.conversion_rate < 0.01:
            base_maturity -= 1

        for stage in EcommerceStage:
            # Varia a maturidade por etapa
            stage_maturity = base_maturity + random.randint(-2, 2)
            maturity[stage.value] = max(1, min(10, stage_maturity))

        return maturity

    def identify_gaps(self, store_id: str) -> List[Dict[str, Any]]:
        """Identifica lacunas nas ferramentas da loja"""
        dna = self.get_store_dna(store_id)
        maturity = self.analyze_store_maturity(store_id)

        if not dna:
            return []

        gaps = []

        # Identifica etapas com baixa maturidade como gaps
        for stage, score in maturity.items():
            if score < 5:
                gaps.append({
                    "stage": stage,
                    "current_score": score,
                    "gap_severity": "alta" if score < 3 else "média",
                    "suggested_priority": 10 - score
                })

        return sorted(gaps, key=lambda x: x["suggested_priority"], reverse=True)
