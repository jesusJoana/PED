import unittest


class TestMessageProcessor(unittest.TestCase):
    """Pruebas unitarias del protocolo usado por el servidor."""

    def setUp(self):
        from src.protocol import MessageProcessor

        self.processor = MessageProcessor()

    # Iteracion 1 - Test 1 Unitario
    # Requisito: el servidor responde al formato c:Frase con c:numero.
    def test_single_character_message_counts_occurrences(self):
        response = self.processor.process("m:combinaciones momentaneas de palabras")

        self.assertEqual("m:3", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: el servidor responde al formato c1,c2,...,cm:Frase con el
    # conteo de cada caracter, manteniendo el orden recibido.
    def test_multiple_character_message_counts_each_character(self):
        response = self.processor.process(
            "m,e,z:Combinaciones momentaneas de palabras"
        )

        self.assertEqual("m:3,e:4,z:0", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: cualquier mensaje que no respete el formato esperado devuelve
    # ERROR.
    def test_message_without_separator_returns_error(self):
        response = self.processor.process("mensaje incorrecto")

        self.assertEqual("ERROR", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: una lista vacia de caracteres no es un comando valido.
    def test_empty_character_list_returns_error(self):
        response = self.processor.process(":frase sin caracter")

        self.assertEqual("ERROR", response)

    # Iteracion 1 - Test 1 Unitario
    # Requisito: cada elemento de la lista debe ser un unico caracter.
    def test_character_token_with_more_than_one_character_returns_error(self):
        response = self.processor.process("mm:frase con formato invalido")

        self.assertEqual("ERROR", response)


if __name__ == "__main__":
    unittest.main()
