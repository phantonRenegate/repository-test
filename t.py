#!/usr/bin/env python3
"""
Script para buscar dados da tabela do Brasileirão e mostrar estatísticas do Corinthians.

--- ERROS DO SCRIPT ORIGINAL ---
1. requests.get() só baixa HTML estático — o ge.globo.com carrega a tabela via
   JavaScript (SPA). O JS nunca executava, então a tabela nunca estava no HTML.
   Resultado: "Tabela de classificação não encontrada."
2. O seletor 'table.tablesorter' não existe na página real do Globo.

--- SOLUÇÃO ---
Usar Playwright, que abre um Chromium headless real, executa o JavaScript
e aguarda o carregamento dinâmico da tabela antes de extrair o HTML.

--- COMO RODAR ---
1. Instale as dependências:
       pip install playwright beautifulsoup4
       playwright install chromium

2. Execute:
       python3 t.py
"""

import re
import sys

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://ge.globo.com/futebol/brasileirao-serie-a/"


def _to_int(text: str) -> int | None:
    """Extrai o primeiro número inteiro de uma string. Retorna None se não achar."""
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def fetch_brasileirao_table() -> list[dict]:
    """
    Abre o site com Playwright (Chromium headless), aguarda a tabela carregar
    e retorna uma lista de dicionários com os dados de cada time.

    Estratégia de carregamento:
    - wait_until="domcontentloaded" (não espera networkidle — o Globo tem ads
      e trackers que nunca param de fazer requests, causando timeout).
    - Recursos desnecessários (imagens, fontes, media) são bloqueados para
      carregar mais rápido.
    - Aguardamos explicitamente pelo seletor da tabela depois do goto.
    """
    print("Iniciando navegador headless (Chromium)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # Bloqueia recursos pesados que não afetam o conteúdo da tabela
        def block_heavy(route, request):
            if request.resource_type in ("image", "media", "font", "stylesheet"):
                route.abort()
            else:
                route.continue_()

        page.route("**/*", block_heavy)

        print(f"Carregando {URL}")
        # "domcontentloaded" — não aguarda requests contínuos de ads/trackers
        page.goto(URL, wait_until="domcontentloaded", timeout=60_000)

        # Aguarda a tabela aparecer no DOM (JavaScript ainda precisa rodar)
        try:
            page.wait_for_selector("table", timeout=30_000)
        except Exception:
            html_snapshot = page.content()
            browser.close()
            debug_path = "/tmp/globo_debug.html"
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(html_snapshot)
            print(
                f"[ERRO] Tabela não apareceu após 30 s.\n"
                f"HTML salvo em {debug_path} — inspecione para ver o que o site retornou."
            )
            sys.exit(1)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # O Globo usa DUAS tabelas separadas:
    #   Tabela 0 — colunas: Posição | Time (nome+sigla concatenados) | (ignorar)
    #   Tabela 1 — colunas: P | J | V | E | D | GP | GC | SG | % | Últimos jogos
    # As linhas das duas tabelas se correspondem pela mesma posição.
    tables = soup.find_all("table")
    if len(tables) < 2:
        print(f"[ERRO] Esperava 2 tabelas, encontrou {len(tables)}.")
        sys.exit(1)

    # Apenas linhas de dados (com <td>, sem <th>)
    name_rows = [r for r in tables[0].find_all("tr") if r.find("td")]
    stat_rows = [r for r in tables[1].find_all("tr") if r.find("td")]

    teams: list[dict] = []

    for name_row, stat_row in zip(name_rows, stat_rows):
        nc = name_row.find_all("td")
        sc = stat_row.find_all("td")

        if len(nc) < 2 or len(sc) < 3:
            continue

        position = _to_int(nc[0].get_text(strip=True))

        # Remove a sigla de 3 letras maiúsculas colada ao final do nome
        # ex: "CorinthiansCOR" → "Corinthians", "São PauloSAO" → "São Paulo"
        raw_name = nc[1].get_text(strip=True)
        name = re.sub(r"[A-Z]{3}$", "", raw_name).strip()

        # Tabela 1: P=0, J=1, V=2, E=3, D=4, GP=5, GC=6, SG=7, %=8
        played = _to_int(sc[1].get_text(strip=True))  # J (jogos)
        won    = _to_int(sc[2].get_text(strip=True))  # V (vitórias)

        if position is None or not name or played is None or won is None:
            continue

        teams.append({"position": position, "name": name, "played": played, "won": won})

    return teams


def find_corinthians(teams: list[dict]) -> dict | None:
    for team in teams:
        if "corinthians" in team["name"].lower():
            return team
    return None


def main():
    print("Buscando dados da tabela do Brasileirão...")
    teams = fetch_brasileirao_table()

    if not teams:
        print("[ERRO] Nenhum time extraído da tabela.")
        print("Verifique se a estrutura da página mudou e ajuste as constantes COL_*.")
        sys.exit(1)

    corinthians = find_corinthians(teams)

    if not corinthians:
        print("[ERRO] Corinthians não encontrado na tabela.")
        print("Times encontrados:", [t["name"] for t in teams])
        sys.exit(1)

    win_pct = (
        (corinthians["won"] / corinthians["played"]) * 100
        if corinthians["played"] > 0
        else 0.0
    )

    print()
    print("=== ESTATÍSTICAS DO CORINTHIANS ===")
    print(f"Posição:                 {corinthians['position']}º")
    print(f"Jogos disputados:        {corinthians['played']}")
    print(f"Vitórias:                {corinthians['won']}")
    print(f"Porcentagem de vitórias: {win_pct:.1f}%")


if __name__ == "__main__":
    main()