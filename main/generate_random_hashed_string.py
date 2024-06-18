import hashlib
import time
class Generator:
    def __init__(self, value) -> None:
        current_time_millis = int(time.time() * 1000)

        # Concatenate current date and time with the user's email
        concatenated_string = f"{current_time_millis} {value}"

        # Apply hashing to the concatenated string
        self.hashed_string = hashlib.sha256(concatenated_string.encode()).hexdigest()

    def __str__(self) -> str:
        return str(self.hashed_string)
    