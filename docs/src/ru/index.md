# github-custom-actions

Библиотека упрощающая создание
[custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions).

Может работать даже с Python 3.7 чтобы поддерживать древние self-hosted action runners.

### Быстрый старт

```python
--8<-- "quick_start.py"
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
--8<-- "input_output_typed.py"
```

Обратите внимание, что вы только определяете типы входов и выходов, а экземпляры этих классов создаются автоматически
при инициализации `MyAction`.

Теперь вы можете использовать атрибуты, определенные в классах `inputs` и `outputs` действия. 
Все имена атрибутов преобразуются в `kebab-case`, что позволяет использовать точечную нотацию, например `inputs.my_input`, 
вместо `inputs['my-input']`.

При желании вы все также можете использовать стиль `inputs['my-input']`.

### Пример использования
[allure-report action](https://github.com/andgineer/allure-report)

