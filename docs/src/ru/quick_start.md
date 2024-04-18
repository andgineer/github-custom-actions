# Быстрый старт

#### Пример

```python
from github_custom_actions import ActionBase, ActionInputs

class MyInputs(ActionInputs):
    my_input: str
    """My input description"""
    
    my_path: Path
    """My path description"""

class MyAction(ActionBase):
    def __init__(self):
        super().__init__(inputs=MyInputs())
        if self.inputs.my_path is None:
            raise ValueError("my_path is required")

    def main(self):
        self.inputs.my_path.mkdir(exist_ok=True)
        self.outputs["RUNNER_OS"] = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Приятного дня!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```
