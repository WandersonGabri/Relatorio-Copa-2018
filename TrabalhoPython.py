import os
import requests
from dataclasses import dataclass

@dataclass
class Gol:
    nome_jogador: str
    minuto: int

    def __repr__(self) -> str:
        return self.nome_jogador + " " + str(self.minuto)

@dataclass
class Partida:
    numero: int
    estadio: str
    cidade: str
    mandante: str
    visitante: str
    gols_mandante: int
    gols_visitante: int
    gols: list[Gol]

    def contem(self, codigo_time: str) -> bool:
        return self.mandante == codigo_time or self.visitante == codigo_time
    
    def contem_cidade(self, ciadade_a_buscar: str) -> bool:
        return self.cidade == ciadade_a_buscar 
    
    def __repr__(self) -> str:
        return (
            self.mandante + " " + str(self.gols_mandante) 
                + " X " 
                + str(self.gols_visitante) + " " + self.visitante)

PARTIDAS: list[Partida] = []
URL: str = "https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_2018"

def load_dados():
    response = requests.get(URL)
    dados = response.json()
    rodadas = dados["rounds"]
    for rodada in rodadas:
        partidas = rodada["matches"]
        for partida in partidas:
            numero = partida["num"]
            estadio = partida["stadium"]["name"]
            cidade = partida["city"]
            mandante = partida["team1"]["code"]
            visitante = partida["team2"]["code"]
            gols_mandante = partida["score1"]
            gols_visitante = partida["score2"]

            gols: list[Gol] = []
            todos_os_gols: list[dict] = partida["goals1"] + partida["goals2"]
            for gol in todos_os_gols:
                gols.append(
                    Gol(gol["name"], gol["minute"])
                )
            
            partida: Partida = Partida(
                numero,
                estadio,
                cidade,
                mandante,
                visitante,
                gols_mandante,
                gols_visitante,
                gols,
            )

            PARTIDAS.append(partida)

def get_partidas_com_filter(codigo_time: str) -> list[Partida]:
    return list(
        filter(
            lambda time: time.contem(codigo_time), 
            PARTIDAS
        )
    )

def get_cidades_com_filter(cidade_buscada: str) -> list[Partida]:
    return list(
        filter(
            lambda cidade: cidade.contem_cidade(cidade_buscada), 
            PARTIDAS
        )
    )

def get_gols_jogador(nome_jogador: str) -> list[Gol]:
    gols_jogador: list[dict] = []
    for partida in PARTIDAS:
        for gol in partida.gols:
            if gol.nome_jogador == nome_jogador:
                gols_jogador.append(
                    {
                        "gol": gol,
                        "partida": partida,
                    }
                )

def get_partidas_por_estadio(estadio_buscado: str) -> list[Partida]:
    return list(
        filter(
            lambda partida: partida.estadio.lower() == estadio_buscado.lower(),
            PARTIDAS
        )
    )                

def get_partidas_por_vitoria_mandante() -> list[Partida]:
    partidas_vitoria_mandante: list[Partida] = []
    for partida in PARTIDAS:
        if partida.gols_mandante > partida.gols_visitante:
            partidas_vitoria_mandante.append(partida)
    return partidas_vitoria_mandante    

def get_partidas_que_deram_como_empate() -> list[Partida]:
    partidas_que_deram_empate: list[Partida] = []
    for partida in PARTIDAS:
        if partida.gols_mandante == partida.gols_visitante:
            partidas_que_deram_empate.append(partida)
    return partidas_que_deram_empate    

def get_partidas_por_vitoria_visitante() -> list[Partida]:
    partidas_vitoria_visitante: list[Partida] = []
    for partida in PARTIDAS:
        if partida.gols_mandante < partida.gols_visitante:
            partidas_vitoria_visitante.append(partida)
    return partidas_vitoria_visitante    

def jogos_por_fase(partidas, fase):
    if fase.lower() == "todos":
        return partidas
    else:
        jogos_fase = list(filter(lambda partida: partida.fase.lower() == fase.lower(), partidas))
        if jogos_fase:
            return jogos_fase
        else:
            print(f"Nenhum jogo encontrado para a fase {fase}")
            return []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("1 - Listar partidas com vitória do mandante")
    print("2 - Listar partidas que deram empate")
    print("3 - Listar partidas com vitória do visitante")
    print("4 - Buscar partidas por cidade")
    print("5 - Buscar partidas por estádio")
    print("6 - Consultar partidas por fase")
    print("7 - Sair")

def main():
    load_dados()
    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            lista_vitorias_mandante = get_partidas_por_vitoria_mandante()
            for partida in lista_vitorias_mandante:
                print(partida)
        elif choice == '2':
            lista_empates = get_partidas_que_deram_como_empate()
            for partida in lista_empates:
                print(partida)
        elif choice == '3':
            lista_vitorias_visitante = get_partidas_por_vitoria_visitante()
            for partida in lista_vitorias_visitante:
                print(partida)
        elif choice == '4':
            cidade_busca = input("Digite o nome da cidade: ")
            partidas_cidade = get_cidades_com_filter(cidade_busca)
            for partida in partidas_cidade:
                print(partida)
        elif choice == '5':
            estadio_busca = input("Digite o nome do estádio: ")
            partidas_estadio = get_partidas_por_estadio(estadio_busca)
            for partida in partidas_estadio:
                print(partida)
        elif choice == '6':
            fase_busca = input("Digite a fase desejada ('todos' para listar todas as fases): ")
            jogos_fase = jogos_por_fase(PARTIDAS, fase_busca)
            for jogo in jogos_fase:
                print(jogo)
        elif choice == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
