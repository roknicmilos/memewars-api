from abc import abstractmethod
from datetime import datetime


class AbstractFixturesGenerator:
    raw_fixtures_item_template: str

    def __init__(self, quantity_level: int = 1):
        self.quantity_level = quantity_level
        self.fixture_template = self.get_fixture_template()
        self.fixture_items = self.get_fixture_items()

    def get_fixture_template(self) -> str:
        raw_fixtures_item_template_without_empty_lines = "".join(
            [line for line in self.raw_fixtures_item_template.splitlines(keepends=True) if line.strip()]
        )
        first_line = raw_fixtures_item_template_without_empty_lines.splitlines()[0]
        first_line_indent = len(first_line) - len(first_line.lstrip())

        prepared_template = ""
        for line in raw_fixtures_item_template_without_empty_lines.splitlines(keepends=True):
            prepared_template += line[first_line_indent:]

        return prepared_template

    def generate(self) -> str:
        """
        Generates content for *.yaml fixture files
        """
        output = ""
        for item in self.fixture_items:
            output += self.render_fixture_item(**item)
        return output

    @abstractmethod
    def get_fixture_items(self) -> list[dict]:
        pass

    def render_fixture_item(self, **kwargs) -> str:
        output = self.fixture_template

        for key, value in kwargs.items():
            if f"@{key}" not in output:
                raise AttributeError(f"{self.__class__.__name__} fixture template does not contain @{key}")
            output = output.replace(f"@{key}", str(value))

        if "@now" in output:
            now_str = datetime.now().isoformat().split(".")[0]
            output = output.replace("@now", now_str)

        return output
