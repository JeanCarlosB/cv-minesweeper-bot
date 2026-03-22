# Autonomous Minesweeper Bot

Um agente autônomo em Python capaz de jogar o clássico Campo Minado utilizando **Visão Computacional** e **Inteligência Simbólica**. O bot lê a tela em tempo real, deduz as posições das minas usando lógica matemática, executa os cliques fisicamente e exporta a telemetria das partidas para análise de dados.

## Tecnologias Utilizadas
* **Python 3**
* **OpenCV (`cv2`) & NumPy:** Visão Computacional, processamento de matrizes e Template Matching.
* **PyAutoGUI:** Automação de interface (controle físico de mouse e teclado).
* **Tkinter & Threading:** Criação de um overlay transparente assíncrono (Always-on-Top) para monitoramento de estado sem interromper o loop principal.
* **CSV:** Geração de base de dados para análise de performance.

## Arquitetura do Sistema

O projeto foi construído sobre três pilares fundamentais de agentes autônomos:

### 1. Percepção (Computer Vision)
O bot não lê a memória do jogo, ele "enxerga" a tela. 
* Utiliza calibração de malha espacial para fatiar o tabuleiro em uma matriz perfeita.
* Implementa um algoritmo de **Corte Central Dinâmico** nos templates visuais para ignorar ruídos de borda e anti-aliasing (causados por transparências e anúncios no jogo), garantindo alta precisão no `cv2.matchTemplate`.

### 2. Raciocínio (Constraint Satisfaction Problem)
A tomada de decisão não usa "chutes", mas sim Inteligência Simbólica baseada em regras estritas aplicadas aos vizinhos (Matriz 3x3) de cada célula:
* **Regra de Perigo (Dedutiva):** Se o número da célula for igual à quantidade de blocos fechados ao redor, todos os blocos fechados são minas (Aplica *Flag*).
* **Regra de Segurança (Subtrativa):** Se a quantidade de *Flags* ao redor já satisfaz o número da célula, todos os blocos fechados restantes são seguros (Aplica *Clique Esquerdo*).

### 3. Ação & Telemetria
* **Execução:** Calcula o centro geométrico do alvo e assume o controle do ponteiro do mouse.
* **Kill Switch:** Um escutador global de teclado (`keyboard`) operando como *Fail-Safe* acionado pela tecla `Q`, interrompendo as threads instantaneamente por segurança.
* **Data Logging:** Ao final de cada execução, o estado da matriz, o tempo de processamento e o resultado (Vitória/Travamento) são exportados silenciosamente para um arquivo `.csv`. Este pipeline prepara os dados para serem consumidos em dashboards analíticos (Power BI) para mapear a eficiência do algoritmo.

## Como Executar

1. Clone o repositório.
2. Instale as dependências: `pip install opencv-python numpy pyautogui keyboard`
3. Certifique-se de que as imagens de template (`1.png`, `2.png`, etc.) estão na raiz do diretório.
4. Abra o Simple Minesweeper na tela e execute o script (preferencialmente como Administrador para liberar os cliques profundos do PyAutoGUI).
5. Solte o mouse e acompanhe o Overlay transparente! (Segure `Q` para abortar).
