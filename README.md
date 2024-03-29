# TPPE_TP1
## ## Trabalho Prático 1 - Test-Driven Development

Trabalho pratico 1 da disciplina de técnicas de programação para plataformas emergentes

Calculadora de IPRF com funções de cadastramento de rendimentos, deduções e dependentes.


## ## Como executar os testes
- para executar a suite de testes e nescessario ter o python >= 3.6 instalado e o pytest.
- o repositório contem um arquivo requirements.txt com as dependencias necessarias para executar o projeto.
- para instalar as dependencias basta executar o comando `pip install -r requirements.txt` no terminal.
- para executar os testes basta executar o comando `pytest` no terminal.
- e possivel também utilizar o vnenv para criar um ambiente virtual para o projeto, ativar o ambiente e instalar as dependencias, para isso basta executar os seguintes comandos no terminal:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- O pytest conta com algumas opções interessantes para visualização, como o parametro -v, -s e -k, para mais informações sobre essas opções basta executar o comando `pytest --help` no terminal. ou consultar a documentação do pytest em https://docs.pytest.org/en/latest/usage.html

## ## Como executar a interface
```
python interface.py
```
Nao funciona em wsl. Pode ser necessario usar 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
![Screenshot from 2022-12-21 17-59-19](https://user-images.githubusercontent.com/42779015/209001925-5b91c67c-5fa1-4f52-8a0b-44b345ec6762.png)

## ## TP3 
O TP3 esta disponivel aqui ![TP3](https://github.com/luisgfmarques/TPPE_TP1/blob/main/TPPE%20T3.pdf).
## Marcos Gabriel Tavares - 170041042
## Luis Marques - 180105604
