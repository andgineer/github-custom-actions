# Quick start

## Example of usage

#### Explicitly defined inputs and outputs

```python
from github_custom_actions import ActionBase, ActionInputs, ActionOutputs

class MyInputs(ActionInputs):
    my_input: str
    """My input description"""
    
    my_path: Path
    """My path description"""
    
    
class MyOutputs(ActionOutputs):
    runner_os: str
    """Runner OS description"""

    
class MyAction(ActionBase):
    def __init__(self):
        super().__init__(inputs=MyInputs(), outputs=MyOutputs())
        if self.inputs.my_path is None:
            raise ValueError("my-path is required")

    def main(self):
        self.inputs.my_path.mkdir(exist_ok=True)
        self.outputs.runner_os = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Have a nice day!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```

#### Simplified version

If you in no mood to scrupulously define your inputs and outputs, you can just use the inputs and outputs as a dict style:

```python
from github_custom_actions import ActionBase

    
class MyAction(ActionBase):
    def main(self):
        if self.inputs["my-path"] is None:
            raise ValueError("my-path is required")
        self.inputs["my-path"].mkdir(exist_ok=True)
        self.outputs["runner-os"] = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Have a nice day!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```

Of course in this case you will not have the benefits of the type hints and the documentation, so choose the way that you prefer.

Anyway you have easy access to your action inputs and outputs and to Github environment variables.
In the example we use [runner_os](https://docs.github.com/en/actions/learn-github-actions/variables) from GitHub environment variables.
