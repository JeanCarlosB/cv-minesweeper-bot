# 💣 Autonomous Minesweeper Bot
* 🎥 Assista ao vídeo de demonstração no YouTube: https://youtu.be/JeQvrYIf3p0

> Um agente autônomo em Python capaz de jogar o clássico Campo Minado utilizando **Visão Computacional** e **Inteligência Simbólica**. 
> O bot lê a tela em tempo real, deduz as posições das minas usando lógica matemática, executa os cliques fisicamente e exporta a telemetria das partidas para análise de dados.

---

## 🚀 Tecnologias Utilizadas

* 🐍 **Python 3**
* 👁️ **OpenCV e NumPy:** Visão Computacional, processamento de matrizes e Template Matching.
* 🖱️ **PyAutoGUI:** Automação de interface, para o controle físico do mouse e teclado.
* 🪟 **Tkinter e Threading:** Criação de um overlay transparente assíncrono, operando em Always-on-Top, para monitoramento de estado sem interromper o loop principal.
* 📊 **CSV:** Geração de base de dados para análise de performance.

---

## 🧠 Arquitetura do Sistema

O projeto foi construído sobre três pilares fundamentais de agentes autônomos:

### 1️⃣ Percepção
O bot não lê a memória do jogo, ele enxerga a tela. 
* Utiliza calibração de malha espacial para fatiar o tabuleiro em uma matriz perfeita.
* Implementa um algoritmo de **Corte Central Dinâmico** nos templates visuais para ignorar ruídos de borda e anti-aliasing causados por transparências e anúncios no jogo, garantindo alta precisão no matchTemplate.

### 2️⃣ Raciocínio
A tomada de decisão não usa chutes, mas sim Inteligência Simbólica baseada em regras estritas aplicadas aos vizinhos em uma matriz 3x3 de cada célula:
* 🚩 **Regra de Perigo Dedutiva:** Se o número da célula for igual à quantidade de blocos fechados ao redor, todos os blocos fechados são minas e o script aplica a Flag.
* ✅ **Regra de Segurança Subtrativa:** Se a quantidade de Flags ao redor já satisfaz o número da célula, todos os blocos fechados restantes são seguros e o script aplica o Clique Esquerdo.

### 3️⃣ Ação e Telemetria
* ⚡ **Execução:** Calcula o centro geométrico do alvo e assume o controle do ponteiro do mouse.
* 🛑 **Kill Switch:** Um escutador global de teclado operando como Fail-Safe acionado pela tecla Q, interrompendo as threads instantaneamente por segurança.
* 💾 **Data Logging:** Ao final de cada execução, o estado da matriz, o tempo de processamento e o resultado da partida são exportados silenciosamente para um arquivo csv. Este pipeline prepara os dados para serem consumidos em dashboards analíticos, como no Power BI, para mapear a eficiência do algoritmo.

---

## 🛠️ Como Executar

**1.** Clone o repositório ou baixe os arquivos.

**2.** Instale as dependências executando no seu terminal:
pip install opencv-python numpy pyautogui keyboard

**3.** Certifique-se de que as imagens de template como 1.png e 2.png estão na mesma pasta do script.

**4.** Abra o Simple Minesweeper na tela e execute o script:
python bot_minesweeper.py

**5.** Solte o mouse e acompanhe o Overlay transparente! Lembre-se de segurar a tecla Q para abortar a qualquer momento.

---

## 🔮 Próximos Passos
* Implementar Algoritmo de Probabilidade Condicional para quando a lógica dedutiva falhar em situações de limite.
* Adicionar navegação autônoma de UI para clicar em "Novo Jogo" e rodar em loop infinito farmando dados.
* Construir um Dashboard em Power BI conectado ao CSV para cruzar layouts de tabuleiro que causam mais travamentos lógicos.
