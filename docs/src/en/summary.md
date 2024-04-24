`summary` property of [ActionBase](base.md) implements 
[FileTextProperty][github_custom_actions.action_base.FileTextProperty] connecting it to file
specified in [Github Step Summary][github_custom_actions.GithubVars.github_step_summary].

In this file your action can return some markdown to include in the summary of the step.

You use the property just like `str`, for example

```python
class MyAction(ActionBase):
    def main(self):
        self.summary.text += (
            self.render(
                "### Hello {{ inputs['name'] }}!\n"
                "Have a nice day!"
            )
        )
```

Here we use [render()](render.md) to create text for the summary.

In the Github workflow summary it will look something like this:

> ### Hello John!
> Have a nice day!

