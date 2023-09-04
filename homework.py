class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Tип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    H_M = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения. км/ч"""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Ккал"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        calories = self.get_spent_calories()
        distance = self.get_distance()
        speed = self.get_mean_speed()

        # Создаем объект класса InfoMessage и возвращаем его
        return InfoMessage(
            training_type=self.training_type,
            duration=self.duration,
            distance=distance,
            speed=speed,
            calories=calories
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.H_M
        )

    def show_training_info(self) -> InfoMessage:
        calories = self.get_spent_calories()
        distance = self.get_distance()
        speed = self.get_mean_speed()
        return InfoMessage('Бег', self.duration, distance, speed, calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_W_1 = 0.035
    COEF_W_2 = 0.029
    KMH_MS = 0.278
    CM_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM * self.KMH_MS)

    def get_spent_calories(self) -> float:
        return (
            ((self.COEF_W_1 * self.weight
              + ((self.get_mean_speed() * self.KMH_MS)**2
                 / self.height / self.CM_M)
              * self.COEF_W_2 * self.weight) * self.duration * self.H_M)
        )

    def show_training_info(self) -> InfoMessage:
        calories = self.get_spent_calories()
        distance = self.get_distance()
        speed = self.get_mean_speed()
        return InfoMessage('Спортивная ходьба', self.duration,
                           distance, speed, calories)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEF_SP = 1.1
    COEF_CAL = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_SP) * self.COEF_CAL
                * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage:
        calories = self.get_spent_calories()
        distance = self.get_distance()
        speed = self.get_mean_speed()
        return InfoMessage('Плавание', self.duration,
                           distance, speed, calories)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type in training_classes:
        training_class = training_classes[workout_type]
        return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
