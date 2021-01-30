# API HTTP

Como compilar e executar?
---
A compilação é feita através do PyInstaller.  
Caso sua máquina não tenha o PyInstaller, primeiro é necessário fazer a instalação do mesmo. Esse processo ocorre através do pip, seguindo os passos abaixo:

- Passo 1:  
Em uma máquina com Python 3 instalado, abra o terminal e digite o comando abaixo, pressione enter e aguarde a instalação:  
```
pip install pyinstaller
```
- Passo 2:  
Ainda dentro do terminal, navegue até a pasta onde se encontra o arquivo **API_Escola_Alf.py**, e então execute o seguinte comando:
```
pyinstaller API_Escola_Alf.py
```
- Passo 3:  
Após encerrar o processo, feche o terminal e abra pelo explorador de arquivos a pasta onde onde se encontrava o arquivo compilado.
Você deve encontrar uma pasta chamada *dist*. Abra ela e procure pelo aplicativo ___API_Escola_Alf.exe___.

- Passo 4:  
Execute o programa. Você deverá ver uma tela semelhante a que está abaixo. Se isso acontecer, significa que ocorreu tudo certo e o programa já está rodando.  

```
 * Serving Flask app "Escola_Alf" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 335-086-224
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Funcionamento da API
---
Na tela que abre com o programa, lemos que o mesmo está sendo executado no *localhost* ("Running on http://127.0.0.1:5000").  

A API possui 8 rotas, que são acessadas quando colocadas após o endereço do *localhost*. Cada uma com uma finalidade específica, as quais estão listadas abaixo junto com seus respectivos métodos HTTP:  
  
  - **/cadastro/alunos - ("POST")** -  Serve para adicionar as informações dos alunos que fizeram as provas (id e nome).

  - **/consulta/alunos - ("GET")** - Retorna os alunos que ficaram registrados no banco de dados, após o cadastro na rota anterior.

  - **/cadastro/gabaritos - ("POST")** - Serve para adicionar as informações sobre as respostas corretas para as questões das provas.

  - **/consulta/gabaritos - ("GET")** - Retorna os gabaritos que foram registrados.

  - **/cadastro/respostas/id_aluno - ("POST")** - Cadastra as respostas de um aluno para todas as questões de todas as provas. O parâmetro *id_aluno* identifica para qual aluno estão sendo atribuídas essas respostas.

  - **/consulta/respostas/id_aluno -  ("GET")** - Retorna as respostas de um determinado aluno que foram cadastradas na rota anterior. O parâmetro *id_aluno*  aqui também identifica o aluno.

  - **/consulta/notas_finais - ("GET")** - Retorna as notas finais de todos os alunos.

  - **/consulta/aprovados - ("GET")** - Retorna os alunos aprovados (nota maior que 7) e as suas respectivas notas.

A entrada e a saída de dados ocorre por meio de JSON. Junto com o script da API no repositório público, há também 3 arquivos JSON que servem de modelo/exemplo de como deve ser formatada a requisição para cada uma das 3 rotas referentes a cadastro (alunos, gabaritos, respostas).  

Recomenda-se o uso de um software específico para testar APIs, como o Postman, que foi utilizado para testar essa.

Restrições
---
Para que o programa entenda e processe corretamente os dados que serão cadastrados, deve-se obedecer as seguintes restrições:  

- **Cadastro de alunos** :  Os alunos devem receber identificações numéricas (*"id_aluno"*) em sequência, começando no 1 e indo até 100, sem pular nenhum número. O sistema não permite cadastrar mais de 100 alunos, nem números repetidos.  
Todos os alunos deverão ser cadastrados de uma única vez. Toda vez que for envida uma requisição, o sistema exclui os dados que estavam na tabela anteriormente e escreve os dados novos. Você pode usar a **/consulta/alunos** para ver quais dados estão atualmente na tabela.  

- **Cadastro de gabaritos** : Tanto as provas quanto as questões também devem receber uma identificação numérica que inicia em 1, porém não impõe limite máximo. Deve-se respeitar a sequência prova/questão (exemplo: 1/1, 1/2, 1/3, 2/1, 2/2, 2/3, 2/4, ...).  
Aqui também deve-se cadastrar todos os gabaritos de uma única vez, o sistema exclui os dados que estavam na tabela anteriormente e escreve os dados da nova requisição. Você pode usar a ***/consulta/gabaritos*** para ver quais dados estão atualmente na tabela.  

- **Cadastro de Respostas** : Essa parte necessita um pouco mais de atenção, pois exige que além dos dados do arquivo JSON, seja inserido o parâmetro *id_aluno* no end point (exemplo: /cadastro/respostas/1, para cadastrar as respostas do aluno 1, /cadastro/respostas/2, para cadastrar as respostas do aluno 2, ...). A rota ***/consulta/respostas/id_aluno*** também exige que seja definido de que aluno deseja-se visualizar as respostas.

- **Ordem de cadastro** : Os dados devem ser cadastrados na sequência que foi passada acima (alunos -> gabaritos -> respostas), pois a última depende dos dados que virão das duas primeiras.