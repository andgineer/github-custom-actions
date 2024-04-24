Свойство summary в ActionBase реализует
[FileTextProperty][github_custom_actions.action_base.FileTextProperty], связывая его с файлом,
указанным в [Github Step Summary][github_custom_actions.GithubVars.github_step_summary].

В этом файле ваше действие может возвращать markdown текст для включения в сводку шага.

Вы используете свойство так же, как и `str`, например

```python
class MyAction(ActionBase):
    def main(self):
        self.summary.text += (
            self.render(
                "### Привет {{ inputs['name'] }}!\n"
                "Желаю хорошего дня!"
            )
        )
```

Здесь мы используем [render()](render.md), чтобы создать текст для сводки.

В сводке Github workflow это будет выглядеть примерно так:

> ### Привет, Джон!
> Желаю хорошего дня!
