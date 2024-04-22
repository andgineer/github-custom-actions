# github-custom-actions

Python package for creating [custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions). 

It works with Python 3.7 and up, so even those dusty old self-hosted action runners can handle it like champs.

### Quick start

```python
--8<-- "quick_start.py"
```

This example uses the `runner_os` variable from GitHub environment variables. 
All variables from the GitHub environment are available in the `vars`, 
with descriptions shown in your IDE on mouse hover:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

The action gets a value from the `my-input` action input and renders 
it in the action step summary on the GitHub build summary.

It also returns a value to the `runner-os` action output.

The main block runs the `main()` method of the action with the necessary boilerplate to catch and report exceptions.

### Explicitly defined inputs and outputs

With explicitly defined inputs and outputs, you can use typo-checked code autocompletion:

```python
--8<-- "input_output_typed.py"
```

Note that you only define the types of inputs and outputs, and instances are created automatically
upon `MyAction` initialization.

Now you can utilize the attributes defined in the `inputs` and `outputs` classes of the action. 
All attributes names are converted to `kebab-case`, allowing dot notation like `inputs.my_input`
to replace the `inputs['my-input']`.

But still can use the `inputs['my-input']` style if you prefer.

### Example of usage
[allure-report action](https://github.com/andgineer/allure-report)
