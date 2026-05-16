class MessageProcessor:
    # Respuesta comun para cualquier mensaje que no cumpla el protocolo.
    ERROR_RESPONSE = "ERROR"

    def process(self, message):
        # Todo comando valido debe separar caracteres y frase con ":".
        if ":" not in message:
            return self.ERROR_RESPONSE

        # Solo se parte por el primer ":" para permitir frases que contengan ":".
        characters_text, phrase = message.split(":", 1)

        # La parte izquierda puede contener uno o varios caracteres separados por coma.
        characters = characters_text.split(",")

        # Rechazamos listas vacias o elementos que no sean caracteres individuales.
        if not characters_text or not self._are_valid_characters(characters):
            return self.ERROR_RESPONSE

        # Construimos la respuesta respetando el orden de caracteres recibido.
        counts = []
        for character in characters:
            counts.append(f"{character}:{phrase.count(character)}")

        return ",".join(counts)

    def _are_valid_characters(self, characters):
        # Cada token debe ser exactamente un caracter: "m" vale, "mm" no.
        for character in characters:
            if len(character) != 1:
                return False
        return True
