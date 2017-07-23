import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
from csv import DictWriter
import os
import sys


def process(files):
    """For each file in the list run file specific processing and collect any
    summary statitics"""
    return [{'Key': 'Value'}]


def header():
    """return the header for the csv file"""
    return ['Key']


class {{ cookiecutter.project_title }}(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tk.Button(self, text='Select Data', command=self.getdata).pack(**button_opt)
        tk.Button(self, text='Save Results', command=self.saveitall).pack(**button_opt)

        # define options for opening or saving a file
        self._button_options(root)

        self.lastAnalysis = None

    def _button_options(self, root):
        self.select_presentation = {
            'defaultextension': '.log',
            'filetypes': [('Presentation files', '.log'), ('all files', '.*')],
            'initialdir': 'C:\\',
            'parent': root,
            'multiple': True,
            'title': 'Load all Presentation logfiles', }
        self.save_csv = {
            'defaultextension': '.csv',
            'filetypes': [('Comma Separated files', '.csv'), ('all files', '.*')],
            'initialdir': 'C:\\',
            'parent': root,
            'title': 'Save to File', }

    def getdata(self):
        """Reads all selected data files and dispatches to an analysis script
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # get filenames
        filenames = askopenfilename(**self.select_presentation)
        self.lastAnalysis = process(filenames)

    def saveitall(self):
        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        if self.lastAnalysis is None:
            showinfo('No data processed, please select files first')
            return

        # get filename
        filename = asksaveasfilename(**self.save_csv)

        # open file on your own
        if filename:
            lines = self.lastAnalysis
            with open(filename, 'w') as csvfile:
                writer = DictWriter(csvfile, header())
                writer.writeheader()
                writer.writerows(lines)
            self.lastAnalysis = None


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append('.')

    return os.path.join(datadir, filename)


if __name__ == '__main__':
    root = tk.Tk()
    try:
        root.iconbitmap(find_data_file('{{ cookiecutter.app_name }}.ico'))
    except tk.TclError:
        pass
    {{ cookiecutter.project_title }}(root).pack()
    root.mainloop()
