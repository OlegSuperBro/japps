# Changelog

# 0.0.4

### Added
- Added `PluginImportError`, `PluginConfigError`, `PluginNoInfoError`, `RunnerError`, `UnknownPluginTypeError` exceptions.
- Added type annotations and forward references in several modules to improve type checking and clarity.
- Integrated additional debug logging for better traceability.
- Added a `_check_is_allowed` func in `japps/PluginManager.py` to validate plugin according to configuration settings.
- Implemented exception handling in `japps/PluginLoaders.py` and `japps/PluginManager.py` to manage plugin loading failures gracefully.

### Changed
- Added `TYPE_CHECKING` to avoid circular imports and improve type hinting.
- Modified logger update function in `japps/Log.py` for `config` to allow using `None` as parameter.
- Most code was refactored to use `PathLike`.
- Updated test configurations to use `pathlib.Path` and deep copies for isolated configuration testing.

### Fixed
- Corrected the issue where plugin names were not checked correctly, potentially allowing duplicate names.

### Removed
- Removed depricated `abstractstaticmethod` and replaced it with `staticmethod` and `abstractmethod`.

# 0.0.3

### Fixed
- Allow no info for single file plugin, apply no info if not all info present in config for package plugins
- One slash instead backslashs in plugin manager (backslashes don't work on linux)

# 0.0.2

### Added
- More error types
- Checking plugins for some conditions (in PluginManager) 
- Allow returning values from plugin running. Dict with `PluginName: value` format or just value for single plugin
- Setting plugin actions in IPlugin classes for using in SimpleFuncRunner


### Changed
- Moved plugins types in separated directory
- Changed default ignore pattern in config
- Now all plugins should have `NAME` declared. If no_info is allowed then will be used "Unknown {}" where "{}" is hash of plugin object

### Fixed
- no_info_default copying insead just assign in PackagePluginLoader class

### Removed
- Setting up plugin actions in config


# 0.0.1

Created
