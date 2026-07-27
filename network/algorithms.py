"""Modulo com os algoritmos de roteamento usados pelo simulador."""

import heapq

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


def dijkstra(
    graph_obj: NetworkGraph,
    start_node: str,
    end_node: str,
) -> tuple[list[str], float]:
    """
    Encontra o caminho de menor latencia entre dois roteadores usando Dijkstra
    com uma fila de prioridades.

    Retorna uma tupla contendo o caminho e a latencia total.

    Levanta NoPathFoundError caso o destino esteja isolado ou algum dos
    roteadores informados nao exista na topologia atual.
    """
    routers = graph_obj.get_all_routers()

    if start_node not in routers or end_node not in routers:
        raise NoPathFoundError(start_node, end_node)

    # Distancia conhecida e roteador anterior no melhor caminho encontrado.
    distances: dict[str, float] = {
        node: float("inf") for node in routers
    }
    previous_nodes: dict[str, str | None] = {
        node: None for node in routers
    }

    distances[start_node] = 0

    # Cada item da fila possui: (distancia acumulada, roteador).
    priority_queue: list[tuple[float, str]] = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Ignora entradas antigas que permaneceram na fila após uma rota
        # melhor para o mesmo roteador ter sido encontrada.
        if current_distance > distances[current_node]:
            continue

        if current_node == end_node:
            break

        for neighbor, weight in graph_obj.get_neighbors(current_node).items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor),
                )

    if distances[end_node] == float("inf"):
        raise NoPathFoundError(start_node, end_node)

    # Reconstrucao eficiente do caminho, do destino ate a origem.
    path: list[str] = []
    current: str | None = end_node

    while current is not None:
        path.append(current)
        current = previous_nodes[current]

    path.reverse()

    return path, distances[end_node]d_node]
