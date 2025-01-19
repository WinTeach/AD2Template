# Release Notes for ad2template v0.9.1

## New Features
- Folders and other files from the template directory are now also copied to the output directory.
- All template file and folder names can also contain AD attributes in the name (e.g.: #mail#_file.txt).

## Improvements
- UI error messages or undetectable domain and non-existent configuration file have been added.

## Bug Fixes
- Using windows-1252 encoding for reading and writing the template files

## Known Issues
- None

# Release Notes for ad2template v0.9.0

## New Features
- Initial release of `ad2template` application.
- Reads configuration from `config.ini`.
- Generates templates using Jinja2.
- Retrieves Active Directory attributes for the current user.
- Supports logging with configurable log levels.
- Ensures template and output folders exist or creates them if missing.

## Improvements
- None

## Bug Fixes
- None

## Known Issues
- None