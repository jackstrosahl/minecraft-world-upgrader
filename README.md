# Spigot World Upgrader

For upgrading worlds through multiple versions of Spigot.  Runs
the spigot jar of each version in order with `--forceupgrade`.

**Usage:**
1. Put the Spigot jars you want to upgrade through in the `jars`
folder.  
2. Put your world folders in `jars`.  (Spigot does the conversion, so need to be named `world*`)
3. Run `python convert.py` and follow the prompt.

My use case was `1.12.2`->`1.16.1`.  I put the Spigot jars for
`1.13.2`,`1.14.4`,`1.15.2`,`1.16.1` in my `jars` directory,
 along with the worlds folders, and ran the script.
