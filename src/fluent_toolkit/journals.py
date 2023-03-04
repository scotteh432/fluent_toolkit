import io
import os
import jinja2
import jinja2.meta
import tempfile


import fluent_toolkit.common as common


class JournalTemplate:
    def __init__(self, path_to_journal_template):

        environment = jinja2.Environment()

        if isinstance(path_to_journal_template, str):
            with open(path_to_journal_template, 'r') as f:
                self._raw_text = f.read()
        elif isinstance(path_to_journal_template, io.StringIO):
            self._raw_text = path_to_journal_template.read()
        else:
            e = '%s was not found!' % path_to_journal_template
            raise FileNotFoundError(e)

        self._template = environment.from_string(self._raw_text)
        self._required_variables = list(jinja2.meta.find_undeclared_variables(environment.parse(self._raw_text)))
        self._submitted_variables = {}
        self._variables_have_been_submitted = False

    @staticmethod
    def from_text(journal_text):
        """
        Entry point that creates a JournalTemplate object directly from text

        :param str journal_text:
        :return: JournalTemplate
        """

        temp_file = io.StringIO(journal_text)
        journal = JournalTemplate(temp_file)
        return journal

    def submit_variables(self, variable_dictionary):
        """
        Submit variables to the jinja2 template

        :param dict variable_dictionary: dictionary object containing all required variables by the template
        """

        # Sanitize input
        if not isinstance(variable_dictionary, dict):
            e = 'variables_dictionary must be of type dict'
            raise ValueError(e)
        self._submitted_variables = variable_dictionary

        # Check if there are any missing variables
        missing_variables = []
        for key in self.required_variables:
            if key not in variable_dictionary.keys():
                missing_variables.append(key)
        if len(missing_variables) != 0:
            e = 'Variables required by the template are missing\n'
            e += '\n'.join(missing_variables)
            raise ValueError(e)

        # Update property with submitted variables
        self._submitted_variables = variable_dictionary
        self._variables_have_been_submitted = True

    @property
    def template(self):
        return self._template

    @property
    def required_variables(self):
        return self._required_variables

    def print_required_variable_names(self):
        output_text = 'Theses are the names of the required variables\n'
        output_text += '\n'.join(self._required_variables)
        print(output_text)

    def get_raw_text(self):
        """
        Returns raw text of journal file before variable substitution has been performed

        :return: raw_text
        :rtype: str
        """

        return self._raw_text

    def get_rendered_text(self):
        """
        Returns text with variable substitution having been performed

        :return: output_text
        :rtype: str
        """
        if len(self._required_variables) == 0 or self._variables_have_been_submitted is True:
            output_text = self.template.render(self._submitted_variables)
            return output_text
        else:
            e = 'Please submit variables using the submit_variables() method before accessing the rendered text'
            raise ValueError(e)


class JournalTemplateSetExportQuantities(JournalTemplate):
    def __init__(self):
        path = os.path.join(common.TEMPLATES_DIR, 'set_export_quantities.jou')
        JournalTemplate.__init__(self, path)


class JournalTemplateStartCalculation(JournalTemplate):
    def __init__(self, iterations):
        path = os.path.join(common.TEMPLATES_DIR, 'start_calculation.jou')
        JournalTemplate.__init__(self, path)

        self.submit_variables({'iterations': iterations})


class JournalTemplateExportCaseData(JournalTemplate):
    def __init__(self, export_file_path):
        path = os.path.join(common.TEMPLATES_DIR, 'export_case_data.jou')
        JournalTemplate.__init__(self, path)

        file_extension = os.path.basename(export_file_path).split('.')[-1]
        if file_extension != 'cas':
            e = 'export_file_path must be ".cas" file. Note that the matching ".dat" file will automatically be created'
            raise ValueError(e)
        self.submit_variables({'export_file_path': export_file_path})


class JournalTemplateStandardInitialization(JournalTemplate):
    def __init__(self):
        path = os.path.join(common.TEMPLATES_DIR, 'standard_initialization.jou')
        JournalTemplate.__init__(self, path)



class JournalTemplateQuit(JournalTemplate):
    def __init__(self):
        path = os.path.join(common.TEMPLATES_DIR, 'quit.jou')
        JournalTemplate.__init__(self, path)


def combine_journals(list_of_journals):
    """
    Combine journals into one file. Please run this BEFORE submitting variables. Running this will reset the journals
    to have no submitted variables. Journals will be combined in the order they are submitted

    :param list list_of_journals: list of JournalTemplate objects

    :return: journal_template
    :rtype: JournalTemplate
    """

    # Sanitize
    if not isinstance(list_of_journals, (list, tuple)):
        raise ValueError('list_of_journals must be of type iterable')
    for x in list_of_journals:
        if not isinstance(x, JournalTemplate):
            e = 'Every entry in list_of_journals must be of type JournalTemplate'
            raise ValueError(e)

    # Combine
    list_of_rendered_text = [j.get_rendered_text() for j in list_of_journals]
    output_text = '\n'.join(list_of_rendered_text)
    journal = JournalTemplate.from_text(output_text)
    return journal
