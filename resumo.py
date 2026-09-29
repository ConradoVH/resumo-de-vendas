#!/usr/bin/env python3
"""
Resumo de Vendas — lê a planilha de vendas (CSV) e gera um relatório pronto:
faturamento total, por mês, por categoria e o top de produtos.

Aceita CSV do Excel brasileiro (ponto-e-vírgula, preços "289,90") e do
padrão internacional (vírgula, preços "289.90"). Detecta sozinho.

Uso:
    python3 resumo.py vendas.csv
    python3 resumo.py vendas.csv --top 10 --saida relatorio.txt
"""
import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime


def numero(texto) -> float:
    """Converte '1234.56', '1.234,56' ou 'R$ 1.234,56' em número."""
    texto = str(texto).replace("R$", "").replace(" ", "").strip()
    if not texto:
        return 0.0
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")  # formato BR 1.234,56
    elif "," in texto:
        texto = texto.replace(",", ".")
    return float(texto)


def brl(valor: float) -> str:
    """1234567.89 -> 'R$ 1.234.567,89'"""
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def data_de(texto: str):
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(texto.strip(), formato)
        except (ValueError, AttributeError):
            pass
    return None


def achar_coluna(colunas, *apelidos):
    """Acha a coluna pelo apelido, ignorando maiúsculas (ex.: 'Preço Unitário')."""
    for apelido in apelidos:
        for coluna in colunas:
            if apelido in str(coluna).lower():
                return coluna
    return None


def ler_planilha(caminho: str):
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        try:
            delimitador = csv.Sniffer().sniff(arquivo.read(4096), delimiters=",;\t").delimiter
        except csv.Error:
            delimitador = ";"
        arquivo.seek(0)
        return list(csv.DictReader(arquivo, delimiter=delimitador))


def agregar(linhas, colunas):
    col_produto = achar_coluna(colunas, "produto", "item", "descri")
    col_preco = achar_coluna(colunas, "preço", "preco", "valor")
    col_qtd = achar_coluna(colunas, "quantidade", "qtde", "qtd")
    col_data = achar_coluna(colunas, "data")
    col_categoria = achar_coluna(colunas, "categoria", "tipo")

    if not (col_produto and col_preco):
        sys.exit(f"Erro: preciso das colunas de produto e preço. Encontrei: {', '.join(map(str, colunas))}")

    resumo = {
        "pedidos": 0, "itens": 0.0, "total": 0.0,
        "por_mes": defaultdict(float),
        "por_categoria": defaultdict(float),
        "por_produto": defaultdict(lambda: [0.0, 0.0]),  # [receita, quantidade]
    }

    for linha in linhas:
        try:
            preco = numero(linha.get(col_preco, ""))
        except ValueError:
            continue  # linha inválida (ex.: rodapé) é pulada
        if preco == 0 and not (linha.get(col_produto) or "").strip():
            continue
        try:
            quantidade = int(numero(linha.get(col_qtd, ""))) if col_qtd else 1
        except ValueError:
            quantidade = 1
        quantidade = max(quantidade, 1)
        receita = preco * quantidade

        resumo["pedidos"] += 1
        resumo["itens"] += quantidade
        resumo["total"] += receita

        if col_data:
            data = data_de(linha.get(col_data, "") or "")
            if data:
                resumo["por_mes"][f"{data.month:02d}/{data.year}"] += receita
        if col_categoria:
            categoria = (linha.get(col_categoria) or "—").strip() or "—"
            resumo["por_categoria"][categoria] += receita
        produto = (linha.get(col_produto) or "—").strip() or "—"
        resumo["por_produto"][produto][0] += receita
        resumo["por_produto"][produto][1] += quantidade

    return resumo


def render(resumo, caminho_planilha: str, top_n: int) -> str:
    largura = 52
    r = ["=" * largura, "RELATÓRIO DE VENDAS".center(largura), "=" * largura]
    r.append(f"Planilha: {caminho_planilha}")
    r.append(f"Pedidos: {resumo['pedidos']}  |  Itens: {resumo['itens']:.0f}  |  "
             f"Faturamento: {brl(resumo['total'])}")

    if resumo["por_mes"]:
        r += ["", "FATURAMENTO POR MÊS"]
        meses = sorted(resumo["por_mes"], key=lambda m: (m[3:], m[:2]))
        for mes in meses:
            r.append(f"  {mes:<10} {brl(resumo['por_mes'][mes]):>18}")

    if resumo["por_categoria"]:
        r += ["", "POR CATEGORIA"]
        for categoria, receita in sorted(resumo["por_categoria"].items(), key=lambda i: -i[1]):
            r.append(f"  {categoria:<24.24} {brl(receita):>18}")

    r += ["", f"TOP {top_n} PRODUTOS (por receita)"]
    top = sorted(resumo["por_produto"].items(), key=lambda i: -i[1][0])[:top_n]
    for i, (produto, (receita, quantidade)) in enumerate(top, 1):
        r.append(f"  {i}. {produto:<26.26} {brl(receita):>18} ({quantidade:.0f} un.)")

    r += ["=" * largura]
    return "\n".join(r)


def main():
    parser = argparse.ArgumentParser(description="Gera relatório de vendas a partir de um CSV.")
    parser.add_argument("planilha", help="arquivo CSV de vendas")
    parser.add_argument("--top", type=int, default=5, help="quantos produtos listar (padrão: 5)")
    parser.add_argument("--saida", help="salvar o relatório num arquivo .txt")
    args = parser.parse_args()

    linhas = ler_planilha(args.planilha)
    if not linhas:
        sys.exit("Erro: o arquivo não tem dados.")
    resumo = agregar(linhas, linhas[0].keys())
    relatorio = render(resumo, args.planilha, args.top)

    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(relatorio + "\n")
        print(f"Relatório salvo em: {args.saida}\n")
    print(relatorio)


if __name__ == "__main__":
    main()
