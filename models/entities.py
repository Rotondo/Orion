
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

class StoreSize(Enum):
    MICRO = "micro"
    PEQUENA = "pequena" 
    MEDIA = "media"
    GRANDE = "grande"

class StoreSegment(Enum):
    FASHION = "fashion"
    ELETRONICOS = "eletronicos"
    CASA_JARDIM = "casa_jardim"
    SAUDE_BELEZA = "saude_beleza"
    ESPORTES = "esportes"
    LIVROS = "livros"

class EcommerceStage(Enum):
    ATRACAO = "1_atracao"
    INFRAESTRUTURA = "2_infraestrutura" 
    NAVEGACAO = "3_navegacao"
    PRODUTO = "4_produto"
    CARRINHO = "5_carrinho"
    PAGAMENTO = "6_pagamento"
    FULFILLMENT = "7_fulfillment"
    ENTREGA = "8_entrega"
    POS_VENDA = "9_pos_venda"
    ANALYTICS = "10_analytics"
    COMPLIANCE = "11_compliance"
    TALENTOS = "12_talentos"

@dataclass
class StoreDNA:
    """Modelo do DNA da Loja - informações cadastrais e performance"""
    store_id: str
    name: str
    segment: StoreSegment
    size: StoreSize
    monthly_revenue: float
    monthly_orders: int
    avg_ticket: float
    conversion_rate: float
    traffic_sources: Dict[str, float]  # {"organic": 0.3, "paid": 0.4, ...}
    pain_points: List[str]
    current_tools: List[str]
    priorities: Dict[EcommerceStage, int]  # peso de 1-10 para cada etapa
    created_at: datetime
    updated_at: datetime

@dataclass 
class Partner:
    """Modelo de Parceiro/Fornecedor de soluções"""
    partner_id: str
    name: str
    category: EcommerceStage
    subcategory: str
    description: str
    pricing_model: str  # "fixed", "percentage", "per_transaction"
    min_price: float
    max_price: Optional[float]
    target_segments: List[StoreSegment]
    target_sizes: List[StoreSize]
    integration_complexity: int  # 1-10
    roi_potential: int  # 1-10
    commission_rate: float

@dataclass
class CompatibilityScore:
    """Score de compatibilidade entre loja e parceiro"""
    store_id: str
    partner_id: str
    segment_match: float
    size_match: float
    pain_point_match: float
    priority_match: float
    total_score: float
    calculated_at: datetime

@dataclass
class ProfitabilityScore:
    """Score de rentabilidade para a plataforma"""
    store_id: str
    partner_id: str
    commission_potential: float
    implementation_cost: float
    retention_probability: float
    total_score: float
    calculated_at: datetime

@dataclass
class FinalRecommendation:
    """Recomendação final combinando compatibilidade e rentabilidade"""
    store_id: str
    partner_id: str
    compatibility_score: float
    profitability_score: float
    final_score: float
    reasoning: List[str]
    priority: int  # 1=alta, 2=media, 3=baixa
    estimated_roi: float
    implementation_timeline: str
    created_at: datetime
