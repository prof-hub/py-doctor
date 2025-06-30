* Nas funções `verificar_consistencia_requirements` e `atualizar_requirements`, **substitua** `codigo = fs.read_text(caminho, default="")` por `codigo = caminho.read_text(encoding="utf-8")`.
* Na função `atualizar_requirements`, **substitua** `fs.write_text(req_path, ...)` por `req_path.write_text("\n".join(novo_req) + "\n", encoding="utf-8")`.

### **Passo 3: Refatorar `cleaner.py` para Remover a Dependência de `filesystem`**

Modifique o arquivo `py_doctor/cleaner.py` de forma similar.

* **Adicione o import:** `import shutil` no topo do arquivo.
* **Remova a linha:** `import py_doctor.filesystem as fs`.
* Na função `_remover_caminho`, **substitua** a chamada `fs.remove_path(caminho)` pela seguinte lógica:
