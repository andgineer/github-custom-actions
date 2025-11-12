# github-custom-actions

Python package for creating [custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions).

[How to Create Your Own GitHub Action in 5 Minutes](https://sorokin.engineer/posts/en/github-custom-actions.html).

The package works with Python 3.8 and up, so even those dusty old self-hosted action runners can
handle it like champs.

### Quick start

```python
--8<-- "quick_start.py"
```

This example uses the [runner_os][github_custom_actions.GithubVars.runner_os]
variable from
[GitHub environment variables][github_custom_actions.GithubVars].
All variables from the GitHub environment are available in the `env`,
with descriptions shown in your IDE on mouse hover:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

The action gets a value from the `my-input` [action input](inputs) and renders
it in the action [step summary](summary) on the GitHub build summary.

It also returns a value to the `runner-os` [action output](outputs).

> **Note:** Output values cannot contain newlines. If you need them
> encode the values (JSON/base64/etc) before writing.

The `run()` in the main block runs the [main()](main) that implements your action.

### Explicitly defined inputs and outputs

With explicitly defined inputs and outputs, you can use typo-checked code autocompletion:

```python
--8<-- "input_output_typed.py"
```

Note that you only define the types of inputs and outputs, and instances are created automatically
upon [ActionBase](base) initialization.

Now you can utilize the attributes defined in the `inputs` and `outputs` classes of the action.
All attributes names are converted to `kebab-case`, allowing dot notation like `inputs.my_input`
to replace the `inputs['my-input']`.

Inputs defined as Path will be converted to `Path` objects.

But still can use the `inputs['my-input']` style if you prefer.

### Example of usage

[Allure Test Report Action](https://github.com/andgineer/allure-report/blob/main/src/allure_generate.py)
