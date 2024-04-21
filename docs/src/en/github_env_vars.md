In the `vars` attribute of the action class, you can access all the environment variables provided by GitHub.

The library provides a full list of 
[GitHub environment variables](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables), 
including descriptions.

```python
from github_custom_actions import ActionBase

class MyAction(ActionBase):
    def main(self):
        print(self.vars.github_repository)
```

IDE autocomplete and hover documentation are supported:
![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

For implementation details, see [GithubVars](github_custom_actions.GithubVars).
