Выходные переменные GitHub Action (outputs)

Использование:
```python
class MyOutputs(ActionOutputs):
   my_output: str

action = ActionBase(outputs=MyOutputs())
action.outputs["my-output"] = "value"
action.outputs.my_output = "value"  # то же самое, что выше
```

С атрибутами можно обращаться только к явно объявленным переменным,
с помощью доступа, подобного словарю, можно обратиться к любой переменной.
Таким образом, вы можете найти баланс между строго определёнными переменными и гибкостью.

Имена атрибутов преобразуются в `kebab-case`.
Так что `action.outputs.my_output` тоже самое, что и `action.outputs["my-output"]`.

Если вам нужно обратиться к выходной переменной с именем в `snake_case`, например `my_output`,
следует использовать только стиль словаря: `action.outputs["my_output"]`.
Но обычно в именах выходных данных GitHub Actions используется `kebab-case`.

Каждое присвоение выходной переменной изменяет файл выходных данных GitHub
(путь определяется как `action.env.github_output`).
