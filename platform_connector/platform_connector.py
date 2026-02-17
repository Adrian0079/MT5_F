import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv
class PlatformConnector():
    def __init__(self, symbol_list: list):
        #Buscamos el archivo .env y cargamos los valores
        load_dotenv(find_dotenv())

        #Inicialización de la plataforma
        self._initialize_platform()

        # Comprobación del tipo de cuenta 
        self._live_account_warning()
        
        #Imprimimos información de la cuenta
        self._print_account_info()

        #Comprobamos el trading algoritmico
        self._check_algo_trading_enabled()

        #Añadimos los simbolos al marketwatch
        self._add_symbols_to_marketwatch(symbol_list)

        


    def _initialize_platform(self) -> None:
        """
        Inicialización de la plataforma MT5 

        Raises:
            Exception: If there is any error while initializing the platform
            
        Return:
            None
        """
        if mt5.initialize(
            path=os.getenv("MT5_PATH"),               
            login=int(os.getenv("MT5_LOGIN")),              
            password=os.getenv("MT5_PASSWORD"),      
            server=os.getenv("MT5_SERVER"),          
            timeout=int(os.getenv("MT5_TIMEOUT")),          
            portable=eval(os.getenv("MT5_PORTABLE"))   #"False"        
        ):
            print("Éxito doc")
        else:
            # Es útil imprimir el error específico de MT5 aquí también
            print("Error detallado:", mt5.last_error())
            raise Exception(f"Ha ocurrido un error doc: {mt5.last_error()}")

    #Definimos si es desde demo o live
    def _live_account_warning(self) -> None:
        #Recuperamos el objeto de tipo AccountInfo
        account_info = mt5.account_info()

        if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("Cuenta de tipo demo!")
        elif account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            if not input("Cuenta de tipo REAL. Estaa usted arriesgando su capital. ¿Desea continuar? (y/n): " ).lower() == "y":
                mt5.shutdown()
                raise Exception("Se detuvo el META")
        else: 
            print("Cuenta de tipo Concurso/Contest")

    def _check_algo_trading_enabled(self) -> None:
        #Comprobamos que el trading algoritmico está activado

        if not mt5.terminal_info().trade_allowed:
            raise Exception("El trading algoritmico está desactivado. Porfavor activalo manualmente!")

    def _add_symbols_to_marketwatch(self, symbols: list) -> None:
        # 1) Comprobamos si el simbolo ya esta visible en el market watch
        # 2) Si no lo está lo añadimos.
        for symbol in symbols:
            if mt5.symbol_info(symbol) is None:
                print(f"No se ha podido añadir el simbolo {symbol} al MarketWatch: {mt5.last_error()}")
                continue
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol, True):
                    print(f"No se ha podido añadir el simbolo {symbol} al Marketwatch: {mt5.last_error()}")
                else:
                    print(f"Simbolo {symbol} se ha añadido correctamente al Marketwatch")
            else:
                print(f"El simbolo {symbol} ya estaba en el marketwatch")
    
    def _print_account_info(self) -> None:
        #Recuperar un objeto de tipo Account info    
        account_info = mt5.account_info()._asdict()

        print(f"+------- información de la cuenta ----------")
        print(f"Account ID: {account_info['login']}")
        print(f"Trader name: {account_info['name']}")
        print(f"Broker: {account_info['company']}")
        print(f"Server: {account_info['server']}")
        print(f"Leverage: {account_info['leverage']}")
        print(f"Divisa de la cuenta: {account_info['currency']}")
        print(f"Balance: {account_info['balance']}")
        print(f"+------- información de la cuenta -----------")

