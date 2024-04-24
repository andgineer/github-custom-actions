# Github variables 

In the `vars` attribute of the action class, you can access all the environment variables provided by GitHub.

The library provides a full list of 
[GitHub environment variables](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables), 
including descriptions.

Paths and files have type Path.

```python
--8<-- "quick_start.py"
```

IDE autocomplete and hover documentation are supported:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg).

If accessed through a dictionary, the variable name remains unchanged; if accessed through class attributes, the 
attribute name is converted to uppercase.
So `action.env["GITHUB_REPOSITORY"]` and `action.env.github_repository` refer to the same variable.

This way with dictionary-like syntax you can access to any environment variable, not only set by Github.

For implementation details, see [GithubVars][github_custom_actions.GithubVars].
