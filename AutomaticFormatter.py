import sublime
import sublime_plugin

from . import pyastyle
from .GenerateOptions import InvalidOption, filter_options, generate_astyle_options, parse_default_file_options, parse_project_file_options


PLUGIN_NAME = 'AutomaticFormatter'
autoformat_on_save = False
syntax_mode = None
default_option_file = None
project_option_file = None
command_line_options = None

SYNTAX_MODE = {
    'C': 'C',
    'C++': 'C',
    "C++ (Header)": "C",
    'OBJC': 'C',
    'OBJC++': 'C',
    'OPENCL': 'C',
    'CUDA-C++': 'C',
    'CS': 'CS',
    'JAVA': 'JAVA',
}


def load_settings():
    global autoformat_on_save
    global syntax_mode
    global default_option_file
    global project_option_file
    global command_line_options

    settings = sublime.load_settings('AutomaticFormatter.sublime-settings')

    autoformat_on_save = settings.get("autoformat_on_save", False)

    syntax_mode = SYNTAX_MODE.copy()
    syntax_mode.update(settings.get('user_defined_syntax_mode_mapping', {}))
    # syntax_mode = {syntax.upper(): mode.upper() for syntax, mode in syntax_mode.items()}

    default_option_file = settings.get("default_option_file", None)
    project_option_file = settings.get("project_option_file", None)

    command_line_options = filter_options(settings.to_dict())


def plugin_loaded():
    load_settings()


class AutomaticFormatterCommand(sublime_plugin.TextCommand):
    def generate_options(self):
        options = dict()

        default_file_options = parse_default_file_options(default_option_file)
        if default_file_options is not None:
            options.update(default_file_options)

        project_path = self.view.window().extract_variables().get("project_path", "")
        project_file_options = parse_project_file_options(project_option_file, project_path)
        if project_file_options is not None:
            options.update(project_file_options)

        options.update(command_line_options)

        view_settings = self.view.settings()
        translate_tabs_to_spaces = view_settings.get('translate_tabs_to_spaces')
        tab_size = view_settings.get('tab_size')
        if translate_tabs_to_spaces is True:
            options.update({"indent": f"spaces={tab_size}", "convert-tabs": True})

        _, astyle_options = generate_astyle_options(options)

        syntax = self.view.syntax().name
        mode = syntax_mode.get(syntax, "")
        if not mode == "":
            astyle_options.append(f"--mode={mode.lower()}")

        astyle_options = ' '.join(option for option in astyle_options)
        return astyle_options

    def run(self, edit):
        try:
            options = self.generate_options()
        except InvalidOption as e:
            sublime.error_message(e)
            return

        view = self.view
        region = sublime.Region(0, view.size())
        code = view.substr(region)
        formatted_code = pyastyle.as_format(code, options)
        if code != formatted_code:
            view.replace(edit, region, formatted_code)

    def is_enabled(self):
        return self.view.syntax().name in syntax_mode


class PluginEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if autoformat_on_save and view.syntax().name in syntax_mode:
            view.run_command('automatic_formatter')

    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'astyleformat_is_enabled':
            return view.syntax().name in syntax_mode
        return None
