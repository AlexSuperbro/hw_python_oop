from dataclasses import dataclass, asdict, field

from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: float = field(default=1000, init=False)
    MIN_IN_HOUR: float = field(default=60, init=False)

    action: float
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Не используем расчет калорий для Training')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = field(default=18, init=False)
    COEFF_CALORIE_2: float = field(default=20, init=False)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: float = field(default=0.035, init=False)
    COEFF_CALORIE_4: float = field(default=0.029, init=False)

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_3 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_4 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = field(default=1.38, init=False)
    COEFF_CALORIE_5: float = field(default=1.1, init=False)
    COEFF_CALORIE_6: float = field(default=2, init=False)

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                * self.COEFF_CALORIE_6 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    help_read_package: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }  # словарь описание: класс
    try:
        return help_read_package[workout_type](*data)
    except KeyError:
        raise KeyError('Проверьте правильность типа тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
