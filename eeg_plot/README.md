# EEG Plot
Sistema para aquisição, visualização e gravação de sinais EEG (eletroencefalográficos) em tempo real via UART, com visualização gráfica dos sinais e de suas FFTs (em dB) usando **PyQtGraph** e **PyQt5**.

## Estrutura do Projeto
```
eeg_plot/
│
├── src/
│   ├── serial_reader.py    
│   ├── eeg_window.py       
│   └── utils.py             
├── output/                  # Diretório onde os arquivos CSV são salvos
├── main.py                  
├── requirements.txt         # Dependências do projeto
├── .gitignore              
└── README.md               
```

## Funcionalidades

- **Leitura serial contínua** de dois canais EEG via UART.  
- **Gravação automática** dos dados em arquivo `.csv` (opcional).  
- **Visualização em tempo real** dos sinais no domínio do tempo e frequência.  
- **Cálculo automático da FFT** em dB para cada canal.  

## Requisitos
Antes de executar o projeto, certifique-se de ter:

- Python **3.8+**
- Instalado as dependências:
    - Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt
        ```
    - Ubuntu:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
- Sistema Linux (ou WSL) com os pacotes gráficos instalados:
    ```bash
    sudo apt install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
                    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
                    libxcb-render-util0
    ```

**Obs:** Gere o arquivo `requirements.txt` novamente após ajustes:
```bash
pip freeze > requirements.txt
```

## Execução
```bash
python3 main.py
```

O programa listará as portas seriais disponíveis. Escolha a porta correspondente ao seu dispositivo EEG (por exemplo, `/dev/ttyUSB0`).

Em seguida, você poderá optar por salvar os dados recebidos em um arquivo CSV dentro da pasta `output/`.


## Salvamento de Dados
- Os dados são armazenados em **buffer** e escritos periodicamente (por padrão, a cada 10 segundos).
- O arquivo é salvo na pasta `output/` com nome no formato:
  ```
  eeg_data_YYYYMMDD_HHMMSS.csv
  ```
- Colunas do CSV:
  ```
  timestamp, ch1_uV, ch2_uV
  ```

## Comunicação Serial
O protocolo de transmissão via UART segue o seguinte formato de pacote:

|   Byte   |                  Descrição                      | 
|----------|-------------------------------------------------| 
|     $    |                 Byte inicial                    | 
|  8 bytes | Dados (<ff) - 2 floats (ch1, ch2) little endian |
|    \n    |                  Byte final                     |


A conversão dos valores de tensão para microvolts (µV) é feita conforme a equação:

```
EEG (µV) = (V - 1.65) * (1 / 2062.5) * 1e6
```

O valor **1.65 V** representa o *offset* introduzido pelo circuito de condicionamento, enquanto **2062.5** corresponde ao ganho total do sistema de aquisição.
