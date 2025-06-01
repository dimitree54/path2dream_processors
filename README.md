# Public Python Package Template

## Using This Template for Your Own Package (e.g., "my_package")

To adapt this template for your new package (let's call it "my_package"):

1.  **Copy or Template the Repository:**
    *   Click the "Use this template" button on GitHub to create a new repository from this template.

2.  **Rename the Package Directory:**
    *   Rename the main package directory in src dir

3.  **Update `pyproject.toml`:**
    *   **`[project].name`**: Change from `"public_package_template"` to `"my_package"`.
    *   **`[project].urls`**: Update `Homepage` and `Repository` URLs to point to your new repository.

4.  **Set up bump version:**
	1.	Go to: https://github.com/settings/personal-access-tokens/new?type=beta
    2.	Set permission "Contents" to Read & Write
    3.  Create a repository secret with the name BUMPVERSION_TOKEN
    4.  It is recommended to make the main branch protected as every push/merge/commit to it will trigger a bump version.

5.  **Set up PyPI**
    1.  Go to: https://pypi.org/manage/account/token/
    2.  Click "Add API token", set the scope for your package
    3.  Create a repository secret with the name PYPI_PUBLISH_TOKEN

6.  **Once you push anything to main, a new tag will be created, built, and published to PyPI**


## Installing Your Published Public Package

Then you can just pip install your package.
