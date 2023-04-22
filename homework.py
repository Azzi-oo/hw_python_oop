M_IN_KM: int = 1000
MIN_IN_HOUR = 60
SEC_IN_HOUR = 3600
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79
a = 0.035
b = 0.029
c = 1.1


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.2f} ч.; '
                f'Дистанция: {self.distance:.2f} км; '
                f'Ср.скорость: {self.speed:.2f} км/ч; '
                f'Потрачено ккал: {self.calories:.2f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance: float = self.action * self.LEN_STEP / M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed: float = self.distance / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        self.calories = ((CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                         + CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / M_IN_KM * self.duration)
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        b1: float = ((self.distance * M_IN_KM)
                     / (self.duration * SEC_IN_HOUR))
        self.calories = (((a * self.weight + (b1**2 / self.height)
                          * b * self.weight) * (self.duration * MIN_IN_HOUR)))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        self.calories = (self.speed + c) * 2 * self.weight * self.duration
        return self.calories

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / M_IN_KM / self.duration)
        return self.speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in workout_types:
        some_training: Training = workout_types[workout_type](*data)
        return some_training
    else:
        print('incorrect package')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
