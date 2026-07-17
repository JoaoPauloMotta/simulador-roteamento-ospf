"""Orquestrador do Simulador de Roteamento OSPF (Open Shortest Path First)."""

import sys
import os

# adiciona o diretorio atual ao path para permitir a importacao dos modulos internos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.graph import NetworkGraph
from network.algorithms import dijkstra, NoPathFoundError
from core.simulator import simulate_link_failure


# ---------------------------------------------------------------------------
# Helpers de input
# ---------------------------------------------------------------------------

def get_router_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip().upper()
        if value:
            return value
        print("O campo nao pode ficar vazio.")


def get_menu_option() -> str:
    return input("Escolha uma opcao: ").strip()


# ---------------------------------------------------------------------------
# Helpers de display
# ---------------------------------------------------------------------------

def show_header() -> None:
    print("\n--- Simulador de Roteamento OSPF ---")
    print("1. Ver o mapa da rede")
    print("2. Calcular a rota mais rapida")
    print("3. Simular rompimento de cabo")
    print("4. Sair")


def display_map(net: NetworkGraph) -> None:
    """Exibe o mapa da rede."""
    print("\n--- Mapa da Rede ---")
    for router in net.get_all_routers():
        neighbors = net.get_neighbors(router)
        print(f"Roteador {router}: {neighbors}")
    print("--------------------\n")


# ---------------------------------------------------------------------------
# Configuracao inicial da rede
# ---------------------------------------------------------------------------

def setup_initial_network() -> NetworkGraph:
    """Configura a topologia inicial da rede."""
    net = NetworkGraph()
    for router in ["A", "B", "C", "D", "E"]:
        net.add_router(router)

    # links iniciais entre os roteadores (roteador1, roteador2, latencia)
    net.add_link("A", "B", 2)
    net.add_link("A", "C", 5)
    net.add_link("B", "C", 1)
    net.add_link("B", "D", 3)
    net.add_link("C", "D", 1)
    net.add_link("D", "E", 4)
    net.add_link("C", "E", 6)
    return net


# ---------------------------------------------------------------------------
# Flows do menu
# ---------------------------------------------------------------------------

def view_map_flow(net: NetworkGraph) -> None:
    display_map(net)


def calculate_route_flow(net: NetworkGraph) -> None:
    """Fluxo interativo para calcular a rota mais rapida entre dois nos."""
    start = get_router_input("No de origem: ")
    end = get_router_input("No de destino: ")
    try:
        path, latency = dijkstra(net, start, end)
        print(f"Rota: {' -> '.join(path)}, Latencia total: {latency}")
    except NoPathFoundError as error:
        print(f"[Roteamento Impossivel]: {error}")


def simulate_failure_flow(net: NetworkGraph) -> None:
    r1 = get_router_input("Roteador 1 do link: ")
    r2 = get_router_input("Roteador 2 do link: ")
    success, message = simulate_link_failure(net, r1, r2)
    print(message)
    if success:
        print("Recalculando rotas contingenciais...")


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    net = setup_initial_network()

    while True:
        show_header()
        choice = get_menu_option()

        if choice == "1":
            view_map_flow(net)
        elif choice == "2":
            calculate_route_flow(net)
        elif choice == "3":
            simulate_failure_flow(net)
        elif choice == "4":
            print("Saindo do simulador.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
