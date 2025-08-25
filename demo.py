#!/usr/bin/env python3
"""
Script de Demonstração do Projeto Órion
Mostra as funcionalidades principais do sistema em ação
"""

import json
import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(__file__))

from services.recommendation_service import OrionOrchestrator
from core.sample_data import create_sample_data

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_section(title):
    """Imprime seção formatada"""
    print(f"\n📋 {title}")
    print("-"*40)

def print_json(data, max_items=3):
    """Imprime JSON formatado com limite de items"""
    if isinstance(data, list) and len(data) > max_items:
        print(f"Showing top {max_items} of {len(data)} items:")
        data = data[:max_items]
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))

def run_orion_demo():
    """Executa demonstração completa do Sistema Órion"""

    print_header("PROJETO ÓRION - DEMONSTRAÇÃO COMPLETA")
    print("Sistema Inteligente de Orquestração de E-commerce")
    print("Autor: Manus AI | Data: 25 de Agosto de 2025")

    # 1. Inicializa o sistema
    print_section("1. Inicializando Sistema Órion")
    orchestrator = OrionOrchestrator()
    print("✅ Orquestrador principal inicializado")
    print("✅ Serviços de DNA, Scoring e Recomendações ativos")
    print("✅ Rede de Agentes Autônomos configurada")

    # 2. Popula dados de exemplo
    print_section("2. Carregando Dados de Exemplo")
    sample_result = create_sample_data(orchestrator)
    print(f"✅ {len(sample_result['stores_created'])} lojas de exemplo criadas")
    print(f"✅ {len(sample_result['partners_created'])} parceiros adicionados ao ecossistema")

    print("\n📊 Lojas criadas:")
    for store_id in sample_result['stores_created']:
        store = orchestrator.dna_service.get_store_dna(store_id)
        print(f"  • {store.name} ({store.segment.value}, {store.size.value}) - R$ {store.monthly_revenue:,.2f}/mês")

    print("\n🤝 Parceiros adicionados:")
    for partner_id in sample_result['partners_created']:
        partner = orchestrator.recommendation_service.partners_db.get(partner_id)
        print(f"  • {partner.name} ({partner.category.value}) - ROI: {partner.roi_potential}/10")

    # 3. Análise de loja específica
    print_section("3. Análise Completa - Loja Fashion")
    store_id = "loja_fashion_001"

    # DNA da loja
    store_dna = orchestrator.dna_service.get_store_dna(store_id)
    print(f"\n🧬 DNA da Loja: {store_dna.name}")
    print(f"  Segmento: {store_dna.segment.value}")
    print(f"  Tamanho: {store_dna.size.value}")
    print(f"  Faturamento mensal: R$ {store_dna.monthly_revenue:,.2f}")
    print(f"  Taxa de conversão: {store_dna.conversion_rate:.1%}")
    print(f"  Pain Points: {', '.join(store_dna.pain_points)}")

    # Análise de maturidade
    maturity = orchestrator.dna_service.analyze_store_maturity(store_id)
    print(f"\n📈 Análise de Maturidade:")
    sorted_maturity = sorted(maturity.items(), key=lambda x: x[1])
    for stage, score in sorted_maturity[:5]:  # Top 5 menores scores
        stage_name = stage.replace('_', ' ').title()
        print(f"  {stage_name}: {score}/10 {'⚠️' if score < 5 else '✅'}")

    # Gaps identificados
    gaps = orchestrator.dna_service.identify_gaps(store_id)
    print(f"\n🎯 Gaps Identificados ({len(gaps)} encontrados):")
    for gap in gaps[:3]:
        print(f"  • {gap['stage'].replace('_', ' ').title()}: {gap['gap_severity']} prioridade")

    # 4. Recomendações personalizadas
    print_section("4. Recomendações Personalizadas")
    recommendations = orchestrator.recommendation_service.get_recommendations_for_store(store_id, limit=5)

    print(f"\n🎯 Top 5 Recomendações para {store_dna.name}:")
    for i, rec in enumerate(recommendations, 1):
        partner = orchestrator.recommendation_service.partners_db.get(rec.partner_id)
        priority_emoji = "🔴" if rec.priority == 1 else "🟡" if rec.priority == 2 else "🟢"

        print(f"\n  {i}. {priority_emoji} {partner.name}")
        print(f"     Score Final: {rec.final_score:.2f}/1.00")
        print(f"     Compatibilidade: {rec.compatibility_score:.2f}")
        print(f"     Rentabilidade: {rec.profitability_score:.2f}")
        print(f"     ROI Estimado: {rec.estimated_roi:.0f}%")
        print(f"     Timeline: {rec.implementation_timeline}")
        if rec.reasoning:
            print(f"     Motivos: {', '.join(rec.reasoning)}")

    # 5. Análise por área prioritária
    print_section("5. Recomendações por Área Prioritária")
    priority_recs = orchestrator.recommendation_service.get_priority_recommendations(store_id)

    for area, recs in priority_recs.items():
        if recs:
            area_name = area.replace('_', ' ').title()
            print(f"\n🎯 {area_name}:")
            for rec in recs[:2]:  # Top 2 por área
                partner = orchestrator.recommendation_service.partners_db.get(rec.partner_id)
                print(f"  • {partner.name} (Score: {rec.final_score:.2f})")

    # 6. Análise de Agentes Autônomos
    print_section("6. Rede de Agentes Autônomos em Ação")

    # Registra agente mestre para a loja
    master_agent = orchestrator.agent_orchestrator.register_master_agent(store_id)
    print(f"✅ Agente Mestre registrado: {master_agent.agent_id}")

    # Executa análise do agente mestre
    all_stores = list(orchestrator.dna_service.stores_db.values())
    all_partners = list(orchestrator.recommendation_service.partners_db.values())
    context = {
        "store_id": store_id,
        "stores": all_stores,
        "partners": all_partners
    }

    master_result = master_agent.execute_action(context)
    print(f"\n🤖 Análise do Agente Mestre:")
    print(f"  Insights gerados: {len(master_result.get('insights', []))}")
    for insight in master_result.get('insights', [])[:3]:
        print(f"  • {insight}")

    # Agente de Inteligência de Mercado
    market_agent = orchestrator.agent_orchestrator.market_agent
    market_analysis = market_agent.execute_action(context)

    print(f"\n📊 Inteligência de Mercado:")
    market_overview = market_analysis['market_overview']
    print(f"  Total de lojas: {market_overview['total_stores']}")
    print(f"  Total de parceiros: {market_overview['total_partners']}")

    segment_dist = market_analysis['segment_distribution']
    print(f"  Distribuição por segmento:")
    for segment, count in segment_dist.items():
        print(f"    {segment.replace('_', ' ').title()}: {count} lojas")

    # 7. Dashboard do Ecossistema
    print_section("7. Dashboard do Ecossistema Órion")
    dashboard = orchestrator.get_ecosystem_dashboard()

    overview = dashboard['ecosystem_overview']
    print(f"\n🌟 Visão Geral do Ecossistema:")
    print(f"  Total de Lojas: {overview['total_stores']}")
    print(f"  Total de Parceiros: {overview['total_partners']}")
    print(f"  Receita Total Mensal: R$ {overview['total_monthly_revenue']:,.2f}")
    print(f"  Taxa de Conversão Média: {overview['average_conversion_rate']:.2%}")

    health = dashboard['health_metrics']
    print(f"\n💚 Métricas de Saúde:")
    print(f"  Lojas com Recomendações: {health['stores_with_recommendations']}")
    print(f"  Agentes Ativos: {health['active_agents']}")
    print(f"  Maturidade do Ecossistema: {health['ecosystem_maturity']}")

    # 8. Simulação de onboarding
    print_section("8. Simulação - Onboarding Nova Loja")

    new_store_data = {
        "store_id": "nova_loja_demo",
        "name": "Demo Store - Suplementos",
        "segment": "saude_beleza",
        "size": "pequena", 
        "monthly_revenue": 8000,
        "monthly_orders": 60,
        "avg_ticket": 133.33,
        "conversion_rate": 0.015,
        "pain_points": ["conversao_baixa", "seo", "mobile"],
        "priorities": {
            "1_atracao": 9,
            "3_navegacao": 8,
            "5_carrinho": 9
        }
    }

    onboard_result = orchestrator.onboard_store(new_store_data)
    print(f"✅ Nova loja onboarded: {onboard_result['store_id']}")
    print(f"🤖 Agente Mestre criado: {onboard_result['master_agent_id']}")
    print(f"📊 Gaps identificados: {len(onboard_result['identified_gaps'])}")
    print(f"🎯 Recomendações iniciais: {len(onboard_result['initial_recommendations'])}")

    if onboard_result['initial_recommendations']:
        print("\n🎯 Primeiras recomendações:")
        for rec in onboard_result['initial_recommendations'][:3]:
            partner = orchestrator.recommendation_service.partners_db.get(rec['partner_id'])
            print(f"  • {partner.name} (Score: {rec['score']:.2f}, Prioridade: {rec['priority']})")

    # 9. Análise de impacto de novo parceiro
    print_section("9. Simulação - Novo Parceiro no Ecossistema")

    new_partner_data = {
        "partner_id": "demo_partner_ai",
        "name": "AI PersonalizaMax",
        "category": "3_navegacao",
        "subcategory": "Personalização com IA",
        "description": "Personalização avançada com inteligência artificial",
        "pricing_model": "fixed",
        "min_price": 399,
        "max_price": 1499,
        "target_segments": ["fashion", "casa_jardim", "saude_beleza"],
        "target_sizes": ["pequena", "media"],
        "integration_complexity": 4,
        "roi_potential": 9,
        "commission_rate": 0.25
    }

    partner_result = orchestrator.add_partner_to_ecosystem(new_partner_data)
    print(f"✅ Novo parceiro adicionado: {partner_result['partner_id']}")
    print(f"📊 Impacto no mercado: {partner_result['market_impact']['market_opportunity']}")
    print(f"🎯 Matches potenciais: {partner_result['market_impact']['potential_matches']} lojas")
    print(f"📈 Percentual de match: {partner_result['market_impact']['match_percentage']:.1f}%")

    # 10. Resultados finais
    print_section("10. Resumo da Demonstração")

    final_dashboard = orchestrator.get_ecosystem_dashboard()
    final_overview = final_dashboard['ecosystem_overview']

    print("\n🎉 Sistema Órion Demonstrado com Sucesso!")
    print(f"\n📊 Estado Final do Ecossistema:")
    print(f"  • {final_overview['total_stores']} lojas gerenciadas")
    print(f"  • {final_overview['total_partners']} parceiros no catálogo")
    print(f"  • R$ {final_overview['total_monthly_revenue']:,.2f} em faturamento mensal total")
    print(f"  • {final_dashboard['health_metrics']['active_agents']} agentes ativos")

    print(f"\n🚀 Capacidades Demonstradas:")
    print("  ✅ Criação e análise de DNA das lojas")
    print("  ✅ Sistema de scoring inteligente (compatibilidade + rentabilidade)")
    print("  ✅ Rede de agentes autônomos funcionando")
    print("  ✅ Recomendações personalizadas e priorizadas")
    print("  ✅ Análise de gaps e maturidade")
    print("  ✅ Onboarding automatizado de lojas")
    print("  ✅ Gestão de parceiros e impacto de mercado")
    print("  ✅ Dashboard completo do ecossistema")
    print("  ✅ Inteligência de mercado e oportunidades")

    print(f"\n🎯 Próximos Passos Recomendados:")
    print("  1. Implementar frontend web para visualização")
    print("  2. Adicionar machine learning aos algoritmos de scoring")
    print("  3. Integrar com APIs reais de parceiros")
    print("  4. Implementar sistema de notificações e alertas")
    print("  5. Adicionar métricas avançadas e analytics")

    print("\n" + "="*60)
    print("🌟 DEMONSTRAÇÃO CONCLUÍDA - PROJETO ÓRION FUNCIONAL!")
    print("="*60)

if __name__ == "__main__":
    run_orion_demo()
