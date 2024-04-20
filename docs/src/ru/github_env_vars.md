Библиотека предоставляет полный список переменных окружения GitHub, включая описание.
Поддерживаются автозавершение и всплывающая документация в IDE.

![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

Используйте [vars attribute of the action class][github_custom_actions.GithubVars]

```python
from github_custom_actions import ActionBase

    
class MyAction(ActionBase):
    def main(self):
        print(self.vars.github_repository)

```