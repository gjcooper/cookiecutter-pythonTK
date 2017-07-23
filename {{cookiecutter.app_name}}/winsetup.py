from setuptools import find_packages
import codecs
import os
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

tcl_path = r'{{ cookiecutter.tcl_path }}'
os.environ['TCL_LIBRARY'] = os.path.join(tcl_path, 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(tcl_path, 'tk8.6')
dll_path = r'{{ cookiecutter.dll_path }}'
include = [(os.path.join(dll_path, 'tcl86t.dll'), 'tcl86t.dll'),
           (os.path.join(dll_path, 'tk86t.dll'), 'tk86t.dll'),
           ('{{ cookiecutter.app_name }}.ico', '{{ cookiecutter.app_name }}.ico')]

base_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(base_dir, 'src')
pkg_dir = os.path.join(src_dir, '{{ cookiecutter.app_name }}')
# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)
about = {}
with open(os.path.join(pkg_dir, '__about__.py')) as f:
    exec(f.read(), about)

targdir = r'[ProgramFilesFolder]\{__author__}\{__title__}'.format(**about)
options = {
    'bdist_msi': {
        'upgrade_code': '{a1e70337-294c-44e9-9a22-e79f3d156761}',
        'add_to_path': False,
        'initial_target_dir': targdir},
    'build_exe': {
        'includes': ['tkinter'],
        'packages': ['tkinter'],
        'include_files': include}}

executables = [Executable(os.path.join(pkg_dir, '{{ cookiecutter.app_name }}.py'),
                          base=base,
                          shortcutName='{{ cookiecutter.project_title }}',
                          shortcutDir='StartMenuFolder')]


def genRST():
    with open('README.md') as mdfile:
        return mdfile.read()


# get the dependencies and installs
with codecs.open(os.path.join(base_dir, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=genRST(),
    url=about['__uri__'],
    license=about['__license__'],
    options=options,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(where='src', exclude=['tests*']),
    package_dir={'': 'src'},
    include_package_data=True,
    author=about['__author__'],
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email=about['__email__'],
    executables=executables
)
