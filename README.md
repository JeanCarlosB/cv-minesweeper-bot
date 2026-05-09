# 🤖 Agente Autônomo de Campo Minado via Visão Computacional
### *Automação de decisão em tempo real e inteligência simbólica*

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/PyAutoGUI-FFCC00?style=for-the-badge&logo=python&logoColor=yellow" alt="PyAutoGUI">
</p>

* 🎥 **Demonstração em Vídeo:** [Assista no YouTube](https://youtu.be/JeQvrYIf3p0)

## 🎯 Visão do Projeto e Valor Técnico
Este projeto implementa um agente autônomo capaz de interpretar e interagir com o clássico Campo Minado sem interceptar a memória interna do sistema. Utilizando **Visão Computacional** para percepção e **Inteligência Simbólica** para raciocínio, a solução demonstra como processos complexos de tomada de decisão podem ser automatizados de forma segura e eficiente.

## ⚙️ Destaques da Solução (Foco Builder)
* [cite_start]**Percepção Visual Não-Invasiva:** Utiliza **OpenCV** e Template Matching com calibração de malha espacial para "enxergar" o tabuleiro em tempo real[cite: 68, 101].
* [cite_start]**Raciocínio Lógico Determinístico:** Substitui tentativas aleatórias por um modelo de tomada de decisão baseado em dedução matemática, analisando matrizes $3\times3$ em torno de cada célula[cite: 69, 102].
* [cite_start]**Geração de Telemetria Contínua:** Estrutura a exportação de logs em formato **CSV**, gerando bases de dados prontas para análise de performance em ferramentas como Power BI ou dashboards em Python[cite: 70, 103].
* **Arquitetura Assíncrona:** Implementação de overlay transparente via Tkinter e Threading, permitindo monitoramento de estado em tempo real sem interromper o loop principal de automação.

## 🧠 Arquitetura do Sistema
O bot opera sobre três pilares fundamentais:
1.  **Percepção:** Algoritmo de **Corte Central Dinâmico** nos templates visuais para ignorar ruídos de borda e garantir alta precisão no reconhecimento.
2.  **Raciocínio:** Aplicação de Regras de Perigo Dedutiva e Segurança Subtrativa para identificação precisa de minas e cliques seguros.
3.  **Ação e Controle:** Controle físico do ponteiro do mouse via PyAutoGUI com um **Kill Switch** global (tecla Q) operando como Fail-Safe instantâneo.

## 🚀 Como executar o projeto
Certifique-se de ter o Python 3 instalado e siga os passos abaixo:

1.  Clone este repositório.
2.  Instale as dependências: 
    ```bash
    pip install opencv-python numpy pyautogui keyboard
    ```
3.  Garanta que os templates de imagem estão na mesma pasta do script.
4.  Abra o jogo na tela e execute:
    ```bash
    python bot_minesweeper.py
    ```

---
**Jean Carlos Barros da Mata**
*Engenheiro de Soluções Técnicas*
📧 [jeansol.dev@gmail.com](mailto:jeansol.dev@gmail.com) | 🔗 [LinkedIn](https://linkedin.com/in/jean-carlos-barros)
