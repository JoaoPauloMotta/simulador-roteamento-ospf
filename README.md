#Simulador de Roteamento OSPF

Simulador didático do protocolo OSPF (Open Shortest Path First), focado no cálculo de rotas de menor latência em uma rede de roteadores e na simulação de falhas de link.

Sobre

O OSPF é um protocolo de roteamento link-state usado em redes internas (IGP), no qual cada roteador conhece a topologia completa da rede e calcula, de forma independente, o caminho de menor custo até qualquer destino. Este projeto implementa essa lógica central: representação da rede como grafo, cálculo de rotas com o algoritmo de Dijkstra e simulação de rompimento de enlaces (link failure), que obriga o recálculo das rotas.

Funcionalidades


Visualização do mapa da rede (roteadores e seus vizinhos, com a latência de cada link)
Cálculo da rota de menor latência entre dois roteadores (algoritmo de Dijkstra)
Simulação de rompimento de cabo (remoção de um link), permitindo observar o recálculo de rotas contingenciais


Arquitetura

O projeto segue separação em camadas, sem misturar lógica de rede, algoritmos e interface no mesmo arquivo:

network_router/
├── network/
│   ├── graph.py         # estrutura de dados da topologia (NetworkGraph)
│   └── algorithms.py    # algoritmo de Dijkstra
├── core/
│   └── simulator.py     # simulação de eventos na rede (queda de link)
├── app.py                # orquestrador: menu, entrada do usuário e chamadas às camadas acima
└── README.md


network/graph.py — representa a topologia como lista de adjacência (dict[str, dict[str, float]]), com métodos para adicionar/remover roteadores e links.
network/algorithms.py — implementação do Dijkstra, que recebe um NetworkGraph e retorna o caminho de menor custo entre dois nós.
core/simulator.py — simula eventos de rede, hoje a queda de um link entre dois roteadores.
app.py — camada de interface (CLI): menu, coleta de entrada e exibição de resultados. Não contém lógica de roteamento.


Como rodar

Requer Python 3.10 ou superior (usa list[str] | None nas assinaturas).

bashpython app.py

Exemplo de uso

--- Simulador de Roteamento OSPF ---
1. Ver o mapa da rede
2. Calcular a rota mais rapida
3. Simular rompimento de cabo
4. Sair
Escolha uma opcao: 2
No de origem: A
No de destino: E
Rota: A -> B -> C -> D -> E, Latencia total: 8

Após simular a queda do link C-D, o mesmo cálculo recalcula automaticamente uma rota alternativa:

Escolha uma opcao: 3
Roteador 1 do link: C
Roteador 2 do link: D
Link entre C e D removido com sucesso.
Recalculando rotas contingenciais...

Escolha uma opcao: 2
No de origem: A
No de destino: E
Rota: A -> B -> C -> E, Latencia total: 9

Topologia inicial

LinkLatênciaA-B2A-C5B-C1B-D3C-D1D-E4C-E6

Algoritmo

O cálculo de rotas usa o Dijkstra clássico: a partir do roteador de origem, mantém a menor distância conhecida até cada nó e vai expandindo pelo nó não visitado de menor distância, atualizando os vizinhos até alcançar o destino (ou esgotar os nós alcançáveis). A complexidade é O(V²) na implementação atual, adequada para redes pequenas/médias como as simuladas aqui.

Possíveis extensões


Trocar a busca linear do nó de menor distância por uma priority queue (heapq), reduzindo a complexidade para O((V + E) log V)
Persistir a topologia da rede em arquivo, permitindo carregar cenários diferentes
Suporte a múltiplas áreas OSPF (hierarquia de roteamento)
