import pandas as pd

class ExportaData:
    def __init__(self, filename="Dados_Exportatos-Casa_de_Aposta_BlueTape.xlsx"):
        self.filename = filename
    def export_to_excel(self, data_list):
        if not data_list:
            print("Não há dados para exportar.")
            return

        df = pd.DataFrame(data_list)
        try:
            df.to_excel(self.filename, index=False)
            print(f"Exportação concluida, dados salvos com sucesso em {self.filename}")

        except Exception as ex:
            print(f"ERRO para exportar arquivo: {ex} ")