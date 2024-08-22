class MacroCommand:
    """Команда, яка виконує список команд"""

    def __init__(self, commands):
        self.commands = list(
            commands
        )  # Побудова списку, ініціалізованим аргументом commands гарант шо це ітер обєкт, і збер локальну копію силок на команди в кожн екземплярі

    def __call__(self):
        for (
            command
        ) in self.commands:  # При виклику екземпляра буде виконуватися кожна команда
            command()
