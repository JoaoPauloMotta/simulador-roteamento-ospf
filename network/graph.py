"""Modulo responsavel por representar a topologia da rede como um grafo."""





class NetworkGraph:

    """Representa a topologia da rede usando uma lista de adjacencia."""



    def __init__(self) -> None:

        # dicionario de dicionarios: {roteador: {vizinho: latencia}}

        self.graph: dict[str, dict[str, float]] = {}



    def add_router(self, name: str) -> None:

        """Adiciona um novo roteador ao grafo."""

        if name not in self.graph:

            self.graph[name] = {}



    def add_link(self, router1: str, router2: str, latency: float) -> None:

        """Adiciona um link bidirecional entre dois roteadores."""

        if router1 not in self.graph or router2 not in self.graph:

            raise ValueError("Um ou ambos os roteadores nao existem.")



        self.graph[router1][router2] = latency

        self.graph[router2][router1] = latency



    def remove_link(self, router1: str, router2: str) -> None:

        """Remove um link entre dois roteadores."""

        if router1 in self.graph and router2 in self.graph[router1]:

            del self.graph[router1][router2]

        if router2 in self.graph and router1 in self.graph[router2]:

            del self.graph[router2][router1]



    def get_neighbors(self, router: str) -> dict[str, float]:

        """Retorna os vizinhos de um roteador."""

        return self.graph.get(router, {})



    def get_all_routers(self) -> list[str]:

        """Retorna todos os roteadores na rede."""

        return list(self.graph.keys())
