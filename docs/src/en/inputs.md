If you use basic [ActionInputs][github_custom_actions.ActionInputs] use dict style to access inputs.


```python

As you can see now you can use the `inputs` and `outputs` attributes of the action class.
All names are converted to snake_case, so you can use them in the action as `inputs.my_input` instead of `inputs['my-input']`.

You you want to use snake_case you are out of luck. For that you should override

if you define it as Path