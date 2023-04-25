from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message_dict = {
            'training_type': f'Тип тренировки: {self.training_type}; ',
            'duration': f'Длительность: {self.duration:.3f} ч.; ',
            'distance': f'Дистанция: {self.distance:.3f} км; ',
            'speed': f'Ср. скорость: {self.speed:.3f} км/ч; ',
            'calories': f'Потрачено ккал: {self.calories:.3f}.',
        }
        return ('{training_type} {duration}'
                '{distance} {speed} {calories}'.format(**message_dict))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = 0

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        self.speed: float = self.get_distance() / self.duration
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

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        self.speed = self.get_mean_speed()
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM * self.duration
                         * self.MIN_IN_HOUR)
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMS_IN_MCH: float = 0.278
    K_1: float = 0.035
    K_2: float = 0.029
    K_3: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.calories = ((self.K_1 * self.weight
                         + ((self.get_mean_speed() * self.KMS_IN_MCH)**2
                            / (self.height / self.K_3))
                         * self.K_2 * self.weight) * self.duration
                         * self.MIN_IN_HOUR)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_4: float = 1.1
    K_5: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        self.calories = (
            self.speed + self.K_4
        ) * 2 * self.weight * self.duration
        return self.calories

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return self.speed


def read_package(workout_type: str, data: list[tuple[int,
                                                     float,
                                                     float]]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types: dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in workout_types:
        some_training: Training = workout_types[workout_type](*data)
        return some_training
    else:
        raise ValueError('Неправильный вид тренировки')


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
