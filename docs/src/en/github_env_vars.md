The library provides full list of GitHub environment variables, including description.
IDE autocomplete and hover documentation are supported.

![var_ide_hover_docstring.jpg](images/var_ide_hover_docstring.jpg)

Just use [vars attribute of the action class][github_custom_actions.GithubVars]

```python
from github_custom_actions import ActionBase

    
class MyAction(ActionBase):
    def main(self):
        print(self.vars.github_repository)

```