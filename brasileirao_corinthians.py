#!/usr/bin/env python3
"""
Script para buscar dados da tabela do Brasileirão e mostrar as estatísticas do Corinthians.

Como rodar:
1. Certifique-se de ter Python 3 instalado.
2. Instale as dependências: pip install requests beautifulsoup4
3. Execute o script: python3 brasileirao_corinthians.py

O script acessa a página do Brasileirão no Globo e extrai a tabela de classificação,
encontra o Corinthians e exibe sua posição, jogos disputados, vitórias e porcentagem de vitórias.
"""

import requests
from bs4 import BeautifulSoup
import sys

def fetch_brasileirao_table():
    """
    Busca a tabela do Brasileirão no site da Globo.
    Retorna uma lista de dicionários com os dados de cada time.
    """
    url = "https://ge.globo.com/futebol/brasileirao-serie-a/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        sys.exit(1)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Procurar a tabela de classificação
    table = soup.find('table', {'class': 'tablesorter'})
    
    if not table:
        print("Tabela de classificação não encontrada.")
        sys.exit(1)
    
    # Extrair os dados da tabela
    rows = table.find_all('tr')[1:]  # Ignorar o cabeçalho
    
    teams_data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 6:  # Verificar se há colunas suficientes
            team_name = cols[1].get_text(strip=True)
            played = int(cols[2].get_text(strip=True))
            won = int(cols[3].get_text(strip=True))
            drawn = int(cols[4].get_text(strip=True))
            lost = int(cols[5].get_text(strip=True))
            
            # Calcular pontos (3 por vitória, 1 por empate)
            points = won * 3 + drawn * 1
            
            teams_data.append({
                'name': team_name,
                'played': played,
                'won': won,
                'drawn': drawn,
                'lost': lost,
                'points': points
            })
    
    return teams_data

def get_corinthians_stats(teams_data):
    """
    Encontra as estatísticas do Corinthians na lista de times.
    Retorna um dicionário com as informações.
    """
    for team in teams_data:
        if 'Corinthians' in team['name']:
            return team
    
    return None

def main():
    print("Buscando dados da tabela do Brasileirão...")
    teams_data = fetch_brasileirao_table()
    
    corinthians = get_corinthians_stats(teams_data)
    
    if not corinthians:
        print("Corinthians não encontrado na tabela.")
        sys.exit(1)
    
    # Calcular porcentagem de vitórias
    win_percentage = (corinthians['won'] / corinthians['played']) * 100 if corinthians['played'] > 0 else 0
    
    print("\n=== ESTATÍSTICAS DO CORINTHIANS ===")
    print(f"Posição: {teams_data.index(corinthians) + 1}")
    print(f"Jogos disputados: {corinthians['played']}")
    print(f"Vitórias: {corinthians['won']}")
    print(f"Porcentagem de vitórias: {win_percentage:.2f}%")

if __name__ == "__main__":
    main()