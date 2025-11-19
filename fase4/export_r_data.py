import sqlite3
import pandas as pd
import os

def export_data():
    print("Conectando ao banco de dados...")
    # Caminho absoluto ou relativo da raiz
    db_path = "farm.db"
    conn = sqlite3.connect(db_path)
    
    # Query simplificada para garantir que o R tenha dados legíveis
    # Pegamos todas as leituras e deixamos o R filtrar/agrupar se quiser, 
    # ou fazemos um pivot simples aqui.
    query = """
        SELECT 
            sec.name as sector, 
            sec.crop_type,
            s.type as sensor_type,
            r.value,
            r.recorded_at
        FROM sensor_readings r
        JOIN sensors s ON r.sensor_id = s.id
        JOIN sectors sec ON s.sector_id = sec.id
    """
    
    print("Extraindo dados...")
    try:
        df = pd.read_sql_query(query, conn)
        
        # Pivot para ter colunas: sector, crop_type, co2, luminosity, density
        # Isso facilita a correlação no R
        df_pivot = df.pivot_table(index=['sector', 'crop_type', 'recorded_at'], 
                                columns='sensor_type', 
                                values='value').reset_index()
        
        # Renomear colunas para bater com o script R (co2_emission -> co2)
        df_pivot.rename(columns={
            'co2_emission': 'co2', 
            'luminosity': 'luminosity', 
            'crop_density': 'density'
        }, inplace=True)
        
        # Preencher NaNs (timestamps podem variar milissegundos) com forward fill
        df_pivot.fillna(method='ffill', inplace=True)
        df_pivot.fillna(method='bfill', inplace=True) # Para os primeiros
        
        output_path = "fase4/sensor_data.csv"
        df_pivot.to_csv(output_path, index=False)
        print(f"Dados exportados para: {output_path}")
        print(df_pivot.head())
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_data()
