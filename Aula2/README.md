## Exercício 2

### Dependências:
*  CoAPthon
*  SenseHat emulator

### Diagrama:
![diagram](https://github.com/juanlucasvieira/IoT2020.1/blob/master/Aula2/diagram.png)

* Ao iniciar o **Cliente CoAP**, o usuário passará como parâmetros a temperatura e pressão que deseja setar como limiar. 
  - Esses limiares serão **enviados** ao Servidor CoAP, através de uma mensagem PUT /threshold.
  - O Cliente também irá enviar uma requisição para **observar** mudanças no recurso threshold.
  - Quando uma notificação de modificação do Threshold - *por outro cliente* - for recebida, o cliente exibe os novos valores de Limiar.
  - O usuário pode optar por sobrescrever o Limiar ao entrar no teclado o comando **OVERWRITE**.
* O **Servidor CoAP**, expõe o recurso Threshold, que armazena um limiar de temperatura e pressão.
  - Sempre que o valor do recurso Threshold é alterado, o servidor **notifica** clientes que estão observando o recurso. 
  - O servidor recebe os valores de temperatura e pressão reportados pelo sensor SenseHat.
  - Se os **valores de temperatura e pressão reportados forem maiores que os armazenados no recurso Threshold**, o servidor executa um comando para acender todos os LEDs do **SenseHat** na cor vermelha.

## Instalação
- Baixar [**master.zip**](https://github.com/juanlucasvieira/IoT2020.1/archive/master.zip)
- Descompactar arquivo .zip

## Execução
Para executar o **servidor**, abra o terminal no diretório Aula2 e digite o comando:

```python coap_server.py```

Para executar o **cliente**, abra o terminal no diretório Aula2 e digite o comando:

```python coap_client.py -a <ip_servidor> -t <limiar_temperatura> -p <limiar_pressão>```

**Exemplo**: ```python coap_client.py -a localhost -t 25 -p 500```

## Exemplo de Execução

![screenshot](https://github.com/juanlucasvieira/IoT2020.1/blob/master/Aula2/screenshot.png)
