# 1 - Introdução
O eletroencefalograma (EEG) é um dispositivo utilizado para o registro da atividade elétrica cerebral. Essa prática oferece uma visão única sobre processos neurológicos e cognitivos e, devido à sua segurança, alta resolução temporal e sensibilidade a mudanças dinâmicas nos sinais neurais, têm ampla aplicação em contextos clínicos e de pesquisa. Tais características tornam o EEG indispensável tanto no diagnóstico de doenças neurológicas quanto na investigação de fenômenos complexos relacionados ao funcionamento do cérebro [1,2].

Apesar da relevância, os sistemas comerciais de EEG apresentam custos elevados, o que limita sua disponibilidade em universidades e centros de pesquisa de menor porte. A título de exemplo, um Eletroencefalograma EEG de 16 canais para uso em telemedicina ocupacional usado é comercializado no Brasil por aproximadamente R$ 12.999,49 [3]. Como alternativa open hardware, a placa OpenBCI Cyton (8 canais), bastante utilizada em projetos acadêmicos e experimentais, tem preço em torno de US$ 1.249,00 (R$ 6.763,58 - Sem taxas aplicadas, convertido em 07/06/2025)[4], enquanto versões de terceiros podem ser encontradas por cerca de US$ 603,09 (R$ 3.265,85 - Sem taxas aplicadas, convertido em 07/06/2025)[5]. Ainda assim, esses valores permanecem pouco acessíveis em contextos estudantis e acadêmicos.

Durante a iniciação científica de um dos integrantes do grupo, voltada à classificação de estágios do sono a partir de sinais de EEG, surgiu o interesse em aplicar algoritmos de classificação em tempo real. No entanto, a falta de equipamentos disponíveis na universidade, somada ao alto custo de aquisição individual, motivou a busca por alternativas mais acessíveis. Foi nesse cenário que surgiu a proposta de desenvolver um sistema de EEG modular e de baixo custo, configurável em número de canais e estruturado em subsistemas que incluem: fonte de tensão simétrica, canais de coleta com condicionamento de sinal e um Digital Signal Controller (DSC) responsável pela amostragem, processamento e comunicação dos dados.

O projeto propõe-se não apenas a oferecer uma solução acessível para pesquisas acadêmicas, mas também a servir como plataforma de aprendizado em disciplinas de eletrônica, processamento digital de sinais e áreas correlatas. Além disso, seu caráter modular e open hardware abre espaço para investigações práticas sobre o porquê dos custos elevados em sistemas profissionais, ao mesmo tempo em que proporciona experiência em desenvolvimento embarcado, montagem e fabricação de placas PCB.

Dessa forma, embora iniciado em âmbito pessoal, o projeto se alinha à proposta da disciplina de Oficina de Integração, já que pode contribuir para o aprendizado coletivo do grupo, estimulando a exploração interdisciplinar e a construção de conhecimento aplicado em diferentes frentes.

# 2 - Objetivos
## 2.1 - Objetivos Gerais
Desenvolver um sistema de EEG open hardware modular, portatil, de baixo custo e fácil montagem, oferecendo maior acessibilidade em ambientes acadêmicos em relação a projetos semelhantes. O sistema será direcionado a aplicações em aulas práticas, pesquisas e desenvolvimento de projetos em universidades, com canais modulares que permitem ao usuário escolher a quantidade de canais a ser utilizada em cada situação específica.

## 2.2 - Objetivos Específicos
1. Projetar o circuito eletrônico dos canais de EEG de forma modular, capaz de captar sinais com alta sensibilidade e precisão, assegurando a integridade do sinal, permitindo a expansão ou redução do número de canais conforme a necessidade.
2. Aplicar métodos de filtragem em hardware e software para reduzir interferências e artefatos indesejados, garantindo a qualidade e confiabilidade dos dados.
3. Realizar a conversão analógico-digital dos sinais EEG captados e implementar um sistema de comunicação que permita a obtenção e processamento desses dados em tempo real em um sistema computacional.
4. Criar um manual de fácil leitura que descreva o processo de montagem do sistema e forneça instruções claras sobre seu funcionamento e utilização, garantindo que o equipamento seja acessível e compreensível para usuários, incluindo estudantes e pesquisadores.

# 3 - Metodologia
Para facilitar o desenvolvimento do sistema de EEG, o projeto foi dividido em três subsistemas: a fonte de tensão, o canal de EEG e o Digital Signal Controller (DSC).

(OBS: Inserir aqui foto do diagrama do sistema)


## 3.1 - Fonte de tensão
O sistema será alimentado por uma bateria de 9V. Considerando que o microcontrolador utilizado provavelmente opera com 3,3V, foram escolhidos amplificadores operacionais e de instrumentação compatíveis com alimentação de ±3,3V. Com isso, os parâmetros da fonte a ser projetada foram definidos da seguinte forma: entrada de 9V (da bateria) e saídas de +3,3V, -3,3V, referência de tensão e +1,65V, sendo esta última utilizada como referência de offset no circuito.

(OBS: Inserir aqui foto do circuito da fonte e gráfico da simulação)

## 3.2 - Canal de EEG
O desenvolvimento do canal do sistema começou pela identificação dos parâmetros do sinal de EEG a ser captado. Para isso, foram consultadas as obras "Clinical Electroencephalography" de O. Mecarelli [1] e "Niedermeyer's Electroencephalography: Basic Principles, Clinical Applications, and Related Fields" de E. Niedermeyer [2]. Com base nessas referências, definiram-se as seguintes características do sinal:

- A amplitude máxima de um EEG registrado no couro cabeludo de adultos varia aproximadamente entre 50 e 400 µV.
- Os sinais de EEG podem ser analisados no domínio da frequência, sendo tradicionalmente divididos em cinco bandas: delta (0,3 – 4 Hz), theta (4 – 8 Hz), alpha (8 – 13 Hz), beta (13 – 30 Hz) e gamma (30 – 80 Hz) [2, p. 134]. Além disso, há interesse crescente em componentes de frequência extremamente baixa (0 – 0,3 Hz), relevantes para diferentes pesquisas.

Com base nessas informações, os parâmetros do canal foram definidos da seguinte forma:

- Considerando que a amplitude máxima do EEG é de 400 µV, o sistema foi projetado para suportar sinais de até 400 µV acrescidos de uma margem de segurança de 400 µV, resultando em uma amplitude máxima de leitura de 800 µV.
- Como a maior frequência tradicionalmente analisada é 80 Hz, o canal foi projetado para captar sinais de até 160 Hz (2 * 80 Hz), garantindo que não haja perdas na banda de interesse.
- O filtro antialiasing do sistema é um passa-baixa de segunda ordem, com frequência de corte em 160 Hz e atenuação de aproximadamente –40 dB em 1,6 kHz. De acordo com o Teorema de Nyquist–Shannon [7], a frequência mínima de amostragem deve ser o dobro da maior frequência presente. Considerando a atenuação eficiente até 1,6 kHz, a taxa mínima de amostragem definida é de 3,2 kHz.
- O conversor A/D do DSC selecionado opera na faixa de 0 a 3,3 V. Portanto, o ganho total do canal foi calculado para que, multiplicando a amplitude máxima de leitura (800 µV) e somando um offset de 1,65 V, a saída alcance 3,3 V. O ganho resultante é aproximadamente 2062,5.

Cada canal possui duas entradas de sinal (eletrodos A e B) e quatro de alimentação (+3,3 V, –3,3 V, +1,65 V e referência). A arquitetura do canal inclui:

1. Filtro passa-alta: atenua a componente contínua do sinal.
2. Filtro rejeita-faixa centrado em 60 Hz: reduz interferências da rede elétrica.
3. Filtro passa-baixa: atua como antialiasing.
4. Circuito de offset: ajusta a tensão do sinal à faixa do conversor A/D.

Dessa forma, a saída teórica de cada canal é expressa por:

V_out = 2062,5 * (V_A - V_B) + 1,65V

(OBS: Inserir aqui foto do circuito do canal e gráfico da simulação)


## 3.3 - Digital Signal Controller (DSC)
O DSC será responsável por amostrar o sinal proveniente do canal de EEG e realizar o pré-processamento digital antes do envio ao sistema computacional. Para atender ao objetivo de portabilidade do sistema, existe uma limitação quanto à ordem dos filtros analógicos implementados, uma vez que filtros de maior ordem ocupam mais espaço no circuito. Para contornar essa restrição física, será aplicada filtragem digital de ordem superior para complementar os filtros analógicos:

- Filtro passa-alta: Fc = 150 mHz;
- Filtro rejeita-faixa: centrado em 60 Hz;
- Filtro passa-baixa: Fc = 160 Hz.

Após a passagem pelo filtro passa-baixa, será realizado o downsampling do sinal, reduzindo a quantidade de dados transmitidos ao computador e facilitando a comunicação via Bluetooth.

Embora o DSC específico ainda não tenha sido definido, prevê-se a utilização de um microcontrolador STM32 baseado na arquitetura ARM Cortex-M4. Este núcleo se destaca de outros da família Cortex-M por integrar instruções de processamento digital de sinais (DSP) em hardware [6], essenciais para aplicações de aquisição e análise de sinais biomédicos como o EEG. Diferentemente dos núcleos Cortex-M0+ ou M3, que dependem de cálculos via software, o Cortex-M4 oferece operações single-cycle, como Multiply-Accumulate (MAC) e SIMD (Single Instruction, Multiple Data) [7], permitindo a execução eficiente de algoritmos de filtragem digital.

(OBS: Inserir aqui foto do subsistema do DSC no diagrama)

# Cronograma

# Referências 
[1] O. Mecarelli, Org., Clinical Electroencephalography, Springer International Publishing (2019).  
[2] E. Niedermeyer, D. L. Schomer, e F. H. L. da Silva, Niedermeyer's Electroencephalography: Basic Principles, Clinical Applications, and Related Fields, 6ª ed., Wolters Kluwer/Lippincott Williams & Wilkins Health (2011).  
[3] Mercado Livre. Eletroencefalograma EEG 16 Canais Telemedicina Ocupacional. Disponível em: https://produto.mercadolivre.com.br/MLB-4503980046-eletroencefalograma-eeg-16-canais-telemedicina-ocupacional-_JM?matt_tool=18956390&utm_source=google_shopping&utm_medium=organic. Acesso em: 07 set. 2025.  
[4] OpenBCI. Cyton Biosensing Board (8-channels). Disponível em: https://shop.openbci.com/products/cyton-biosensing-board-8-channel. Acesso em: 07 set. 2025.  
[5] eBay. OpenBCI V3 EEG Copia. Disponível em: https://www.ebay.com/itm/157280657975?chn=ps&google_free_listing_action=view_item. Acesso em: 07 set. 2025.  
[6] ARM. Cortex-M4. Disponível em: https://www.arm.com/products/silicon-ip-cpu/cortex-m/cortex-m4. Acesso em: 07 set. 2025.  
[7] QCENTLABS. The Core Wars, ARM Cortex M0+ vs M3 vs M4 vs M7. Disponível em: http://qcentlabs.com/posts/cortex-wars/. Acesso em: 07 set. 2025.
