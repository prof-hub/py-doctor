    ```
* No bloco `try...finally` de `__main__.py`, **adicione a chamada** para a nova funcionalidade:
    ```python
    # Adicionar no bloco de condicionais em __main__.py
    from cleaner import arquivar_logs_antigos
    ...
    elif args.comando == "arquivar-logs":
        arquivar_logs_antigos(args.dias)
    ```

