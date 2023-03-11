from abc import abstractmethod


class AbstractFixturesGenerator:
    """
    Generates content (string) for *.yaml files containing fixtures
    """

    raw_fixture_template: str

    def __init__(self):
        self.fixture_template = self.get_fixture_template()

    def get_fixture_template(self) -> str:
        raw_fixture_template_without_empty_lines = "".join([
            line for line in self.raw_fixture_template.splitlines(keepends=True) if line.strip()
        ])
        first_line = raw_fixture_template_without_empty_lines.splitlines()[0]
        first_line_indent = len(first_line) - len(first_line.lstrip())

        prepared_template = ''
        for line in raw_fixture_template_without_empty_lines.splitlines(keepends=True):
            prepared_template += line[first_line_indent:]

        return prepared_template

    @abstractmethod
    def generate(self) -> str:
        pass
