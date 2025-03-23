# Переменные окружения GitHub

В атрибуте `env` класса действия вы можете получить доступ ко всем переменным окружения, предоставляемым GitHub.

Библиотека предоставляет полный список
[переменных окружения GitHub](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables),
включая описания.

Пути и файлы имеют тип `Path`.

```python
--8<-- "quick_start.py"
```

Поддерживается автодополнение в IDE и документация при наведении:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg).

При доступе через атрибуты класса имя атрибута преобразуется в верхний регистр что нам дает стандартное
имя переменной окружения Github.

При доступе через словарь имя переменной никак не изменяется, что позволяет прочитать любую переменную окружения, не
только установленную Github.

Таким образом `action.env["GITHUB_REPOSITORY"]` и `action.env.github_repository` обращаются к одной и той же переменной.

Для деталей реализации смотрите [GithubVars][github_custom_actions.GithubVars].
