class LetterCountProtocol:
    """Procesa los mensajes del protocolo de conteo de letras."""

    ERROR_RESPONSE = "ERROR"

    def process(self, message):
        if ":" not in message:
            return self.ERROR_RESPONSE

        letters_part, phrase = message.split(":", 1)
        letters = letters_part.split(",")

        if not self._valid_letters(letters):
            return self.ERROR_RESPONSE

        counts = []
        for letter in letters:
            counts.append(f"{letter}:{phrase.count(letter)}")

        return ",".join(counts)

    def _valid_letters(self, letters):
        if not letters:
            return False

        for letter in letters:
            if len(letter) != 1:
                return False

        return True
