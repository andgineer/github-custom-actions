## github_custom_actions.action_base.ActionBase.render

```
github_custom_actions.action_base.ActionBase.render(template: str) -> str
```

Отрендерить шаблон с помощью Jinja.

В контекст включаются `inputs`, `outputs` и `env` из вашей Github action.

Так что вы можете использовать что-то вроде:
```python
self.render("### {{ inputs.name }}!\\nЖелаю хорошего дня!")
```

## github_custom_actions.action_base.ActionBase.render_template

```
github_custom_actions.action_base.ActionBase.render_template(template_name: str, **kwargs: str) -> str
```

Отрисовать шаблон из директории `templates`.
`template_name` - это имя файла шаблона без расширения. `kwargs` - это переменные контекста шаблона.

В контекст также включаются `inputs`, `outputs` и `env` из вашей Github action.

Использование:
```
self.render_template("executor.json", image="ubuntu-latest")
```
