# Simulador de Roteamento OSPF

Simulador didático em Python para cálculo de rotas de menor latência, análise
de topologias e simulação de falhas de enlaces.

O projeto representa a rede como um grafo ponderado e utiliza o algoritmo de
Dijkstra com fila de prioridades para encontrar o caminho de menor custo.

> O projeto reproduz conceitos centrais de roteamento link-state, mas não
> implementa todas as mensagens, estados e áreas definidos pelo protocolo OSPF.

## Problema estudado

Em uma rede, a rota mais curta pode deixar de existir ou mudar quando um enlace
é interrompido. O simulador permite observar:

1. como os roteadores e enlaces formam um grafo;
2. como o menor caminho é calculado;
3. como uma falha modifica a topologia;
4. quando ainda existe uma rota alternativa;
5. quando parte da rede se torna inalcançável.

## Funcionalidades

- Visualização dos roteadores e enlaces.
- Cálculo da rota de menor latência.
- Simulação da queda de um link.
- Recálculo de rotas alternativas.
- Identificação de roteadores isolados.
- Tratamento de destinos inexistentes ou inalcançáveis.

## Destaques técnicos

- Grafo representado por lista de adjacência.
- Algoritmo de Dijkstra com `heapq`.
- Complexidade de \(O((V+E)\log V)\) para listas de adjacência.
- Exceção específica para ausência de rota.
- Separação entre interface, modelo de rede e simulação.
- Reconstrução eficiente do caminho ao final da busca.

## Estrutura

| Caminho | Responsabilidade |
|---|---|
| `app.py` | Menu, entradas e apresentação dos resultados |
| `network/graph.py` | Representação da topologia |
| `network/algorithms.py` | Dijkstra e tratamento de rotas impossíveis |
| `core/simulator.py` | Falhas de enlaces e conectividade |
| `.gitignore` | Arquivos ignorados pelo Git |
| `README.md` | Documentação do projeto |

## Topologia inicial

| Enlace | Latência |
|---|---:|
| A–B | 2 |
| A–C | 5 |
| B–C | 1 |
| B–D | 3 |
| C–D | 1 |
| C–E | 6 |
| D–E | 4 |

## Como executar

Requer Python 3.10 ou superior e não possui dependências externas.

```bash
cd simulador-roteamento-ospf
python app.py
```

## Exemplo de uso

```text
--- Simulador de Roteamento OSPF ---
1. Ver o mapa da rede
2. Calcular a rota mais rapida
3. Simular rompimento de cabo
4. Sair
Escolha uma opcao: 2
No de origem: A
No de destino: E
Rota: A -> B -> C -> D -> E, Latencia total: 8
```

Após a remoção do enlace C–D, uma rota alternativa pode ser encontrada:

```text
Rota: A -> B -> C -> E, Latencia total: 9
```

## Algoritmo

A fila de prioridades armazena pares no formato:

```text
(distância acumulada, roteador)
```

Quando uma distância menor é encontrada, o roteador é inserido novamente na
fila. Entradas antigas são ignoradas quando retiradas.

Essa abordagem evita a busca linear pelo próximo nó e melhora a escalabilidade
em redes esparsas.

## Limitações e próximos passos

- A topologia inicial está definida diretamente em `app.py`.
- As alterações existem apenas durante a execução.
- O simulador não implementa troca real de pacotes OSPF.
- Ainda não há testes automatizados.
- Próximas evoluções podem incluir carregamento por arquivo, múltiplas áreas,
  custos configuráveis, testes e visualização gráfica da rede.

## Autor

**João Paulo Benati Motta** — estudante de Engenharia Física na UFRGS, com
interesse em algoritmos, redes e arquitetura de software.
