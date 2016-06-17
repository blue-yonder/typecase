# -*- coding: utf-8 -*-
#
extensions = [
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

# General information about the project.
project = u'Typecase'
copyright = u'2016, Holger Peters'
author = u'Holger Peters'

version = u'0.0.0'
release = u'0.0.0'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False


html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'Typecasedoc'
