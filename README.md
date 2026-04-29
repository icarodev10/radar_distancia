# 📡 Radar de Varredura Ultrassônico (Python + Arduino)

Um radar bidimensional em tempo real inspirado em painéis de sonar e telemetria. Este projeto integra hardware (sensor ultrassônico montado sobre um eixo móvel) e software (interface gráfica de alta performance em Python) para mapear obstáculos em um arco de 180 graus.

## DEMO 📸:

https://github.com/user-attachments/assets/2fc10e39-456b-46ff-863e-22c8d3ca1a8a

## 🕹️ O Projeto
O sistema utiliza um Arduino como unidade de controle central para orquestrar o "pescoço" mecânico (Servo Motor) e os "olhos" (Sensor HC-SR04). O hardware realiza a varredura contínua do ambiente e transmite dados em coordenadas polares (Ângulo e Distância) via comunicação Serial. 

No backend, um script em Python intercepta esses pacotes, aplica matemática trigonométrica para converter os dados em coordenadas cartesianas (eixos X e Y) e renderiza um mapa visual imersivo com efeito de rastro ("fade out") nos alvos detectados.

## ⚙️ Lógica de Estados e Feedback Visual
A interface mapeia o ambiente dinamicamente. Os obstáculos encontrados geram "blips" luminosos no painel do radar, alterando seu estado de alerta e cor conforme a proximidade do alvo:

* **> 30 cm:** Seguro 🟩 (Ponto de detecção Verde)
* **Entre 15 e 30 cm:** Atenção 🟨 (Ponto de detecção Amarelo)
* **< 15 cm:** Zona de Perigo 🟥 (Ponto de detecção Vermelho)

## 🛠️ Tecnologias Utilizadas
* **Backend/Interface:** Python 3 (Bibliotecas: `pygame`, `pyserial`, `math`)
* **Hardware:** Arduino Uno
* **Componentes Físicos:** Sensor Ultrassônico HC-SR04, Micro Servo Motor SG90 (180º).

## 🚀 Como Executar
1. Instale as dependências do Python rodando no terminal: `pip install pygame pyserial`
2. Carregue o código `.ino` na placa Arduino.
3. Certifique-se de que o Monitor Serial do Arduino esteja fechado.
4. Certifique-se de que a porta COM no arquivo Python está correta (ex: `COM3`).
5. Execute o script principal (ex: `python rastreador.py`) para abrir o painel.
