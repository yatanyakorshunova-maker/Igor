"""Игровая логика цифрового питомца без зависимости от Kivy."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Dict


def clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    """Ограничивает число заданным диапазоном."""
    return max(minimum, min(maximum, int(value)))


@dataclass
class PetModel:
    name: str = "Бруно"
    species: str = "такса"
    character: str = "весёлый"
    favorite_food: str = "пицца"
    satiety: int = 50
    mood: int = 50
    energy: int = 50
    coins: int = 0
    actions: int = 0
    reward_received: bool = False
    sleeping: bool = False

    @property
    def level(self) -> int:
        return 1 + self.actions // 5

    def normalize(self) -> None:
        self.satiety = clamp(self.satiety)
        self.mood = clamp(self.mood)
        self.energy = clamp(self.energy)
        self.coins = max(0, int(self.coins))
        self.actions = max(0, int(self.actions))

    def feed(self) -> str:
        if self.sleeping:
            return "Питомец спит. Подождите пробуждения."
        self.satiety += 20
        self.mood += 5
        self.coins += 2
        self.actions += 1
        self.normalize()
        return "Спасибо! Было очень вкусно."

    def play(self) -> str:
        if self.sleeping:
            return "Питомец спит. Подождите пробуждения."
        self.mood += 20
        self.energy -= 15
        self.satiety -= 5
        self.coins += 3
        self.actions += 1
        self.normalize()
        return "Отличная игра! Давайте ещё раз."

    def start_sleep(self) -> str:
        if self.sleeping:
            return "Питомец уже спит."
        self.sleeping = True
        self.actions += 1
        return "Тихо... Питомец засыпает."

    def finish_sleep(self) -> str:
        self.energy += 30
        self.satiety -= 10
        self.coins += 1
        self.sleeping = False
        self.normalize()
        return "Питомец проснулся и снова полон сил."

    def passive_tick(self) -> str:
        """Небольшое естественное снижение показателей."""
        if self.sleeping:
            return "Питомец спокойно спит."
        self.satiety -= 2
        self.mood -= 1
        self.energy -= 1
        self.normalize()
        return self.status_message()

    def image_state(self) -> str:
        if self.sleeping:
            return "sleep"
        if self.satiety < 25:
            return "hungry"
        if self.energy < 25:
            return "tired"
        if self.mood < 30:
            return "sad"
        if self.mood >= 80:
            return "happy"
        return "normal"

    def status_message(self) -> str:
        state = self.image_state()
        messages = {
            "sleep": "Питомец сладко спит.",
            "hungry": "Я очень голоден. Пора перекусить!",
            "tired": "Сил почти не осталось. Мне нужен сон.",
            "sad": "Мне немного грустно. Давайте поиграем.",
            "happy": "У меня прекрасное настроение!",
            "normal": "Всё хорошо. Что будем делать?",
        }
        return messages[state]

    def check_reward(self) -> bool:
        """Выдаёт награду ровно один раз и сообщает, выдана ли она сейчас."""
        goal_reached = self.satiety >= 80 and self.mood >= 80 and self.energy >= 80
        if goal_reached and not self.reward_received:
            self.reward_received = True
            self.coins += 100
            return True
        return False

    def reset(self, keep_name: bool = True) -> None:
        name = self.name
        fresh = PetModel()
        self.__dict__.update(fresh.__dict__)
        if keep_name:
            self.name = name

    def to_dict(self) -> Dict[str, Any]:
        self.normalize()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PetModel":
        allowed = {field.name for field in fields(cls)}
        clean = {key: value for key, value in data.items() if key in allowed}
        model = cls(**clean)
        # После перезапуска приложение не должно оставлять питомца в заблокированном сне.
        model.sleeping = False
        model.normalize()
        return model
