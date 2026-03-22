import cv2
import numpy as np
import pyautogui
import time
import keyboard
import threading
import tkinter as tk
import csv
import datetime

# --- 1. CONSTANTES (Memória Muscular) ---
COLUNAS, LINHAS = 9, 9
ORIGEM_X, ORIGEM_Y = 751, 250
LARGURA_BLOCO, ALTURA_BLOCO = 62.75, 62.60

arquivos = {'1': '1.png', '2': '2.png', '3': '3.png', '4': '4.png', 'vazio': 'vazio.png', 'flag': 'flag.png'}
templates_carregados = {}

print("Carregando Cérebro e aplicando Corte Central...")
for nome, caminho in arquivos.items():
    img = cv2.imread(caminho)
    if img is not None:
        h, w = img.shape[:2]
        cy, cx = h // 2, w // 2
        templates_carregados[nome] = img[max(0, cy-13):cy+13, max(0, cx-13):cx+13]

# --- 2. FUNÇÃO DE RELATÓRIO (CSV) ---
def salvar_relatorio(tempo_total, matriz):
    arquivo = 'historico_partidas.csv'
    cabecalho = ('Data_Hora', 'Tempo_Segundos', 'Status', 'Minas_Restantes', 'Tabuleiro_Final')
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blocos_fechados = sum(linha.count('#') for linha in matriz)
    status = "VENCEU" if blocos_fechados == 0 else "TRAVOU_OU_PERDEU"
    matriz_str = " | ".join(" ".join(linha) for linha in matriz)
    
    try:
        arquivo_existe = False
        try:
            with open(arquivo, 'r', encoding='utf-8') as f: arquivo_existe = True
        except FileNotFoundError: pass
            
        with open(arquivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not arquivo_existe: writer.writerow(cabecalho)
            writer.writerow((agora, round(tempo_total, 2), status, blocos_fechados, matriz_str))
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

# --- 3. FUNÇÕES DE VISÃO E AÇÃO ---
def ler_tela():
    tela = pyautogui.screenshot()
    img_tela = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)
    matriz = [['#' for _ in range(COLUNAS)] for _ in range(LINHAS)]
    
    for l in range(LINHAS):
        for c in range(COLUNAS):
            x1 = int(round(ORIGEM_X + (c * LARGURA_BLOCO)))
            y1 = int(round(ORIGEM_Y + (l * ALTURA_BLOCO)))
            x2 = int(round(x1 + LARGURA_BLOCO))
            y2 = int(round(y1 + ALTURA_BLOCO))
            
            recorte = img_tela[y1:y2, x1:x2]
            
            melhor_nome, melhor_score = '#', 0.0
            for nome, temp in templates_carregados.items():
                try:
                    res = cv2.matchTemplate(recorte, temp, cv2.TM_CCOEFF_NORMED)
                    _, val_max, _, _ = cv2.minMaxLoc(res)
                    if val_max > melhor_score:
                        melhor_score = val_max
                        melhor_nome = nome
                except: pass
            
            if melhor_score >= 0.70: matriz[l][c] = melhor_nome
    return matriz

def get_vizinhos(l, c):
    vizinhos = []
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dl == 0 and dc == 0: continue
            nl, nc = l + dl, c + dc
            if 0 <= nl < LINHAS and 0 <= nc < COLUNAS: vizinhos.append((nl, nc))
    return vizinhos

def clicar(linha, coluna, botao='left'):
    centro_x = int(ORIGEM_X + (coluna * LARGURA_BLOCO) + (LARGURA_BLOCO / 2))
    centro_y = int(ORIGEM_Y + (linha * ALTURA_BLOCO) + (ALTURA_BLOCO / 2))
    pyautogui.moveTo(centro_x, centro_y, duration=0.2)
    pyautogui.mouseDown(button=botao)
    time.sleep(0.05)
    pyautogui.mouseUp(button=botao)
    time.sleep(0.1)

# --- 4. OVERLAY TRANSPARENTE ---
class OverlayMinesweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        cor_invisivel, cor_fundo = "#ABCDEF", "#1E1E1E"
        self.root.config(bg=cor_invisivel)
        self.root.attributes("-transparentcolor", cor_invisivel)
        
        pos_x = int(ORIGEM_X + (COLUNAS * LARGURA_BLOCO) + 20)
        self.root.geometry(f"+{pos_x}+{ORIGEM_Y}")
        
        self.painel = tk.Frame(self.root, bg=cor_fundo, padx=15, pady=15, relief="ridge", bd=2)
        self.painel.pack()
        
        self.label = tk.Label(self.painel, text="ESTADO: AGUARDANDO", font=("Consolas", 16, "bold"), fg="#00FF00", bg=cor_fundo)
        self.label.pack()
        self.label_tempo = tk.Label(self.painel, text="Tempo: 00:00", font=("Consolas", 14), fg="#FFFFFF", bg=cor_fundo)
        self.label_tempo.pack()
        self.label_info = tk.Label(self.painel, text="STOP: SEGURE Q", font=("Consolas", 10), fg="#AAAAAA", bg=cor_fundo)
        self.label_info.pack()

    def update_estado(self, texto, cor_texto="#00FF00"):
        self.label.config(text=f"ESTADO: {texto}", fg=cor_texto)
        self.root.update()

    def update_tempo(self, segundos):
        mins, segs = divmod(int(segundos), 60)
        self.label_tempo.config(text=f"Tempo: {mins:02d}:{segs:02d}")
        self.root.update()

    def update_info(self, texto):
        self.label_info.config(text=texto)
        self.root.update()

# --- 5. O LOOP DE INTELIGÊNCIA ---
def loop_jogo():
    try:
        print("BOT INICIADO! Vá para o jogo. Segure Q para abortar.")
        time.sleep(3)
        
        overlay.update_estado("EXECUTANDO", "#00FF00")
        inicio_tempo = time.time()
        
        # Clique Inicial
        overlay.update_info("Dando clique inicial...")
        clicar(4, 4, botao='left')
        time.sleep(1.5)
        
        jogadas_feitas = True
        while jogadas_feitas:
            overlay.update_tempo(time.time() - inicio_tempo)
            
            if keyboard.is_pressed('q'):
                overlay.update_estado("ABORTADO", "#FF0000")
                overlay.root.after(3000, overlay.root.destroy)
                return

            jogadas_feitas = False
            overlay.update_info("Lendo Tabuleiro...")
            matriz = ler_tela()
            
            overlay.update_info("Raciocinando...")
            for l in range(LINHAS):
                for c in range(COLUNAS):
                    if keyboard.is_pressed('q'): return
                    
                    celula = matriz[l][c]
                    if celula in ('1', '2', '3', '4'):
                        valor = int(celula)
                        vizinhos = get_vizinhos(l, c)
                        
                        fechados = [v for v in vizinhos if matriz[v[0]][v[1]] == '#']
                        bandeiras = [v for v in vizinhos if matriz[v[0]][v[1]] == 'flag']
                        
                        if len(fechados) > 0 and (valor - len(bandeiras)) == len(fechados):
                            for vf in fechados:
                                clicar(vf[0], vf[1], botao='right')
                                matriz[vf[0]][vf[1]] = 'flag'
                                jogadas_feitas = True
                        elif len(fechados) > 0 and len(bandeiras) == valor:
                            for vf in fechados:
                                clicar(vf[0], vf[1], botao='left')
                                jogadas_feitas = True

            if jogadas_feitas: time.sleep(0.5)

        if not keyboard.is_pressed('q'):
            tempo_final = time.time() - inicio_tempo
            salvar_relatorio(tempo_final, matriz)
            overlay.update_estado("FINALIZADO", "#0000AA")
            overlay.update_info("Dados salvos. Fechando em 5s...")
            overlay.root.after(5000, overlay.root.destroy)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        overlay.update_estado("ERRO", "#FF0000")
        overlay.root.after(5000, overlay.root.destroy)

# --- EXECUÇÃO PRINCIPAL ---
overlay = OverlayMinesweeper()
thread_jogo = threading.Thread(target=loop_jogo, daemon=True)
thread_jogo.start()
overlay.root.mainloop()