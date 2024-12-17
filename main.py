from states.rj import RioDeJaneiro

def main():
    rj = RioDeJaneiro()
    rj.fetch_data()
    rj.save_to_json("outputs/rj.json")

if __name__ == "__main__":
    main()
