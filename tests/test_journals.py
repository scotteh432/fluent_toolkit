import pytest


import fluent_toolkit.journals as journals


class TestJournals:
    def test_journals_template_init(self):
        template = journals.JournalTemplateStartCalculation(iterations=10)
        template.submit_variables({'iterations': 20})
        x = template.get_rendered_text()

    def test_missing_variables(self):
        template = journals.JournalTemplateStartCalculation(iterations=10)
        with pytest.raises(ValueError):
            template.submit_variables({})
        with pytest.raises(ValueError):
            template.get_rendered_text()

    def test_from_text(self):
        text = 'journal'
        journal = journals.JournalTemplate.from_text(text)
        assert isinstance(journal, journals.JournalTemplate)
        assert journal.get_rendered_text() == text

    def test_combine_journals(self):
        template1 = journals.JournalTemplateSetExportQuantities()
        template2 = journals.JournalTemplateExportCaseData('test.cas')
        template3 = journals.JournalTemplateStartCalculation(iterations=10)
        template4 = journals.JournalTemplateQuit()

        new_journal = journals.combine_journals(list_of_journals=[template1, template2, template3, template4])
        new_journal.submit_variables(
            {'export_file_path': 'path.cas',
             'iterations': 10}
        )
        print(new_journal.get_rendered_text())