The [ActionBase][github_custom_actions.ActionBase] base class also exposes helpers to emit the
standard GitHub workflow log commands. Use `debug(message: str)` when you want to show extra
information only when a workflow runs with debug logging enabled. For annotations that should show
up in the PR “Files changed” view, call
[ActionBase.message()][github_custom_actions.ActionBase.message] (or its convenience aliases
[error_message][github_custom_actions.ActionBase.error_message],
[notice_message][github_custom_actions.ActionBase.notice_message], and
[warning_message][github_custom_actions.ActionBase.warning_message]) so you can attach file, line,
and column
information:

```python
class MyAction(ActionBase):
    def main(self):
        self.debug("Finished parsing configuration")
        self.error_message(
            message="Unknown key 'service_port'",
            title="Invalid config",
            file="config.yml",
            line=14,
            column=1,
        )
```

Those helpers format the underlying `::<severity>::` workflow command for you; refer to the links
above for the full list of keyword arguments if you need to build more complex annotations.

::: github_custom_actions.ActionBase
    options:
      heading_level: 1
      show_submodules: false
