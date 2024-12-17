from states.rj import RioDeJaneiro
from states.sp import SaoPaulo

def main():
    # rj = RioDeJaneiro()
    # rj.fetch_data()
    # rj.save_to_json("outputs/rj.json")
    
    sp = SaoPaulo()
    sp.fetch_data()
    sp.save_to_json("outputs/sp.json")
    

if __name__ == "__main__":
    main()
