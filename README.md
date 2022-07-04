# Sublime Text 4 Automatic Formatter

## Description

AutomaticFormatter is a simple code formatter plugin for **Sublime Text 4**.
It provides ability to format C, C++, C++/CLI, Objective‑C, C#, and Java Source Code.

## Installation

Install AutomaticFormatter [Package Control](https://packagecontrol.io/search/AutomaticFormatter).

## Usage

### Key Bindings

Pressing <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd>, will activate AutomaticFormatter.

Settings
--------

There are three ways to set options, please refer to http://astyle.sourceforge.net/astyle.html for more information.

For **per-project settings** can add a `.astylerc` file to the `project_path`, **only support long options**.

```json
# .astylerc
--style=google
--indent=force-tab=4
...
```

Acknowledgement
-------

- [Artistic Style](http://astyle.sourceforge.net/)

  A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI, Objective‑C, C#, and Java Source Code.

- [SublimeAStyleFormatter](https://github.com/timonwong/SublimeAStyleFormatter)

  A code formatter/beautifier for Sublime Text 2 & 3.

- [pyastyle](https://github.com/MambaWong/pyastyle)

  Python Binding for Artistic Style.
