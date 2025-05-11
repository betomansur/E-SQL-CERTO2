import json
import sys
import os

def analisar_resultados(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    etapas = ["SF", "CSG", "QE", "SR"]
    tempo_total = {etapa: 0.0 for etapa in etapas}
    tempo_total["total_time"] = 0.0
    total_tokens = 0
    total_perguntas = 0
    total_acertos = 0

    for item in dados:
        total_perguntas += 1

        # Tempo
        timing = item.get("timing", {})
        for etapa in etapas:
            tempo_total[etapa] += timing.get(etapa, 0.0)
        tempo_total["total_time"] += timing.get("total_time", 0.0)

        # Tokens
        total_tokens += item.get("total_usage", {}).get("total_tokens", 0)

        # Acurácia
        if item.get("results", {}).get("exec_res", 0) == 1:
            total_acertos += 1

    print(f"\n📊 Estatísticas com base em {total_perguntas} perguntas:")

    print("\n⏱️ Tempos médios por etapa:")
    for etapa in etapas + ["total_time"]:
        media = tempo_total[etapa] / total_perguntas
        print(f" - {etapa}: {media:.2f} segundos")

    media_tokens = total_tokens / total_perguntas
    print(f"\n🔢 Média de total_tokens por pergunta: {media_tokens:.2f}")

    acuracia = (total_acertos / total_perguntas) * 100
    print(f"\n✅ Acurácia: {acuracia:.2f}% ({total_acertos} corretas de {total_perguntas})")


import os
import glob

def processar_todos_resultados(pasta_base="results"):
    # Percorre todos os subdiretórios da pasta 'results' e encontra predictions.json
    caminhos = glob.glob(os.path.join(pasta_base, "**", "predictions.json"), recursive=True)
    
    for caminho in caminhos:
        print(f"Analisando: {caminho}")
        analisar_resultados(caminho)

# Chamada da função principal
processar_todos_resultados()
