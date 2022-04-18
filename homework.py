class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    min_in_hour: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        # по формуле "action * LEN_STEP / M_IN_KM"
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration  # по формуле из ТЗ
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        details = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return details


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calorie_run = ((self.coeff_calorie_1 * self.get_mean_speed()
                       - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                       * self.duration * self.min_in_hour)
        return calorie_run  # по формуле из ТЗ


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calorie_walk = ((self.coeff_calorie_3 * self.weight
                        + (self.get_mean_speed()**2 // self.height)
                        * self.coeff_calorie_4 * self.weight)
                        * self.duration * self.min_in_hour)
        return calorie_walk  # по формуле из ТЗ


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_swim = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return speed_swim
        # по формуле длина_бассейна * count_pool / M_IN_KM / время_тренировки

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calorie_swim = ((self.get_mean_speed() + self.coeff_calorie_5)
                        * self.coeff_calorie_6 * self.weight)
        return calorie_swim  # по формуле (средняя_скорость + 1.1) * 2 * вес


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dick_read_package = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }  # словарь описание: класс
    training_class = dick_read_package[workout_type]  # нашли класс по ключу
    return training_class(*data)
    # здесь возвращаем объект. *data - разбиваем список на аргументы
    # а здесь могла быть ваша реклама


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()  # вызван метод show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
