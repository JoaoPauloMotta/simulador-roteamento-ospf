"""Modulo com as rotinas de simulacao de eventos na rede (ex: queda de link)."""

from network.graph import NetworkGraph
from network.algorithms import dijkstra, NoPathFoundError


def check_network_isolation(graph_obj: NetworkGraph, reference_node: str) -> list[str]:
    """
    Verifica, a partir de um roteador de referencia, quais roteadores da rede
    ficaram inalcancaveis (isolados) na topologia atual.
    Retorna a lista de roteadores isolados.
    """
    isolated_routers: list[str] = []

    # percorre todos os roteadores da rede, exceto o proprio no de referencia
    for router in graph_obj.get_all_routers():
        if router == reference_node:
            continue

        # tenta calcular uma rota; se nao houver caminho, o roteador esta isolado
        try:
            dijkstra(graph_obj, reference_node, router)
        except NoPathFoundError:
            isolated_routers.append(router)

    return isolated_routers


def simulate_link_failure(graph_obj: NetworkGraph, router1: str, router2: str) -> tuple[bool, str]:
    """
    Simula uma queda de link entre dois roteadores, removendo-o do grafo,
    e retorna o status da operacao.

    Apos a remocao, verifica se a rede permanece totalmente conectada. Caso
    algum roteador tenha ficado isolado (cenario de "Roteamento Impossivel"),
    o retorno inclui uma mensagem detalhando quais roteadores foram afetados.
    """
    try:
        graph_obj.remove_link(router1, router2)
    except Exception as error:
        return False, str(error)

    all_routers = graph_obj.get_all_routers()
    if not all_routers:
        return True, f"Link entre {router1} e {router2} removido com sucesso."

    # escolhe um roteador de referencia para verificar a conectividade da rede
    reference_node = all_routers[0]
    isolated_routers = check_network_isolation(graph_obj, reference_node)

    # monta a mensagem final, alertando sobre roteadores isolados, se houver
    if isolated_routers:
        isolated_list = ", ".join(isolated_routers)
        message = (
            f"Link entre {router1} e {router2} removido.\n"
            f"----------------------------------------\n"
            f"[Roteamento Impossivel]\n"
            f"Nenhuma rota alternativa foi encontrada.\n"
            f"Roteador(es) isolado(s) da rede: {isolated_list}\n"
            f"----------------------------------------"
        )
        return True, message

    return True, f"Link entre {router1} e {router2} removido com sucesso. Rede permanece totalmente conectada."
