# github-custom-actions

Библиотека упрощающая создание
[custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions).

[Как создать свой GitHub Action за 5 минут](https://sorokin.engineer/posts/ru/github-custom-actions.html).

Библиотека может работать даже с Python 3.8 чтобы поддерживать древние self-hosted action runners.

### Быстрый старт

```python
--8<-- "quick_start.py"
```

Этот пример использует переменную [runner_os][github_custom_actions.GithubVars.runner_os] из
[переменных окружения GitHub][runner_os][github_custom_actions.GithubVars].

Все переменные из окружения GitHub доступны в `env`,
описания которых отображаются в вашей IDE при наведении мыши:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

Action получает значение из [action input](inputs) `my-input` и отображает его
в [step summary](summary) на странице билда GitHub.

Оно также возвращает значение в [action output](outputs) `runner-os`.

> **Внимание:** Строки в output не должны содержать переносов строки.
> Если они вам нужны то придется строки как-то кодировать (base64/etc).

`run()` в основном блоке запускает метод [main()](main) реализующий вашу Github action.

### Явно определенные входы и выходы

С явно определенными входами и выходами вы можете использовать автодополнение кода с проверкой на опечатки:

```python
--8<-- "input_output_typed.py"
```

Обратите внимание, что вы только определяете типы входов и выходов, а экземпляры этих классов создаются автоматически
при инициализации [ActionBase](base).

Теперь вы можете использовать атрибуты, определенные в классах `inputs` и `outputs` действия.
Все имена атрибутов преобразуются в `kebab-case`, что позволяет использовать точечную нотацию, например `inputs.my_input`,
вместо `inputs['my-input']`.

Если вы определили input как `Path`, он будет преобразован в объект `Path`.

При желании вы все также можете использовать стиль `inputs['my-input']`.

### Пример использования

[Allure Test Report Action](https://github.com/andgineer/allure-report/blob/main/src/allure_generate.py)
