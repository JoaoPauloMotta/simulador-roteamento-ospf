"""Modulo com os algoritmos de roteamento usados pelo simulador."""

from network.graph import NetworkGraph


class NoPathFoundError(Exception):
    """
    Levantada quando nao existe nenhum caminho possivel entre dois roteadores
    na topologia atual (por exemplo, apos a queda de um link que isola um no).
    """

    def __init__(self, start_node: str, end_node: str) -> None:
        self.start_node = start_node
        self.end_node = end_node
        super().__init__(
            f"Nenhuma rota disponivel entre {start_node} e {end_node}: "
            f"destino inalcancavel na topologia atual."
        )


def dijkstra(graph_obj: NetworkGraph, start_node: str, end_node: str) -> tuple[list[str], float]:
    """
    Algoritmo de Dijkstra para encontrar o caminho de menor latencia entre dois roteadores.
    Retorna (caminho, latencia_total).

    Levanta NoPathFoundError caso o destino esteja isolado na topologia atual.
    """
    if start_node not in graph_obj.get_all_routers() or end_node not in graph_obj.get_all_routers():
        raise NoPathFoundError(start_node, end_node)

    # 1. Inicializacao das estruturas do Dijkstra
    distances: dict[str, float] = {node: float("inf") for node in graph_obj.get_all_routers()}
    previous_nodes: dict[str, str | None] = {node: None for node in graph_obj.get_all_routers()}
    distances[start_node] = 0

    unvisited: set[str] = set(graph_obj.get_all_routers())

    # 2. Busca do caminho de menor custo, no a no
    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])

        if distances[current_node] == float("inf"):
            break

        if current_node == end_node:
            break

        unvisited.remove(current_node)

        # atualiza a distancia dos vizinhos do no atual, se encontrar um caminho mais curto
        for neighbor, weight in graph_obj.get_neighbors(current_node).items():
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

    # 3. Reconstrucao do caminho a partir dos nos anteriores
    if distances[end_node] == float("inf"):
        raise NoPathFoundError(start_node, end_node)

    path: list[str] = []
    current: str | None = end_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[end_node]
