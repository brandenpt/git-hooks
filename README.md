# Branden Client git hooks

## About

This git hook verifies if parts of two files are the same and if not then asks to overwrite the file
in the sub directory.

It's a bit necessary if you want to detach some of your build logic to plugins from a composite build,
like this [example](https://github.com/cortinico/kotlin-gradle-plugin-template), because you want to have the same
plugins and versions has the main project.

This script detects, before commit, if the files are different and if they are then asks if you want overwrite them.
If you cancel the commit is also canceled. If you continue then the files are overwritten and added to the commit.

## Usage

### Dependencies

 - Unix like system
 - Python 3.8


Change the [copyconfigargs.py](scripts/copyconfigargs.py) with the names and settings for whatever you like.
The scripts only accept one directory with files to be overwritten.

```python
# Directory with the files to be overwritten
dir_overwrite: str = "build-config-plugins"

# Name of the files to be overwritten
file_names_list: List[str] = ["settings.gradle.kts", "gradle.properties"]

# Dictionary with the needles for each file:
# needles_dict = { file_name: needle }
# A needle should be in ascii and should not be made with only whitespaces
needles_dict: Dict[str, str] = {}

# If the needle_dict doesn't have the needle for the file then use this one:
default_needle: str = "build-config-plugins-needle"

# Timeout in seconds for the prompt, -1 to be unlimited and 0 to always cancel
timeout: int = 5
```

Then copy or hardlink all the scripts in the scripts directory to '.git/hooks/' and done.

## License

The main scripts are licensed with the Mozilla Public License, v. 2.0.
So if you want to change them then you must open-sourced them.

The companion files have the Unlicense so you can do whatever you like, but you can not, of course, copyright them.
