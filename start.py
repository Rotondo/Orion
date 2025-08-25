#!/usr/bin/env python3
"""
Script para inicializar o Projeto Órion
"""

import os
import sys
import subprocess
import time

def print_logo():
    logo = """
    ██████╗ ██████╗  ██████╗      ██╗███████╗████████╗ ██████╗      ██████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝╚══██╔══╝██╔═══██╗    ██╔═══██╗██╔══██╗██║██╔═══██╗████╗  ██║
    ██████╔╝██████╔╝██║   ██║     ██║█████╗     ██║   ██║   ██║    ██║   ██║██████╔╝██║██║   ██║██╔██╗ ██║
    ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝     ██║   ██║   ██║    ██║   ██║██╔══██╗██║██║   ██║██║╚██╗██║
    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗   ██║   ╚██████╔╝    ╚██████╔╝██║  ██║██║╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝   ╚═╝    ╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

    🚀 SISTEMA INTELIGENTE DE ORQUESTRAÇÃO DE E-COMMERCE
    """
    print(logo)

def check_python_version():
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        sys.exit(1)

def run_tests():
    print("🧪 Executando testes...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              check=True, capture_output=True, text=True)
        print("✅ Todos os testes passaram")
    except subprocess.CalledProcessError as e:
        print("⚠️  Alguns testes falharam, mas continuando...")
        print(e.stdout)

def start_api():
    print("🚀 Iniciando API do Órion...")
    print("📡 API será acessível em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("\n⏱️  Aguardando 3 segundos antes de iniciar...")
    time.sleep(3)

    try:
        os.system(f"{sys.executable} -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload")
    except KeyboardInterrupt:
        print("\n👋 Sistema Órion encerrado pelo usuário")

def main():
    print_logo()
    print("Autor: Manus AI | Data: 25 de Agosto de 2025\n")

    check_python_version()
    install_dependencies()
    run_tests()

    print("\n🌟 Sistema Órion pronto para uso!")
    print("\nOpções disponíveis:")
    print("1. Iniciar API (recomendado)")
    print("2. Executar demonstração")
    print("3. Sair")

    while True:
        choice = input("\nEscolha uma opção (1-3): ").strip()

        if choice == "1":
            start_api()
            break
        elif choice == "2":
            print("\n🎬 Executando demonstração...")
            os.system(f"{sys.executable} demo.py")
            break
        elif choice == "3":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida. Digite 1, 2 ou 3.")

if __name__ == "__main__":
    main()
