from cx_Freeze import setup, Executable

# Dependências adicionais podem ser adicionadas aqui
build_exe_options = {
    "packages": ["Back", "Front", "PIL", "cv2", "numpy", "matplotlib"],  # Adicione outras bibliotecas conforme necessário
}

setup(
    name="MeuApp",
    version="0.1",
    description="Descrição do seu aplicativo",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],  # Altere conforme necessário
)