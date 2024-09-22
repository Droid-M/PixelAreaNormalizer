## PixelAreaNormalizer

PixelAreaNormalizer é uma ferramenta em Python que utiliza OpenCV para processar imagens, calcular a área em km² por pixel e normalizar essas áreas. O programa realiza a soma ponderada das intensidades de níveis de cinza, considerando as áreas dos pixels, ideal para análises geográficas e científicas de imagens.

## Uso da Aplicação

#### Criação do Ambiente Virtual

Para isolar as dependências do projeto, crie um ambiente virtual utilizando _venv_: `python -m venv venv`

### Ativação do Ambiente Virtual

- No Windows: `venv\Scripts\activate`
- No Linux ou macOS: `source venv/bin/activate`

### Instalar as bibliotecas necessárias

Com o ambiente virtual ativado, instale as bibliotecas requeridas usando _pip_: `pip install opencv-python numpy`

### Execução da Aplicação

Para utilizar o PixelAreaNormalizer, você deve executar o script através do terminal, passando os caminhos das imagens e as áreas correspondentes em km².

A sintaxe deve obedecer o padrão: `python main.py --imagens <caminho_da_imagem_1> <caminho_da_imagem_2> ... --areas_km <area_km1> <area_km2> …`

Por exemplo, para processar duas imagens (`Assets/1.png` e `Assets/2.png`) com áreas de 10 km² e 20 km², execute:  
`python main.py --imagens Assets/1.png Assets/2.png --areas_km 10 20`

### Observações

- Certifique-se de que as áreas correspondam ao número de imagens fornecidas. Caso contrário, a aplicação retornará um erro.
- As áreas devem ser números positivos. Áreas negativas não são aceitas.

### Registro de Logs

Os eventos e erros durante o processamento serão registrados em um arquivo chamado `processamento_imagens.log`. Verifique este arquivo para depurar ou entender melhor o que ocorreu durante a execução do programa.
