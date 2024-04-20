# Быстрый старт

## Пример

#### Типизированные входящие и выходящие переменные

```python
from github_custom_actions import ActionBase, ActionInputs, ActionOutputs

class MyInputs(ActionInputs):
    my_input: str
    """My input description"""
    
    my_path: Path
    """My path description"""
    
    
class MyOutputs(ActionOutputs):
    runner_os: str
    """Runner OS description"""

    
class MyAction(ActionBase):
    def __init__(self):
        super().__init__(inputs=MyInputs(), outputs=MyOutputs())
        if self.inputs.my_path is None:
            raise ValueError("my-path is required")

    def main(self):
        self.inputs.my_path.mkdir(exist_ok=True)
        self.outputs.runner_os = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Have a nice day!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```

#### Упрощенный вариант

Если вы не хотите подробно определять ваши входы и выходы, вы можете использовать их в стиле словаря:

```python
from github_custom_actions import ActionBase

    
class MyAction(ActionBase):
    def main(self):
        if self.inputs["my-path"] is None:
            raise ValueError("my-path is required")
        self.inputs["my-path"].mkdir(exist_ok=True)
        self.outputs["runner-os"] = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Have a nice day!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```

Конечно, у вас не будет подсказок в вашей IDE и описаний, как в документации, но вы можете выбрать, что вам больше нравится. 

В любом случае, у вас есть простой доступ к входам и выходам вашей action, а также к переменным окружения GitHub.
В примере выше мы используем [runner_os](https://docs.github.com/en/actions/learn-github-actions/variables) из переменных окружения GitHub.