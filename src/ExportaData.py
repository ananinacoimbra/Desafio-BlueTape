import pandas as pd
import os

class ExportaData:

    def __init__(self, filename="Dados_Exportados-Casa_de_Aposta_BlueTape.xlsx"):
        self.filename = filename

    def export_to_excel(self, data_list: list):
        if not data_list:
            print("Não há dados para exportar.")
            return False
        try:
            df = pd.DataFrame(data_list)
            dir_name = os.path.dirname(self.filename)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with pd.ExcelWriter(self.filename, engine='xlsxwriter') as writer:
                if 'Periodo' in df.columns:
                    periodos = df['Periodo'].dropna().unique()
                    for periodo in periodos:
                        df_periodo = df[df['Periodo'] == periodo]                       
                        sheet_name = str(periodo).replace('/', '-').replace('\\', '-')
                        sheet_name = sheet_name[:31]
                        df_periodo.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"Dados de {periodo} exportados para aba '{sheet_name}'")
                else:
                    df.to_excel(writer, sheet_name='Dados', index=False)
                    print(" Coluna 'Periodo' não encontrada. Dados salvos em aba única 'Dados'.")
            print(f"Exportação concluída com sucesso: {self.filename}")
            return True
        except Exception as ex:
            print(f"ERRO ao exportar arquivo: {ex}")
            return False
