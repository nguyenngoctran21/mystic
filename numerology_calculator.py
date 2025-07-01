# numerology_calculator.py (full version)

from typing import List, Dict, Tuple
from collections import Counter
import re

class NumerologyCalculator:
    PYTHAGOREAN_MAP = {
        'A': 1, 'J': 1, 'S': 1,
        'B': 2, 'K': 2, 'T': 2,
        'C': 3, 'L': 3, 'U': 3,
        'D': 4, 'M': 4, 'V': 4,
        'E': 5, 'N': 5, 'W': 5,
        'F': 6, 'O': 6, 'X': 6,
        'G': 7, 'P': 7, 'Y': 7,
        'H': 8, 'Q': 8, 'Z': 8,
        'I': 9, 'R': 9
    }
    VOWELS = {'A', 'E', 'I', 'O', 'U'}
    MASTER_NUMBERS = {11, 22, 33}

    def __init__(self, full_name: str, birthdate: str):
        self.name = self._validate_name(full_name)
        self.birthdate = self._validate_birthdate(birthdate)
        self.day, self.month, self.year = self._parse_birthdate()
        self.name_numbers = self._convert_name_to_numbers()
        self.letter_counts = Counter(self.name)

    def _validate_name(self, name: str) -> str:
        if not name or not isinstance(name, str):
            raise ValueError("Name cannot be empty")
        return re.sub(r"[^A-Z]", "", name.upper())

    def _validate_birthdate(self, birthdate: str) -> str:
        parts = birthdate.strip().split("/")
        if len(parts) != 3:
            raise ValueError("Invalid date format. Use dd/mm/yyyy")
        day, month, year = map(int, parts)
        return birthdate

    def _parse_birthdate(self) -> Tuple[int, int, int]:
        return tuple(map(int, self.birthdate.split("/")))

    def _reduce(self, n: int) -> int:
        if n in self.MASTER_NUMBERS:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
            if n in self.MASTER_NUMBERS:
                return n
        return n

    def _convert_name_to_numbers(self) -> List[int]:
        return [self.PYTHAGOREAN_MAP[c] for c in self.name if c in self.PYTHAGOREAN_MAP]

    def _sum_digits(self, value: int) -> int:
        return sum(int(d) for d in str(value))

    def life_path_number(self):
        return self._reduce(self._reduce(self.day) + self._reduce(self.month) + self._reduce(self.year))

    def expression_number(self):
        return self._reduce(sum(self.name_numbers))

    def soul_urge_number(self):
        vowels = [self.PYTHAGOREAN_MAP[c] for c in self.name if c in self.VOWELS and c in self.PYTHAGOREAN_MAP]
        return self._reduce(sum(vowels))

    def personality_number(self):
        consonants = [self.PYTHAGOREAN_MAP[c] for c in self.name if c not in self.VOWELS and c in self.PYTHAGOREAN_MAP]
        return self._reduce(sum(consonants))

    def birthday_number(self):
        return self._reduce(self.day)

    def maturity_number(self):
        return self._reduce(self.life_path_number() + self.expression_number())

    def balance_number(self):
        initials = [word[0] for word in self.name.split() if word]
        return self._reduce(sum(self.PYTHAGOREAN_MAP.get(c, 0) for c in initials))

    def hidden_passion_number(self):
        freq = Counter(self.name_numbers)
        max_occurrence = max(freq.values())
        return [k for k, v in freq.items() if v == max_occurrence]

    def get_all(self) -> Dict[str, any]:
        return {
            "life_path": self.life_path_number(),
            "expression": self.expression_number(),
            "soul_urge": self.soul_urge_number(),
            "personality": self.personality_number(),
            "birthday": self.birthday_number(),
            "maturity": self.maturity_number(),
            "balance": self.balance_number(),
            "hidden_passion": self.hidden_passion_number()
        }
