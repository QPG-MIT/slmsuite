# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import base64
import os
import sys
import inspect
import shutil

import requests

# import numpydoc

module_paths = [
    os.path.abspath("../.."),
    os.path.abspath("../../slmsuite"),
    ]
for module_path in module_paths:
    sys.path.insert(0, module_path)

# -- Project information -----------------------------------------------------

project = "slmsuite"
copyright = "2025, slmsuite Developers"
author = "slmsuite Developers"
release = "0.3.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.extlinks",
    "sphinx.ext.linkcode",
    "sphinx_design",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "nbsphinx",
    "sphinx_copybutton",
    "sphinx_last_updated_by_git",
    # "sphinxcontrib.video",
]

extlinks = {
    "issue": ("https://github.com/slmsuite/slmsuite/issues/%s", "GH"),
    "pull": ("https://github.com/slmsuite/slmsuite/pull/%s", "PR"),
}

# Adapted from https://github.com/DisnakeDev/disnake/blob/7853da70b13fcd2978c39c0b7efa59b34d298186/docs/conf.py#L192
def linkcode_resolve(domain, info):
    if domain != 'py':
        return None

    try:
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        obj = inspect.unwrap(obj)

        if isinstance(obj, property):
            obj = inspect.unwrap(obj.fget)

        path = os.path.relpath(inspect.getsourcefile(obj))
        path = path.split('slmsuite/')[-1]
        src, lineno = inspect.getsourcelines(obj)
    except Exception:
        return None

    path = f"{path}#L{lineno}-L{lineno + len(src) - 1}"
    return f"https://github.com/slmsuite/slmsuite/blob/main/slmsuite/" + path

# Add any paths that contain templates here, relative to this directory.
templates_path = ["templates"]

# numpydoc_xref_param_type = True
# numpydoc_xref_ignore = {"optional", "type_without_description", "BadException"}
# # Run docstring validation as part of build process
# numpydoc_validation_checks = {"all", "GL01", "SA04", "RT03"}
toc_object_entries_show_parents = 'hide'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autosummary_generate = True
autodoc_member_order = "bysource"   # This doesn't work for autosummary unfortunately
                                    # https://github.com/sphinx-doc/sphinx/issues/5379
# autodoc_typehints = "signature"
napoleon_use_param = True
add_module_names = False # Remove namespaces from class/method signatures

nbsphinx_execute = "never"
nbsphinx_allow_errors = True #continue through jupyter errors

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# copybutton_prompt_text = "$ "

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# html_theme = "sphinx_rtd_theme"
navigation_with_keys = True

html_sidebars = {
    "**": [],
}
# html_sidebars = {
#     "**": ["sidebar-nav-bs", "sidebar-ethical-ads"]
# }
html_context = {
    "default_mode": "auto",
}

html_title = f"{project} v{release} Manual"
html_last_updated_fmt = "%b %d, %Y"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the built-in "default.css".
# html_static_path = [] # ["static"]
# html_static_path = ['static']
# html_css_files = ['custom.css']

# Add a logo
# html_theme_options = {"logo_only": True}
html_logo = "static/slmsuite.svg"

# Add a favicon
html_favicon = "static/slmsuite-notext-32x32.ico"

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "logo": {
        "image_light": "static/slmsuite.svg",
        "image_dark": "static/slmsuite-dark.svg",
    },
    "show_prev_next": True,
    "navbar_end": ["theme-switcher", "navbar-icon-links"], #, "search-field.html"
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/slmsuite/slmsuite/",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/slmsuite/",
            "icon": "fab fa-python",
        },
    ],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": ["last-updated", "theme-version"],
    # "content_footer_items": ["last-updated"],
    "show_version_warning_banner": True,
    "navbar_center": ["navbar-nav"],   # "version-switcher",  # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/version-dropdown.html
    # "switcher": {
    #     "version_match": switcher_version,
    #     "json_url": "https://numpy.org/doc/_static/versions.json",
    # },
    "secondary_sidebar_items": {
        "**" : ["page-toc", "edit-this-page", "sourcelink"],
        "index" : [],
        "examples" : [],
    }, # , "breadcrumbs"
    "show_toc_level": 4
    # "secondary_sidebar_end": ["sidebar-ethical-ads"],
}

# https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
def skip(app, what, name, obj, would_skip, options):
    skip_ = would_skip
    # Document `__init__`.
    if name in ("__init__",):
        skip_ = False
    # Don't document magic things.
    elif name in ("__dict__", "__doc__", "__weakref__", "__module__"):
        skip_ = True
    # Don't document private things.
    elif name[0] == '_':
        skip_ = True

    return skip_

examples_repo_owner = "slmsuite"
examples_repo_name = "slmsuite-examples"
# relative to this directory
examples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_examples")
images_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../_build/html/_images")

def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.add_css_file('css/custom.css')

    # Use local notebooks
    # examples_source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..", "slmsuite-examples/examples")
    # shutil.copytree(examples_source,examples_path)

    # Download example notebooks.
    # NOTE: GitHub API only supports downloading files up to 100 MB.
    try:
        os.makedirs(examples_path, exist_ok=False)
        os.makedirs(images_path, exist_ok=True)
        tree_url = (
            "https://api.github.com/repos/{}/{}/git/trees/main?recursive=1"
            "".format(examples_repo_owner, examples_repo_name)
        )
        tree_response = requests.get(tree_url).json()
        for path_object in tree_response["tree"]:
            path_str = path_object["path"]
            if path_str[0:9] == "examples/" and ((path_str[-6:] == ".ipynb") or (path_str[-4:] == ".gif")):
                print("Downloading", path_str)
                file_name = path_str[9:]
                file_url = (
                    "https://api.github.com/repos/{}/{}/git/blobs/{}"
                    "".format(examples_repo_owner, examples_repo_name, path_object["sha"])
                )
                file_url2 = (
                    "https://github.com/{}/{}/blob/main/{}?raw=true"
                    "".format(examples_repo_owner, examples_repo_name, path_str)
                )
                if path_str[-6:] == ".ipynb":
                    file_path = os.path.join(examples_path, file_name)
                    file_response = requests.get(file_url).json()
                    file_content = file_response["content"]
                    file_str = base64.b64decode(file_content.encode("utf8")).decode("utf8")
                    with open(file_path, "w", encoding='utf8') as file_:
                        file_.write(file_str)
                else:
                    file_path = os.path.join(examples_path, file_name)
                    with open(file_path, "wb") as file_:
                        file_.write(requests.get(file_url2).content)

                    image_path = os.path.join(images_path, file_name)
                    shutil.copy(file_path, image_path)
    except OSError as e:
        print("WARNING: Not downloading example notebooks because they have already been downloaded. "
              "Update the examples by deleting the `_examples` directory (or `make clean`). Error:\n{}".format(e))
    except BaseException as e:
        print("WARNING: Unable to download example notebooks. "
              "Building without examples. Error:\n{}".format(e))
