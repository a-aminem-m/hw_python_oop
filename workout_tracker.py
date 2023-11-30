class InfoMessage:
    """Training information."""
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
        return (f'Type of workout: {self.training_type}; '
                f'Duration: {self.duration:.3f} ч.; '
                f'Distance: {self.distance:.3f} км; '
                f'Average speed: {self.speed:.3f} км/ч; '
                f'Kilocalories burned: {self.calories:.3f}.')


class Training:
    """Basic training class."""
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
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average driving speed. km/h"""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """ПGet the number of calories burned. Kcal"""
        raise NotImplementedError("The get_spent_calories method "
                                  "is overridden in child classes.")
        

    def show_training_info(self) -> InfoMessage:
        """Return an information message about the completed workout."""
        calories = self.get_spent_calories()
        distance = self.get_distance()
        speed = self.get_mean_speed()
        # Create an object of the InfoMessage class and return it
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=distance,
            speed=speed,
            calories=calories
        )


class Running(Training):
    """Workout: running."""
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


class SportsWalking(Training):
    """Workout: race walking."""
    COEF_W_1 = 0.035
    COEF_W_2 = 0.029
    KMH_MS = 0.278
    CM_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_spent_calories(self) -> float:
        speed_ms = self.get_mean_speed() * self.KMH_MS
        duration_m = self.duration * self.H_M
        height_m = self.height / self.CM_M
        return (
            ((self.COEF_W_1 * self.weight
              + (speed_ms**2 / height_m) * self.COEF_W_2 * self.weight)
             * duration_m)
        )


class Swimming(Training):
    """Workout: swimming."""
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


def read_package(workout_type: str, data: list) -> Training:
    """Read data received from sensors."""
    training_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type in training_classes:
        training_class = training_classes[workout_type]
        return training_class(*data)
    else:
        raise ValueError(f"The '{workout_type}' workout type is not supported.")


def main(training: Training) -> None:
    """Main function."""
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
