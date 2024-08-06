# wagtail-portablepages

Export individual Wagtail pages as JSON and import them back to a Wagtail instance.

wagtail-portablepages has some constrains to be able to import an exported page:

- The `translation_key` must not already exist (it won't overwrite an existing page).
- The Django application and model that the specific page belongs to must exist.
- The Django application's latest migration state must match that of the page export.

⚠️ wagtail-portablepages ***WILL NOT***:

- Export any foreign keys, one-to-many, or many-to-many relationships; these relationships will break.
- Export any snippets of any kind; these will have to be readded/reassociated/etc.
- Export any documents, images, etc; these will have to be moved independently and readed/reassociated/etc.
- Export any page translations; these will have to be exported independently. The translation key will be preserved.

If you have any of these needs, [wagtail-transfer](https://github.com/wagtail/wagtail-transfer) is a better option.

🚧 This is still a work in progress. 🚧

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Exporting](#exporting)
  - [Importing](#importing)
  - [JSON Format](#json-format)
- [Getting help](#getting-help)
- [Getting involved](#getting-involved)
- [Licensing](#licensing)

## Dependencies

- Python 3.8+
- Django 4.2 (LTS)+
- Wagtail 6.1

It should be compatible at all intermediate versions, as well.
If you find that it is not, please [file an issue](https://github.com/cfpb/wagtail-portablepages/issues/new).

## Installation

1. Install wagtail-portablepages:

```shell
pip install wagtail-portablepages
```

2. Add `portablepages` as an installed app in your Django `settings.py`:

 ```python
 INSTALLED_APPS = (
     ...
     "portablepages",
     ...
 )
```

## Usage


### Exporting

In a page listing iin the Wagtail admin the more options menu under the `…` icon in a page's row will contain an "Export" item. This will export the page data as JSON and begin a file download of that JSON file.

To export the page data to JSON in Python, wagtail-portablepages provides an `export_page()` function that takes a page to export and will return the JSON as a string. From there it can be handled as needed.

```python
from wagtail.models import Page
from portablepages.utils import export_page

# Get the page we want to export
specific_page = Page.objects.get(pk=1234).specific

# Export it to a JSON string
page_json = export_page(specific_page)
```

### Importing

In a page listing iin the Wagtail admin the more options menu under the `…` icon in a page's row will contain an "Import" item. This will prompt you to upload a previously exported page JSON file as a child page of the page you selected.

To import page JSON in Python, wagtail-portablepages provides an `import_page()` function that takes a parent page and a JSON string containing previously exported page data, and will return the new page object created from the page data.

```python
from wagtail.models import Page
from portablepages.utils import import_page

# Read the JSON string in from the file
with open("my-page.json") as page_file:
    page_json = page_file.read().decode("utf8")

# Get the page that will be the parent of our imported page
parent_page = Page.objects.get(pk=123)

# Import the page as a child of the parent page from the JSON string
new_page = import_page(parent_page, page_json)
```

### JSON format



## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/wagtail-portablepages/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Licensing
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

