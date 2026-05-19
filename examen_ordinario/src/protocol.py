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

        return ",".join(self._format_count(letter, phrase) for letter in letters)

    def _valid_letters(self, letters):
        if not letters:
            return False

        for letter in letters:
            if len(letter) != 1:
                return False

        return True

    def _format_count(self, letter, phrase):
        return f"{letter}:{phrase.count(letter)}"
