from pathlib import Path

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
    inputs: MyInputs
    outputs: MyOutputs

    def main(self):
        if self.inputs.my_path is None:
            raise ValueError("my-path is required")
        self.inputs.my_path.mkdir(exist_ok=True)
        self.outputs.runner_os = self.env.runner_os
        self.summary.text += self.render(
            "### {{ inputs.my_input }}.\nHave a nice day, {{ inputs['name'] }}!",
        )


if __name__ == "__main__":
    MyAction().run()
