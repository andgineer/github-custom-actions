[Базовый класс][github_custom_actions.ActionBase] для GitHub Action.

`ActionBase` также предоставляет вспомогательные методы для вывода стандартных GitHub workflow
команд. С помощью `debug(message: str)` можно писать диагностические сообщения, которые появятся
только при запуске job с включенным debug-логированием. Для аннотаций, которые должны отображаться
в разделе “Files changed”, используйте
[ActionBase.message()][github_custom_actions.ActionBase.message] или её варианты
[error_message][github_custom_actions.ActionBase.error_message],
[notice_message][github_custom_actions.ActionBase.notice_message] и
[warning_message][github_custom_actions.ActionBase.warning_message], чтобы передать путь к файлу,
строку и колонку:

```python
class MyAction(ActionBase):
    def main(self):
        self.debug("Завершён разбор конфигурации")
        self.error_message(
            message="Неизвестный ключ 'service_port'",
            title="Некорректная конфигурация",
            file="config.yml",
            line=14,
            column=1,
        )
```

Эти методы формируют нужную команду `::<severity>::` автоматически; за подробностями параметров
можно обратиться по ссылкам выше.

В своем подклассе вы должны реализовать метод `main()` который вызывается из
[run()][github_custom_actions.ActionBase.run].

Вы можете определить пользовательские типы входных и/или выходных данных в подклассе.
Или вы можете ничего не делать в подклассе, если вам не нужны типизированные входные и выходные данные.

Обратите внимание, что это просто типы, экземпляры этих типов автоматически создаются в методе init.

#### Использование:
```python
--8<-- "input_output_typed.py"
```
