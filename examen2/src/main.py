from src.server import UDPInfoServer


def main():
    """Arranca el servidor UDP con los valores por defecto del contrato."""
    server = UDPInfoServer()
    server.run()


if __name__ == "__main__":
    main()
