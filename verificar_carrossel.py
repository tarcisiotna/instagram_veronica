#!/usr/bin/env python3
"""
Script para verificar se o carrossel segue todas as regras obrigatórias.
Executar APÓS gerar o HTML e ANTES de exportar os slides.
"""

from pathlib import Path
import sys

def verificar_regras(pasta_slides):
    """Verifica se todas as regras do carrossel estão sendo seguidas"""
    
    pasta = Path(pasta_slides)
    html_path = pasta / "carousel.html"
    
    print("🔍 VERIFICANDO REGRAS DO CARROSSEL...")
    print("=" * 50)
    
    # REGRA 1: HTML existe e tem tamanho adequado
    if not html_path.exists():
        print("❌ VIOLAÇÃO: carousel.html não encontrado!")
        print("   Use: python3 modelo_instagram.py \"Título\" \"Subtítulo\"")
        return False
    
    html_size_mb = html_path.stat().st_size / 1024 / 1024
    if html_size_mb < 1.5:  # nanobanana tem imagens menores (80KB-130KB)
        print(f"❌ VIOLAÇÃO: carousel.html tem apenas {html_size_mb:.1f}MB")
        print("   Deve ter >1.5MB (imagens embedadas)")
        return False
    else:
        print(f"✅ HTML: {html_size_mb:.1f}MB (ok)")
    
    # REGRA 2: Verificar se há imagens de baixa qualidade no HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "foto1.jpeg" in content:
        print("❌ VIOLAÇÃO: HTML contém foto1.jpeg (baixa qualidade)")
        print("   Use apenas imagens >7MB: 0AVA3114.jpg, 0AVA3115.jpg, etc.")
        return False
    else:
        print("✅ Imagens: Nenhuma imagem de baixa qualidade detectada")
    
    # REGRA 3: Verificar se export script está disponível
    export_script = Path(__file__).parent / "export_veronica_node.js"
    if not export_script.exists():
        print("❌ VIOLAÇÃO: export_veronica_node.js não encontrado!")
        print("   Use o script correto com scale factor 2.5714")
        return False
    else:
        print("✅ Export script: export_veronica_node.js disponível")
    
    print("=" * 50)
    print("✅ TODAS AS REGRAS CUMPRIDAS!")
    print(f"\n📋 PRÓXIMOS PASSOS:")
    print(f"1. Exportar: node export_veronica_node.js")
    print(f"2. Verificar: ls -lh {pasta}/slide_1.png")
    print(f"3. Postar no Instagram! 🎉")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 verificar_carrossel.py pasta/dos/slides")
        print("Ex: python3 verificar_carrossel.py slides/reeducacao-alimentar")
        sys.exit(1)
    
    sucesso = verificar_regras(sys.argv[1])
    sys.exit(0 if sucesso else 1)