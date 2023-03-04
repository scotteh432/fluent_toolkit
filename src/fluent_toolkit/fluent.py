import os
import subprocess

import fluent_toolkit.journals


class FluentRun:
    """
    Class for managing a run of ANSYS Fluent given an inputted Mesh File and JournalTemplate object

    :param fluent_toolkit.journals.JournalTemplate journal_template: JournalTemplate class object
    :param str destination_folder: folder where your results will be saved to
    """

    def __init__(self, journal_template, destination_folder):
        self.journal_template = journal_template
        self.destination_folder = destination_folder

    def _save_journal_file(self):
        journal_dir = os.path.join(self.destination_folder, 'journal')
        if not os.path.isdir(journal_dir):
            os.mkdir(journal_dir)
        with open(self.journal_file_path, 'w') as f:
            text = self.journal_template.get_rendered_text()
            f.write(text)

    def _run_fluent(self, dimensions=2, cores=12, batch=False):
        """
        Launches fluent and runs the journal
        """
        # Run command
        if batch is True:
            p1 = subprocess.Popen('fluent %dddp -t%d -g -i "%s"' % (dimensions, cores, self.journal_file_path.replace('\\', '/')), stdout=subprocess.PIPE, shell=True)
        else:
            p1 = subprocess.Popen('fluent %dddp -t%d -i "%s"' % (dimensions, cores, self.journal_file_path.replace('\\', '/')), stdout=subprocess.PIPE, shell=True)
        p1.communicate()

    def run(self, dimensions=2, cores=12, batch=False):
        """
        Run the solver system

        :param int dimensions: 2 or 3 (launches either 2d fluent or 3d fluent)
        :param int cores: number of compute cores
        :param bool batch: if True, runs in batch mode, else runs in gui mode (default is False)
        """

        self._save_journal_file()
        self._run_fluent(dimensions=dimensions, cores=cores, batch=batch)

    @property
    def journal_file_path(self):
        path = os.path.join(self._destination_folder, 'journal.jou')
        return path

    @property
    def destination_folder(self):
        return self._destination_folder

    @destination_folder.setter
    def destination_folder(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        self._destination_folder = path


