Отрендерить шаблон с помощью Jinja.

В контекст включаются `inputs`, `outputs` и `env` из вашей Github action.

Так что вы можете использовать что-то вроде:
```python
self.render("### {{ inputs.name }}!\\nЖелаю хорошего дня!")
```