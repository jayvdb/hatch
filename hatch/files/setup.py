from hatch.structures import File
from hatch.utils import normalize_package_name

TEMPLATE = """\
#################### Maintained by Hatch ####################
# This file is auto-generated by hatch. If you'd like to customize this file
# please add your changes near the bottom marked for 'USER OVERRIDES'.
# EVERYTHING ELSE WILL BE OVERWRITTEN by hatch.
#############################################################
from io import open

from setuptools import find_packages, setup

with open('{package_name_normalized}/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \\'"')
            break
    else:
        version = '0.0.1'

with open('{readme_file}', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = {requires}

kwargs = {{
    'name': '{package_name}',
    'version': version,
    'description': '',
    'long_description': readme,
    'author': '{name}',
    'author_email': '{email}',
    'maintainer': '{name}',
    'maintainer_email': '{email}',
    'url': '{package_url}',
    'license': '{license}',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',{license_classifiers}
        'Natural Language :: English',
        'Operating System :: OS Independent',{pyversions}
        'Programming Language :: Python :: Implementation :: CPython',{pypy}    ],
    'install_requires': REQUIRES,
    'tests_require': ['coverage', 'pytest'],
    'packages': find_packages(exclude=('tests', 'tests.*')),{entry_point}
}}

#################### BEGIN USER OVERRIDES ####################
# Add your customizations in this section.{user_overrides}
###################### END USER OVERRIDES ####################

setup(**kwargs)
"""


class SetupFile(File):
    def __init__(self, name, email, package_name, pyversions, licenses, readme,
                 package_url, cli, requires=None, user_overrides=None):
        normalized_package_name = normalize_package_name(package_name)

        pypy = '\n'
        versions = ''
        for pyversion in pyversions:
            if not pyversion.startswith('pypy'):
                versions += "\n        'Programming Language :: Python :: {}',".format(
                    pyversion
                )
            else:
                pypy = "\n        'Programming Language :: Python :: Implementation :: PyPy',\n"

        license_classifiers = ''
        for li in licenses:
            license_classifiers += "\n        '{}',".format(li.pypi_classifier)

        entry_point = ''
        if cli:
            entry_point += (
                '\n'
                "    'entry_points': {{\n"
                "        'console_scripts': [\n"
                "            '{pn} = {pnn}.cli:{pnn}',\n"
                '        ],\n'
                '    }},'.format(pn=package_name, pnn=normalized_package_name)
            )

        # For testing we use https://github.com/r1chardj0n3s/parse and its
        # `parse` function breaks on empty inputs.
        entry_point += '\n'
        user_overrides = '\n' + (user_overrides or '')

        super(SetupFile, self).__init__(
            'setup.py',
            TEMPLATE.format(
                name=name,
                email=email,
                package_name=package_name,
                package_name_normalized=normalized_package_name,
                readme_file=readme.file_name,
                package_url=package_url,
                license='/'.join(li.short_name for li in licenses),
                license_classifiers=license_classifiers,
                pyversions=versions,
                pypy=pypy,
                entry_point=entry_point,
                user_overrides=user_overrides,
                requires=requires or [],
            )
        )
