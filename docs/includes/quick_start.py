from github_custom_actions import ActionBase


class MyAction(ActionBase):
    def main(self):
        self.outputs["runner-os"] = self.env.runner_os
        self.summary.text += self.render(
            "### {{ inputs['my-input'] }}.\nHave a nice day!",
        )


if __name__ == "__main__":
    MyAction().run()
