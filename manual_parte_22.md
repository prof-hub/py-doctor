
### **Passo 5: Adicionar Comando para Arquivar Logs**

A função `arquivar_logs_antigos` em `cleaner.py` nunca é chamada. Adicione um novo comando na CLI para executá-la.

* Em `__main__.py`, localize o bloco de `argparse` e **adicione um novo parser**:
    ```python
    # Adicionar junto aos outros parsers em __main__.py
    p_arquivar = sub.add_parser("arquivar-logs", help="Arquivar logs antigos")
    p_arquivar.add_argument("dias", type=int, help="Idade mínima em dias para arquivar os logs")
