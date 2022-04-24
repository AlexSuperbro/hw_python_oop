from dataclasses import dataclass, asdict, fields

from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MIN_IN_HOUR: ClassVar[float] = 60

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
        raise NotImplementedError(f'Не используем расчет калорий '
                                  f'для {self.__class__.__name__}')

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

    RUN_SPEED_COEFF1: ClassVar[float] = 18
    RUN_SPEED_COEFF2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUN_SPEED_COEFF1 * self.get_mean_speed()
                - self.RUN_SPEED_COEFF2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_WEIGHT_COEF1: ClassVar[float] = 0.035
    WALK_WEIGHT_COEF2: ClassVar[float] = 0.029
    WALK_SQUARE: ClassVar[float] = 2

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WALK_WEIGHT_COEF1 * self.weight
                + (self.get_mean_speed()**self.WALK_SQUARE // self.height)
                * self.WALK_WEIGHT_COEF2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    ADD_SPEED: ClassVar[float] = 1.1
    WEIGHT_SWIM_COEF: ClassVar[float] = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.ADD_SPEED)
                * self.WEIGHT_SWIM_COEF * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    help_read_package: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }  # словарь описание: класс
    if workout_type not in help_read_package:
        raise ValueError(workout_type)
    if len(data) != len(fields(help_read_package[workout_type])):
        raise TypeError(f'В данных тренировки {workout_type} передано '
                        f'неверное количество элементов: {len(data)} вместо '
                        f'{len(fields(help_read_package[workout_type]))}.')
    return help_read_package[workout_type](*data)


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
        try:
            main(read_package(workout_type, data))
        except ValueError as err:
            print(f'Проверьте правильность типа тренировки {err}')
        except TypeError as err1:
            print(err1)
