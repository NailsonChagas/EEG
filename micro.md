# STM32 Arm Cortex-M4

| Característica                  | STM32G474RE                     | STM32G431RB                     | STM32L471VG                    | Observações                                 |
| :------------------------------ | :------------------------------ | :------------------------------ | :----------------------------- | :------------------------------------------ |
| **Família / Foco**              | Alta Performance & Analog       | Performance & Analog            | **Ultra Baixo Consumo**        | **L4 é focado em eficiência energética**    |
| **Núcleo**                      | Cortex-M4 com FPU @ **170 MHz** | Cortex-M4 com FPU @ **170 MHz** | Cortex-M4 com FPU @ **80 MHz** | G4 tem mais que o dobro da velocidade       |
| **Flash Memory**                | 512 KB                          | 128 KB                          | **1 MB**                       | **L471 tem a maior memória Flash**          |
| **SRAM**                        | 128 KB                          | 32 KB                           | 128 KB                         | G474 e L471 empatam em SRAM                 |
| **Acceleradores Matemáticos**   | **CORDIC e FMAC**               | **CORDIC e FMAC**               | Não                            | **Exclusivo das famílias G4**               |
| **Consumo (Run Mode)**          | \~100 µA/MHz (est.)             | \~100 µA/MHz (est.)             | **100 µA/MHz**                 | Similar em operação ativa                   |
| **Modo Stop (Typ.)**            | \~30 µA (Stop 0)                | \~30 µA (Stop 0)                | **1.1 µA (Stop 2)**            | **L4 é ordens de magnitude mais eficiente** |
| **Modo Standby (Typ.)**         | \~500 nA                        | \~500 nA                        | **120 nA**                     | **L4 é muito mais eficiente em standby**    |
| **ADCs (12-bit)**               | **5x (4 Msps)**                 | 2x (4 Msps)                     | 3x (5 Msps)                    | G4 tem mais ADCs, L4 tem maior velocidade   |
| **DACs (12-bit)**               | **7x**                          | 4x                              | 2x                             | **G474 domina em DACs**                     |
| **Comparadores**                | **7x**                          | 4x                              | 2x                             | **G474 domina em comparadores**             |
| **Amplificadores Operacionais** | **6x**                          | 3x                              | 2x                             | **G474 domina em OPAMPs**                   |
| **Timer HRTIM**                 | **Sim (184 ps)**                | Não                             | Não                            | **Exclusivo do G474**                       |
| **Interfaces CAN**              | **3x FDCAN**                    | 1x FDCAN                        | 1x CAN 2.0B                    | G4 tem CAN mais moderno (FD)                |
| **Interfaces I²C**              | 4x                              | 3x                              | 3x                             | G474 tem mais I²C                           |
| **Interfaces SPI**              | 4x                              | 3x                              | 3x + 1x Quad-SPI               | Similar                                     |
| **Interfaces USART/UART**       | 6x                              | 5x                              | **6x**                         | Similar                                     |
| **Interface USB**               | Device FS                       | Device FS                       | Device FS                      | Similar                                     |
| **Controlador UCPD**            | Sim                             | Sim                             | Não                            | **Exclusivo das famílias G4**               |
| **Interface Memória Externa**   | **FSMC + Quad-SPI**             | Não                             | **FSMC + Quad-SPI**            | G474 e L471 suportam memória externa        |
| **DMA**                         | 16 canais                       | 12 canais                       | 14 canais                      | Similar                                     |
| **Capacitive Sensing**          | Não                             | Não                             | **Sim (24 canais)**            | **Exclusivo do L471**                       |
| **DFSDM**                       | Não                             | Não                             | **4x Filtros**                 | **Exclusivo do L471** (para ADC digital)    |
| **Pinos (Pacotes)**             | Até 128 pinos                   | Até 100 pinos                   | Até 100 pinos                  | G474 oferece o pacote maior                 |

### STM32G474RE
A **escolha para performance e controle**. Ideal para aplicações que demandam:
* Suporta ADC oversampling via hardware
* Alta velocidade de processamento (**170 MHz**).
* Periféricos analógicos avançados e numerosos (**ADCs, DACs, OPAMPs, COMPs**).
* Controle preciso de potência com **HRTIM**.
* Comunicação industrial robusta com múltiplos **FDCAN**.

### STM32G431RB
A **versão econômica do G4**. Boa escolha quando se precisa do:
* Suporta ADC oversampling via hardware
* Núcleo rápido com **instruções DSP** e **aceleradores matemáticos**.
* Recursos analógicos razoáveis, mas sem exageros.
* Custo mais baixo em comparação ao G474.

### STM32L471VG
A **escolha para eficiência energética e duração de bateria**. Destaques:
* **Ultra baixo consumo** em Stop (1.1 µA) e Standby (120 nA).
* Até **1 MB de memória Flash**.
* Recursos adicionais como **Capacitive Sensing (24 canais)** e **DFSDM** para filtragem digital de sinais.
* Indicado para:
  * Dispositivos portáteis e movidos a bateria.
  * Sensores que passam a maior parte do tempo em modo de baixo consumo.
  * Aplicações que exigem longa autonomia.