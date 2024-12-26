from states.rj import RioDeJaneiro
from states.sp import SaoPaulo
from states.mg import MinasGerais
from states.es import EspiritoSanto

def main():
    # rj = RioDeJaneiro()
    # rj.fetch_data()
    # rj.save_to_json("outputs/rj.json")
    
    # sp = SaoPaulo()
    # sp.fetch_data()
    # sp.save_to_json("outputs/sp.json")
    
    # mg = EspiritoSanto()
    # mg.fetch_data()
    # mg.save_to_json("outputs/mg.json")
    
    es = EspiritoSanto()
    es.fetch_data()
    es.save_to_json("outputs/es.json")

if __name__ == "__main__":
    main()
