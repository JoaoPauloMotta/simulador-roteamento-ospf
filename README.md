# Simulador de Roteamento OSPF

Simulador didático do protocolo OSPF (Open Shortest Path First), focado no cálculo de rotas de menor latência em uma rede de roteadores, simulação de falhas de link e tratamento de resiliência de rede (nós isolados).

## Sobre
O OSPF é um protocolo de roteamento *link-state* usado em redes internas (IGP), no qual cada roteador conhece a topologia completa da rede e calcula, de forma independente, o caminho de menor custo até qualquer destino. Este projeto implementa essa lógica central: representação da rede como grafo, cálculo de rotas com o algoritmo de Dijkstra, simulação de rompimento de enlaces (*link failure*) e tratamento robusto de exceções quando a topologia se torna desconexa.

## Funcionalidades
* **Visualização do mapa da rede:** Exibe os roteadores ativos, seus respectivos vizinhos e as latências de cada link.
* **Cálculo de rota de menor latência:** Determina o caminho mais rápido entre dois roteadores arbitrários utilizando o algoritmo de Dijkstra.
* **Simulação de rompimento de cabo:** Remove um link da topologia de forma dinâmica, permitindo observar o recálculo automático para rotas contingenciais.
* **Tratamento de Roteamento Impossível:** Identifica quando a queda de um link isola um roteador ou divide a rede, disparando alertas claros em vez de permitir a quebra do simulador.

## Arquitetura do Projeto
O projeto segue uma rigorosa separação em camadas, isolando a lógica de negócios da interface de linha de comando:

```text
network_router/
├── network/
│   ├── graph.py       # Estrutura de dados da topologia (NetworkGraph)
│   └── algorithms.py  # Algoritmo de Dijkstra e exceções de conectividade
├── core/
│   └── simulator.py   # Simulação de eventos e checagem de integridade de rede
├── app.py             # Orquestrador: CLI, tratamento de fluxos e menus
└── README.md
