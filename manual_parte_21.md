    ```python
    if caminho.is_dir():
        shutil.rmtree(caminho)
    else:
        caminho.unlink()
    ```

### **Passo 4: Deletar o Arquivo Redundante**

**Exclua** o arquivo `py_doctor/filesystem.py` do projeto. Ele não é mais necessário.
