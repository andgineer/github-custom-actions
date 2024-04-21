В атрибуте `vars` класса действия вы можете получить доступ ко всем переменным окружения, предоставляемым GitHub.

Библиотека предоставляет полный список 
[переменных окружения GitHub](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables), 
включая описания.

```python
from github_custom_actions import ActionBase

class MyAction(ActionBase):
    def main(self):
        print(self.vars.github_repository)
```

Поддерживается автодополнение в IDE и документация при наведении:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

Для деталей реализации смотрите [GithubVars](github_custom_actions.GithubVars).
