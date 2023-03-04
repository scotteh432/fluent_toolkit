import os


import test_utils
import fluent_toolkit.fluent
import fluent_toolkit.journals


class TestFluentRun:
    def test_init(self):
        journal = fluent_toolkit.journals.JournalTemplateStartCalculation(iterations=20)
        fluent_handler = fluent_toolkit.fluent.FluentRun(journal_template=journal, destination_folder=test_utils.create_test_dump())
        fluent_handler.run()


