
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.entities import StoreSegment, StoreSize, EcommerceStage
from services.recommendation_service import OrionOrchestrator

app = FastAPI(
    title="Projeto Órion - API",
    description="API do Sistema Inteligente de Orquestração de E-commerce",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do orquestrador
orchestrator = OrionOrchestrator()

# Modelos Pydantic para requests
class StoreCreateRequest(BaseModel):
    store_id: str
    name: str
    segment: str
    size: str
    monthly_revenue: float = 0
    monthly_orders: int = 0
    avg_ticket: float = 0
    conversion_rate: float = 0.02
    traffic_sources: Dict[str, float] = {"organic": 0.4, "paid": 0.6}
    pain_points: List[str] = []
    current_tools: List[str] = []
    priorities: Dict[str, int] = {}

class PartnerCreateRequest(BaseModel):
    partner_id: str
    name: str
    category: str
    subcategory: str = ""
    description: str = ""
    pricing_model: str = "fixed"
    min_price: float = 0
    max_price: Optional[float] = None
    target_segments: List[str] = []
    target_sizes: List[str] = []
    integration_complexity: int = 5
    roi_potential: int = 5
    commission_rate: float = 0.1

# Endpoints principais

@app.get("/")
async def root():
    return {
        "message": "Projeto Órion - Sistema de Orquestração de E-commerce", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/stores")
async def create_store(store_data: StoreCreateRequest):
    """Cria uma nova loja no sistema"""
    try:
        result = orchestrator.onboard_store(store_data.dict())
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stores/{store_id}")
async def get_store(store_id: str):
    """Recupera informações de uma loja"""
    store_dna = orchestrator.dna_service.get_store_dna(store_id)
    if not store_dna:
        raise HTTPException(status_code=404, detail="Store not found")

    # Converte dataclass para dict
    store_data = {
        "store_id": store_dna.store_id,
        "name": store_dna.name,
        "segment": store_dna.segment.value,
        "size": store_dna.size.value,
        "monthly_revenue": store_dna.monthly_revenue,
        "monthly_orders": store_dna.monthly_orders,
        "avg_ticket": store_dna.avg_ticket,
        "conversion_rate": store_dna.conversion_rate,
        "traffic_sources": store_dna.traffic_sources,
        "pain_points": store_dna.pain_points,
        "current_tools": store_dna.current_tools,
        "priorities": store_dna.priorities,
        "created_at": store_dna.created_at.isoformat(),
        "updated_at": store_dna.updated_at.isoformat()
    }

    return {"success": True, "data": store_data}

@app.get("/stores/{store_id}/analysis")
async def analyze_store(store_id: str):
    """Executa análise completa de uma loja"""
    try:
        result = orchestrator.run_full_analysis(store_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stores/{store_id}/recommendations")
async def get_store_recommendations(
    store_id: str, 
    limit: int = 10, 
    min_score: float = 0.3
):
    """Obtém recomendações para uma loja"""
    try:
        recommendations = orchestrator.recommendation_service.get_recommendations_for_store(
            store_id, limit, min_score
        )

        # Converte para dict
        recs_data = [
            {
                "partner_id": rec.partner_id,
                "compatibility_score": rec.compatibility_score,
                "profitability_score": rec.profitability_score,
                "final_score": rec.final_score,
                "priority": rec.priority,
                "reasoning": rec.reasoning,
                "estimated_roi": rec.estimated_roi,
                "implementation_timeline": rec.implementation_timeline,
                "created_at": rec.created_at.isoformat()
            }
            for rec in recommendations
        ]

        return {"success": True, "data": recs_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stores/{store_id}/gaps")
async def get_store_gaps(store_id: str):
    """Identifica gaps/lacunas de uma loja"""
    try:
        gaps = orchestrator.dna_service.identify_gaps(store_id)
        maturity = orchestrator.dna_service.analyze_store_maturity(store_id)

        return {
            "success": True, 
            "data": {
                "gaps": gaps,
                "maturity_analysis": maturity
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/partners")
async def create_partner(partner_data: PartnerCreateRequest):
    """Adiciona novo parceiro ao ecossistema"""
    try:
        result = orchestrator.add_partner_to_ecosystem(partner_data.dict())
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/partners/{partner_id}/analysis")
async def analyze_partner(partner_id: str):
    """Analisa performance de um parceiro"""
    try:
        result = orchestrator.recommendation_service.get_partner_performance_analysis(partner_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ecosystem/dashboard")
async def get_ecosystem_dashboard():
    """Dashboard do ecossistema completo"""
    try:
        dashboard = orchestrator.get_ecosystem_dashboard()
        return {"success": True, "data": dashboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/opportunities")
async def get_market_opportunities():
    """Análise de oportunidades de mercado"""
    try:
        opportunities = orchestrator.recommendation_service.generate_market_opportunities()
        return {"success": True, "data": opportunities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/enums")
async def get_enums():
    """Retorna enums disponíveis para facilitar frontend"""
    return {
        "success": True,
        "data": {
            "store_segments": [seg.value for seg in StoreSegment],
            "store_sizes": [size.value for size in StoreSize],
            "ecommerce_stages": [stage.value for stage in EcommerceStage]
        }
    }

# Endpoint para popular dados de exemplo
@app.post("/seed-data")
async def seed_example_data():
    """Popula sistema com dados de exemplo para demonstração"""
    try:
        from ..core.sample_data import create_sample_data
        result = create_sample_data(orchestrator)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
