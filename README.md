<a name="readme-top"></a>

# Cloud-logger-AAIB
Repositório com os ficheiros referentes ao trabalho alternativo da UC AAIB (FCT-NOVA) 2022/2023.

## Sobre o projeto

O objetivo deste trabalho passou pela criação de um sistema "data logger" de áudio proveniente do microfone do computador. Os dados adquiridos são exibidos em "real time" numa página desenvolvida em "Streamlit" sob a forma de gráficos, com a possibilidade de gravar os mesmos ou abrir os dados de uma outra sessão.

### Diagrama da arquitetura do sistema

![image](https://user-images.githubusercontent.com/117983623/204655626-318ce1fc-f8ab-4fa3-8e32-65743d0d385a.png)

A aquisição de aúdio proveniente do microfone é iniciada quando o utilizador clica no botão "Start" na página web. Quando isto acontece é publicada uma mensagem com valor "True" para o tópico "Status" que é recebida pelo cliente executado no computador, que por sua vez começa a publicar os dados do aúdio para o tópico "SoundSigAAIB".
Os dados são depois recebidos pelo cliente em execução no gitpod e guardados sucessivamente num ficheiro .txt, a aplicação web no streamlit lê o último valor colocado neste ficheiro e constroí o gráfico de Sonograma do aúdio recolhido.
A aquisição de aúdio é terminada após ser pressionado o botão "Stop".

## Requisitos

* MQTT Paho
* MQTT mosquitto
* Streamlit
* Pyaudio

## Get Started

Para começar é necessário criar um workspace no Gitpod com os ficheiros deste repositório. A instalação de todos os requisitos incluídos no ficheiro .gitpod.yml é feita automaticamente.
Após terminada a instalação a página web é aberta numa nova janela e o subscriber.py encontra-se disponível para receber dados. O próximo passo é correr o ficheiro publisher.py no prompt do computador. 
Completos todos estes passos, pode-se iniciar a aquisição de áudio clicando no botão "Start" da página web.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Cloud-logger-AAIB)

<!-- CONTACTOS -->
## Contactos

Tiago Batista - ts.batista@campus.fct.unl.pt



<p align="right">(<a href="#readme-top">back to top</a>)</p>
