2.  **Análise de Argumentos:** `__main__.py` verifica se foram passados argumentos (`diagnosticar`, `limpar`).
    * **Se sim (Modo Não Interativo):** Executa a função correspondente (`diagnosticar_projeto` ou `limpar_pycache`) e encerra.
    * **Se não (Modo Interativo):** Inicia a função `menu()`.
3.  **Carregamento da Configuração:** A função `obter_workspace` de `utils.py` é chamada.
    * Ela procura por `.pydoctor_config`.
    * Se não encontra ou o arquivo é inválido, entra em modo interativo e solicita ao usuário um caminho válido, salvando-o em um novo `.pydoctor_config`.
4.  **Menu Principal:** `menu()` lista os projetos encontrados no workspace.
5.  **Seleção de Ação:** O usuário escolhe um projeto, e `menu_acao()` é chamado, exibindo as opções: "Diagnosticar" ou "Limpar".
6.  **Execução da Tarefa:** A função correspondente de `checker.py` or `cleaner.py` é executada.
7.  **Registro de Log:** Todas as ações importantes são registradas em um arquivo na pasta `logs/`.
