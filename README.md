#  SimpleVisibility 1.2.0 for Blender

A small blender addon to keep render-visibility in sync with viewport-visibility. 
Intended for simpler usecases/workflows where render and viewport visibility shall always be treated the same.

# Usage

Visibility sync can be triggered manually via the outliner context menu. Or it can update the sync status automatically directly before render via the autoupdate setting. The setting is permanent across working sessions and can easily be toggled via the outliner context menu. So just activate / deactivate it as needed.

# Buy me a coffee

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I31T92M)

# Installation

- Use "Code -> Download zip" to download 
- Extract the python file (.py) from the zip archive 
- Install the extracted python file within blender  (Edit Menu -> Preferences -> Addons)
- Activate "Object: SimpleVisibility"

# Preferences

AutoUpdate added

# What's New

Updated to 1.1.0

- Optional AutoUpdate mechanism added ( activate it in the addon preferences ) 

Updated to 1.1.1
- Changed Behaviour for Global Viewport Visibility (screen icon). Now always set to visible, not to interfere.

Updated to 1.1.2

- Switching AutoUpdate (permanent setting) is now easier reachable directly from outliner context menu
		   
Updated to 1.2.0 
- This version now supports syncing collections and collection hierarchies aswell
- Syncing now works with multiple Viewlayers
- Multiple Windows are fully support for manual sync and auto sync modes
- Multiple Main-Windows are already fully supported for manual sync. 
- Note: With AutoUpdate mode the viewlayer detection might sync to the active viewlayer of another than the current window, but just in case of multiple main windows with multiple viewlayers and different active viewlayers set on each window. In this case you might want to switch to manual sync mode temporarily. Should be ruled out soon.
