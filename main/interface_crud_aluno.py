import curses
from crud_aluno import criar_aluno, ler_alunos, atualizar_aluno, deletar_aluno, StatusHistorico
from datetime import datetime

def main(stdscr):
    # Configurações iniciais do curses
    curses.curs_set(0)
    stdscr.clear()

    menu = ["Criar Aluno", "Listar Alunos", "Atualizar Aluno", "Deletar Aluno", "Sair"]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Sistema de Gerenciamento de Alunos", curses.A_BOLD)

        # Mostra o menu
        for idx, row in enumerate(menu):
            if idx == current_row:
                stdscr.addstr(idx + 2, 0, row, curses.color_pair(1) | curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, row)

        # Captura a entrada do usuário
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                criar_aluno_interface(stdscr)
            elif current_row == 1:
                listar_alunos_interface(stdscr)
            elif current_row == 2:
                atualizar_aluno_interface(stdscr)
            elif current_row == 3:
                deletar_aluno_interface(stdscr)
            elif current_row == 4:
                break

        stdscr.refresh()

def criar_aluno_interface(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Criar Novo Aluno")
    stdscr.addstr(1, 0, "Nome: ")
    nome = stdscr.getstr(1, 6).decode("utf-8")
    stdscr.addstr(2, 0, "Status do Histórico (1-Pronto, 2-Entregue, 3-Solicitado, 4-Falta Documentos): ")
    status = int(stdscr.getstr(2, 62).decode("utf-8"))
    status_enum = list(StatusHistorico)[status - 1]
    stdscr.addstr(3, 0, "Data de Solicitação (YYYY-MM-DD): ")
    data_solicitacao = stdscr.getstr(3, 37).decode("utf-8")
    stdscr.addstr(4, 0, "Última Série/Ano Estudado: ")
    ultima_serie = stdscr.getstr(4, 27).decode("utf-8")
    stdscr.addstr(5, 0, "Último Ano Letivo: ")
    ultimo_ano = int(stdscr.getstr(5, 21).decode("utf-8"))
    stdscr.addstr(6, 0, "Observações (opcional): ")
    observacoes = stdscr.getstr(6, 21).decode("utf-8") or None

    criar_aluno(
        nome=nome,
        status=status_enum,
        data_solicitacao=data_solicitacao,
        ultima_serie=ultima_serie,
        ultimo_ano=ultimo_ano,
        observacoes=observacoes
    )
    stdscr.addstr(8, 0, "Aluno criado com sucesso! Pressione qualquer tecla para voltar.")
    stdscr.getch()

def listar_alunos_interface(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Lista de Alunos")
    alunos = ler_alunos()
    for idx, aluno in enumerate(alunos, start=1):
        stdscr.addstr(idx, 0, f"{aluno.numero_pasta}. {aluno.nome_aluno} - {aluno.status_historico.value}")
    stdscr.addstr(len(alunos) + 2, 0, "Pressione qualquer tecla para voltar.")
    stdscr.getch()

def atualizar_aluno_interface(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Atualizar Aluno")
    stdscr.addstr(1, 0, "Número da Pasta: ")
    numero_pasta = int(stdscr.getstr(1, 18).decode("utf-8"))
    stdscr.addstr(2, 0, "Nome (deixe vazio para não alterar): ")
    nome = stdscr.getstr(2, 36).decode("utf-8") or None
    stdscr.addstr(3, 0, "Status do Histórico (1-Pronto, 2-Entregue, 3-Solicitado, 4-Falta Documentos): ")
    status = stdscr.getstr(3, 62).decode("utf-8")
    status_enum = list(StatusHistorico)[int(status) - 1] if status else None
    stdscr.addstr(4, 0, "Observações (deixe vazio para não alterar): ")
    observacoes = stdscr.getstr(4, 46).decode("utf-8") or None

    atualizar_aluno(numero_pasta, nome_aluno=nome, status_historico=status_enum, observacoes=observacoes)
    stdscr.addstr(6, 0, "Aluno atualizado com sucesso! Pressione qualquer tecla para voltar.")
    stdscr.getch()

def deletar_aluno_interface(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Deletar Aluno")
    stdscr.addstr(1, 0, "Número da Pasta: ")
    numero_pasta = int(stdscr.getstr(1, 18).decode("utf-8"))

    deletar_aluno(numero_pasta)
    stdscr.addstr(3, 0, "Aluno deletado com sucesso! Pressione qualquer tecla para voltar.")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)