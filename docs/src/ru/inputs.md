Входные переменные GitHub Action (inputs)

Использование:
```python
class MyInputs(ActionInputs):
    my_input: str

action = ActionBase(inputs=MyInputs())
print(action.inputs.my_input)
print(action.inputs["my-input"])  # то же самое, что и выше
```

Имена атрибутов преобразуются в `kebab-case`.
Таким образом, `action.inputs.my_input` тоже самое, что и `action.inputs["my-input"]`.

Если вам нужно получить доступ к входному параметру с именем в `snake_case` `my_input`, вы должны
использовать стиль словаря: `action.inputs["my_input"]`.
Но обычно в GitHub Actions имена входных данных используются в `kebab-case`.

По соглашению GitHub все имена входных данных преобразуются в верхний регистр в окружении и имеют
префикс "INPUT_".
Таким образом, `actions.inputs.my_input` или `actions.inputs['my-input']` будет переменной
`INPUT_MY-INPUT` в окружении.
ActionInputs автоматически выполняет преобразование.

Использует ленивую загрузку значений.
Таким образом, значение считывается из окружения только при доступе к нему и только один раз,
и сохраняется во внутреннем словаре объекта.
