# outputs вашей GitHub Action

Выходящие параметры описываются в наследнике 
[class ActionOutputs][github_custom_actions.ActionOutputs]

Если вы не создаете наследника, то можете получать выходные параметры в стиле словаря.
Описав же наследника вы получите все преимущества автодополнения и проверки типов.

```python
class MyOutputs(ActionOutputs):
    my_output: str

action = ActionBase(outputs=MyOutputs())
action.outputs["my-output"] = "value"
action.outputs.my_output = "value"  # the same as above
```

Имена атрибутов преобразуются в `kebab-case`. 
Таким образом, `action.outputs.my_output` эквивалентен `action.outputs["my-output"]`.

Если вам нужно получить доступ к выходным данным с именем в snake_case `my_output`, 
следует использовать только стиль словаря: `action.outputs["my-output"]`. 
Но обычно в именах выходных данных GitHub Actions используется kebab-case.

Каждое присваивание переменных выводов изменяет файл выводов Github 
(путь определяется переменной Github `action.env.github_output`).
