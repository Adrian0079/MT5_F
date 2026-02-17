#from platform_connector import PlatformConnector
from platform_connector.platform_connector import PlatformConnector



if __name__ == "__main__":
    #Definición de variables necesarias para la estrategia
    symbols = ['EURUSD', 'USDJPY']
    print("Iniciando el bot doc...")
    CONNECT = PlatformConnector(symbol_list=symbols)


