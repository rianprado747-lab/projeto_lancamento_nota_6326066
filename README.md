### 📚 Bibliotecas Necessárias
Para que a automação execute corretamente, certifique-se de que o ambiente possui as seguintes bibliotecas instaladas e importadas:
* `pyautogui`
* `webbrowser`
* `time` (nativa do Python)
* `pandas` (importada como `pd`)
* `numpy` (importada como `np`)
* `os` (nativa do Python)

### ⚠️ IMPORTANTE: Estrutura do Formulário
> O Google Forms utilizado como simulador do sistema legado **deve obrigatoriamente** seguir a exata ordem abaixo para o preenchimento correto das informações pelo robô:
> 
> `nome` ➔ `ra` ➔ `nota1` ➔ `tf01` ➔ `nota2` ➔ `tf02` ➔ `nf1` ➔ `nf2` ➔ `media` ➔ `situacao`

### 🚀 Como Usar o Script
1. Abra o arquivo principal do código.
2. Localize a variável `link` e defina-a com a URL do seu Google Forms.
3. Localize a variável `tabela_alunos` e insira o caminho correto do seu arquivo `.csv` de testes.
4. Execute o script e siga as instruções no terminal.
