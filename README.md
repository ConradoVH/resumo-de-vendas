# 📊 Resumo de Vendas

Transforma a planilha de vendas em um relatório pronto — faturamento total, por mês, por categoria e o top de produtos — em um comando, sem abrir Excel.

## O problema que resolve

Todo fim de mês a mesma cena: abrir a planilha, filtrar, somar à mão, montar o relatório no Word. 2 horas de trabalho que este script faz em 1 segundo — sempre do mesmo jeito, sem erro de conta.

## Como usar

```bash
python3 resumo.py vendas.csv                      # relatório na tela
python3 resumo.py vendas.csv --top 10             # top 10 produtos
python3 resumo.py vendas.csv --saida relatorio.txt  # salva em arquivo
```

**Requisito: só Python 3.** Nada para instalar.

## inteligente por padrão

- Detecta sozinho se o CSV usa **ponto-e-vírgula (Excel BR) ou vírgula (padrão internacional)**
- Entende preços em **formato brasileiro** (`1.234,56`) e internacional (`1234.56`)
- Acha as colunas pelos nomes comuns (`Produto`/`Item`, `Preço`/`Valor`, `Quantidade`/`Qtd`, `Data`, `Categoria`)
- Pula linhas inválidas sem quebrar

## Exemplo real (gerado do `exemplo-vendas.csv`)

```
====================================================
                RELATÓRIO DE VENDAS                 
====================================================
Planilha: portfolio/resumo-de-vendas/exemplo-vendas.csv
Pedidos: 15  |  Itens: 33  |  Faturamento: R$ 6.293,10

FATURAMENTO POR MÊS
  08/2026           R$ 3.815,30
  09/2026           R$ 2.477,80

POR CATEGORIA
  Monitores                       R$ 2.697,00
  Periféricos                     R$ 1.849,00
  Acessórios                        R$ 947,60
  Áudio                             R$ 799,50

TOP 5 PRODUTOS (por receita)
  1. Monitor 24 polegadas              R$ 2.697,00 (3 un.)
  2. Teclado Mecânico                  R$ 1.449,50 (5 un.)
  3. Headset com Microfone               R$ 799,50 (5 un.)
  4. Mouse Sem Fio                       R$ 399,50 (5 un.)
  5. Mousepad XL                         R$ 319,20 (8 un.)
====================================================
```

## Adaptando para você

Sua planilha tem outras colunas (vendedor, forma de pagamento)? Quer o relatório em PDF, com gráfico, ou enviado por e-mail todo dia 1º? É a adaptação que eu faço para você.

---

*Feito como demonstração de automação Python sob medida. Sua tarefa chata vira 1 comando — fale comigo: [seu e-mail] · [seu LinkedIn]*
