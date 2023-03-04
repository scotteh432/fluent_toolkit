# This is a set of instructions (with code) on how to get started with this system

# First, pip install fluent_toolkit into your python interpreter. Now you can directly import these libraries:
import fluent_toolkit.fluent
import fluent_toolkit.journals


if __name__ == "__main__":

    # JournalTemplates: - this system uses a class called JournalTemplate for handling variable substitution. This allows
    # you to parameterize your journal files

    # for example:
    file_path = '2-flow-conditions.jou'
    journal = fluent_toolkit.journals.JournalTemplate(file_path)

    # Variables are identified with {{ }} syntax. To see all variables identified by the template:
    print('These are the required variables from the template:')
    journal.print_required_variable_names()
    print('----------------------------------------')

    # Variables can be submitted using a dictionary:
    variables = {
        'x_component': 1.00,
        'pressure': 101325.0,
        'y_component': 0.0,
        'temperature': 288.15,
        'mach_number': 0.25,
        'z_component': 0.0
    }
    journal.submit_variables(variables)
    rendered_text = journal.get_rendered_text()
    print(rendered_text)
    print('----------------------------------------')
    # Note that an error message will be raised if you miss any variables

    # ----------------------------------------
    # Combining multiple journals:
    # Combing multiple journals together is a good way to compartmentalize functionality, and (as we will see soon)
    # is how we add loops into our system

    journal1 = fluent_toolkit.journals.JournalTemplate('1-model-setup.jou')
    journal1.submit_variables({'mesh_file_full_path': 'fake/path/to/msh'})

    journal2 = fluent_toolkit.journals.JournalTemplate('2-flow-conditions.jou')
    journal2.submit_variables(variables)

    combined_journal = fluent_toolkit.journals.combine_journals([journal1, journal2])
    print(combined_journal.get_rendered_text())
    print('----------------------------------------')

    # combined journal will append the text from each journal together in the same order as the list is in. NOTE THAT
    # YOU MUST SUBMIT VARIABLES BEFORE COMBINING! VARIABLES WITH THE SAME NAMES WILL COLLIDE OTHERWISE.

    # --------------------------------------------
    # Built-in Journals:
    # I created some built-in journals with some basic functionality for you
    j1 = fluent_toolkit.journals.JournalTemplateSetExportQuantities()  # <-- sets export quantities to the things you need for basic aerospace stuff
    j2 = fluent_toolkit.journals.JournalTemplateStandardInitialization()  # <-- initializes flow field
    j3 = fluent_toolkit.journals.JournalTemplateStartCalculation(iterations=100)  # <-- Runs the calculation with n number of iteration
    j4 = fluent_toolkit.journals.JournalTemplateExportCaseData(export_file_path='path/to/export.cas')  # <-- Exports a .cas and matching .dat file

    # -------------------------------------
    # Loop through flow conditions
    # By combining journals together, I can create a loop through flow conditions:

    mach_numbers = [0.20, 0.80, 1.50]
    journals = []

    # Mesh loading and model setup
    j1 = fluent_toolkit.journals.JournalTemplate('1-model-setup.jou')
    j1.submit_variables({'mesh_file_full_path': 'fake/path/to/msh'})
    journals.append(j1)

    # Set flow conditions
    variables = {
        'x_component': 1.00,
        'pressure': 101325.0,
        'y_component': 0.0,
        'temperature': 288.15,
        'mach_number': mach_numbers[0],
        'z_component': 0.0
    }

    for i, m in enumerate(mach_numbers):
        j2 = fluent_toolkit.journals.JournalTemplate('2-flow-conditions.jou')
        variables['mach_number'] = m
        j2.submit_variables(variables)
        journals.append(j2)

        if i == 0:
            j3 = fluent_toolkit.journals.JournalTemplateSetExportQuantities()
            j4 = fluent_toolkit.journals.JournalTemplateStandardInitialization()  # <-- only initialize the first, case so that the solution from the previous run becomes the init conditions for the next.

            journals.append(j3)
            journals.append(j4)

        j5 = fluent_toolkit.journals.JournalTemplateStartCalculation(iterations=1000)
        journals.append(j5)

        case_file = 'output_path/case_%d.cas' % i
        j6 = fluent_toolkit.journals.JournalTemplateExportCaseData(export_file_path=case_file)
        journals.append(j6)

    combined_journal = fluent_toolkit.journals.combine_journals(journals)

    with open('my_journal.jou', 'w') as f:
        f.write(combined_journal.get_rendered_text())

    # Tadah! There is your journal!

    # ---------------------------------------------------
    # Auto running of fluent
    # I included a tool for running fluent direct from python

    # No garuntee this works. I could not test it because I don't have a fluent license anymore

    fluent_handler = fluent_toolkit.fluent.FluentRun(combined_journal, destination_folder='path/to/destination/')
    fluent_handler.run(dimensions=2, cores=8, batch=False)














