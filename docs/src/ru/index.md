# github-custom-actions

Библиотека упрощающая создание
[custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions).

Может работать даже с Python 3.7 чтобы поддерживать древние self-hosted action runners.

### Быстрый старт

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

Этот пример использует переменную `runner_os` из переменных окружения GitHub. 

Все переменные из окружения GitHub доступны в `vars`, 
описания которых отображаются в вашей IDE при наведении мыши:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

Action получает значение из action input `my-input` и отображает его 
в `step summary` на странице билда GitHub.

Оно также возвращает значение в action output `runner-os`.

Основной блок запускает метод `main()` действия с необходимым кодом для перехвата и обработки исключений.

### Явно определенные входы и выходы

С явно определенными входами и выходами вы можете использовать автодополнение кода с проверкой на опечатки:

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
    inputs = MyInputs()
    outputs = MyOutputs()

    def main(self):
        if self.inputs.my_path is None:
            raise ValueError("my-path is required")
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

Теперь вы можете использовать атрибуты, определенные в классах `inputs` и `outputs` действия. 
Все имена преобразуются в `snake_case`, что позволяет использовать точечную нотацию, например `inputs.my_input`, 
вместо `inputs['my-input']`.

### Пример использования
[allure-report action](https://github.com/andgineer/allure-report)

