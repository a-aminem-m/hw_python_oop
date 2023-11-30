# Workout Tracker

###### (This project was developed during the "Python Developer" training program at [Yandex.Practicum](https://practicum.yandex.ru/), as a part of the learning curriculum.)

## Description
This project is a workout tracker written in Python. It provides basic classes for various types of workouts and allows for the analysis of sensor data, displaying information about completed workouts.

## Project Structure

### Classes

#### `InfoMessage`
Class for creating informational messages about workouts.

```python
class InfoMessage:
    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float) -> None:
        # ...

    def get_message(self) -> str:
        # ...
```
#### `Running`
Class for running workouts, inherited from Training.

```python
class Running(Training):
    def get_distance(self) -> float:
        # ...

    def get_spent_calories(self) -> float:
        # ...

```

#### `SportsWalking`
Class for sports walking workouts, inherited from Training.

```python
class SportsWalking(Training):
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        # ...

    def get_distance(self) -> float:
        # ...

    def get_spent_calories(self) -> float:
        # ...
```

#### `Swimming`
Class for swimming workouts, inherited from Training.

```python
class Swimming(Training):
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        # ...

    def get_distance(self) -> float:
        # ...

    def get_mean_speed(self) -> float:
        # ...

    def get_spent_calories(self) -> float:
        # ...

```

### Functions

#### read_package
Function to read sensor data and create an instance of the corresponding workout class.

```python
def read_package(workout_type: str, data: list) -> Training:
    # ...
```

#### main
The main function that prints information about the completed workout.

```python
def main(training: Training) -> None:
    # ...
```

## Usage

```python
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
```

Simply run the script, and it will display information about the workouts using the provided data.

**Note:** This description may be expanded depending on additional features and project specifics.
