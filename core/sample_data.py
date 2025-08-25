
from datetime import datetime
from models.entities import StoreSegment, StoreSize, EcommerceStage

def create_sample_data(orchestrator):
    """Cria dados de exemplo para demonstração do sistema"""

    # Lojas de exemplo
    sample_stores = [
        {
            "store_id": "loja_fashion_001",
            "name": "Moda & Estilo Boutique",
            "segment": "fashion",
            "size": "pequena",
            "monthly_revenue": 25000,
            "monthly_orders": 180,
            "avg_ticket": 138.89,
            "conversion_rate": 0.022,
            "traffic_sources": {"organic": 0.3, "paid": 0.5, "social": 0.2},
            "pain_points": ["baixa_conversao", "alto_cac", "abandono_carrinho"],
            "current_tools": ["google_ads", "facebook_ads", "hotjar"],
            "priorities": {
                "1_atracao": 8,
                "3_navegacao": 9,
                "5_carrinho": 7,
                "9_pos_venda": 6
            }
        },
        {
            "store_id": "loja_eletronicos_002", 
            "name": "TechMaster Electronics",
            "segment": "eletronicos",
            "size": "media",
            "monthly_revenue": 85000,
            "monthly_orders": 320,
            "avg_ticket": 265.63,
            "conversion_rate": 0.031,
            "traffic_sources": {"organic": 0.45, "paid": 0.35, "direct": 0.2},
            "pain_points": ["logistica_cara", "atendimento", "gestao_estoque"],
            "current_tools": ["google_analytics", "bling_erp", "mercado_envios"],
            "priorities": {
                "7_fulfillment": 9,
                "8_entrega": 8,
                "9_pos_venda": 7,
                "10_analytics": 6
            }
        },
        {
            "store_id": "loja_casa_003",
            "name": "Casa & Decoração Premium",
            "segment": "casa_jardim",
            "size": "grande",
            "monthly_revenue": 180000,
            "monthly_orders": 450,
            "avg_ticket": 400.00,
            "conversion_rate": 0.028,
            "traffic_sources": {"organic": 0.6, "paid": 0.25, "social": 0.15},
            "pain_points": ["mobile_experience", "personalizacao", "upsell"],
            "current_tools": ["vtex", "google_ads", "zendesk", "mailchimp"],
            "priorities": {
                "2_infraestrutura": 7,
                "3_navegacao": 9,
                "4_produto": 8,
                "10_analytics": 8
            }
        },
        {
            "store_id": "loja_saude_004",
            "name": "Vida Saudável Suplementos",
            "segment": "saude_beleza",
            "size": "pequena",
            "monthly_revenue": 15000,
            "monthly_orders": 95,
            "avg_ticket": 157.89,
            "conversion_rate": 0.018,
            "traffic_sources": {"organic": 0.2, "paid": 0.6, "influencer": 0.2},
            "pain_points": ["conversao_baixa", "carrinho_abandono", "seo"],
            "current_tools": ["shopify", "facebook_ads", "instagram"],
            "priorities": {
                "1_atracao": 9,
                "3_navegacao": 8,
                "5_carrinho": 9,
                "6_pagamento": 6
            }
        }
    ]

    # Parceiros de exemplo
    sample_partners = [
        {
            "partner_id": "partner_ads_001",
            "name": "AdOptimizer Pro",
            "category": "1_atracao",
            "subcategory": "Gestão de Ads",
            "description": "Plataforma de otimização automática de campanhas Google e Meta Ads",
            "pricing_model": "percentage",
            "min_price": 500,
            "max_price": 5000,
            "target_segments": ["fashion", "eletronicos", "saude_beleza"],
            "target_sizes": ["pequena", "media"],
            "integration_complexity": 3,
            "roi_potential": 8,
            "commission_rate": 0.15
        },
        {
            "partner_id": "partner_search_002",
            "name": "SmartSearch AI",
            "category": "3_navegacao",
            "subcategory": "Busca Inteligente",
            "description": "Motor de busca com IA e recomendações personalizadas",
            "pricing_model": "fixed",
            "min_price": 299,
            "max_price": 1299,
            "target_segments": ["fashion", "casa_jardim", "eletronicos"],
            "target_sizes": ["media", "grande"],
            "integration_complexity": 4,
            "roi_potential": 7,
            "commission_rate": 0.20
        },
        {
            "partner_id": "partner_checkout_003",
            "name": "ConvertMax Checkout",
            "category": "5_carrinho",
            "subcategory": "Otimização de Checkout",
            "description": "Checkout otimizado com A/B test automático e recuperação de carrinho",
            "pricing_model": "per_transaction",
            "min_price": 0.50,
            "max_price": 2.00,
            "target_segments": ["fashion", "saude_beleza", "eletronicos"],
            "target_sizes": ["pequena", "media", "grande"],
            "integration_complexity": 2,
            "roi_potential": 9,
            "commission_rate": 0.25
        },
        {
            "partner_id": "partner_payment_004",
            "name": "PayFlow Gateway",
            "category": "6_pagamento",
            "subcategory": "Gateway de Pagamento",
            "description": "Gateway com melhores taxas e múltiplos meios de pagamento",
            "pricing_model": "percentage",
            "min_price": 0,
            "target_segments": ["fashion", "eletronicos", "casa_jardim", "saude_beleza"],
            "target_sizes": ["pequena", "media", "grande"],
            "integration_complexity": 3,
            "roi_potential": 6,
            "commission_rate": 0.10
        },
        {
            "partner_id": "partner_logistics_005",
            "name": "LogiSmart Fulfillment",
            "category": "7_fulfillment", 
            "subcategory": "Gestão de Estoque",
            "description": "Sistema WMS com previsão de demanda por IA",
            "pricing_model": "fixed",
            "min_price": 899,
            "max_price": 3999,
            "target_segments": ["eletronicos", "casa_jardim"],
            "target_sizes": ["media", "grande"],
            "integration_complexity": 6,
            "roi_potential": 8,
            "commission_rate": 0.12
        },
        {
            "partner_id": "partner_shipping_006",
            "name": "ExpressFrete",
            "category": "8_entrega",
            "subcategory": "Gestão de Frete",
            "description": "Plataforma multi-transportadora com otimização de rotas",
            "pricing_model": "percentage",
            "min_price": 0,
            "target_segments": ["fashion", "eletronicos", "casa_jardim", "saude_beleza"],
            "target_sizes": ["pequena", "media", "grande"],
            "integration_complexity": 4,
            "roi_potential": 7,
            "commission_rate": 0.08
        },
        {
            "partner_id": "partner_crm_007",
            "name": "CustomerCare 360",
            "category": "9_pos_venda",
            "subcategory": "CRM Omnichannel",
            "description": "CRM com automação de marketing e customer success",
            "pricing_model": "fixed",
            "min_price": 199,
            "max_price": 1499,
            "target_segments": ["fashion", "saude_beleza", "casa_jardim"],
            "target_sizes": ["pequena", "media", "grande"],
            "integration_complexity": 5,
            "roi_potential": 7,
            "commission_rate": 0.18
        },
        {
            "partner_id": "partner_analytics_008",
            "name": "DataInsights Pro",
            "category": "10_analytics",
            "subcategory": "Business Intelligence",
            "description": "Dashboard BI com análises preditivas e KPIs automatizados",
            "pricing_model": "fixed",
            "min_price": 399,
            "max_price": 1999,
            "target_segments": ["eletronicos", "casa_jardim"],
            "target_sizes": ["media", "grande"],
            "integration_complexity": 4,
            "roi_potential": 8,
            "commission_rate": 0.22
        }
    ]

    # Cria lojas
    stores_created = []
    for store_data in sample_stores:
        result = orchestrator.onboard_store(store_data)
        stores_created.append(result["store_id"])

    # Cria parceiros
    partners_created = []
    for partner_data in sample_partners:
        result = orchestrator.add_partner_to_ecosystem(partner_data)
        partners_created.append(result["partner_id"])

    return {
        "stores_created": stores_created,
        "partners_created": partners_created,
        "sample_data_loaded_at": datetime.now(),
        "message": "Dados de exemplo carregados com sucesso!"
    }
