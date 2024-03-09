# Changelog

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
