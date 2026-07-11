"""Modulo com as rotinas de simulacao de eventos na rede (ex: queda de link)."""

from network.graph import NetworkGraph


def simulate_link_failure(graph_obj: NetworkGraph, router1: str, router2: str) -> tuple[bool, str]:
    """
    Simula uma queda de link entre dois roteadores, removendo-o do grafo,
    e retorna o status da operacao.
    """
    try:
        graph_obj.remove_link(router1, router2)
        return True, f"Link entre {router1} e {router2} removido com sucesso."
    except Exception as error:
        return False, str(error)
