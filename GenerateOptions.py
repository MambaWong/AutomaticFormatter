import os
import re


class InvalidOption(Exception):
    def __init__(self, option_name, option_value):
        self.name = option_name
        self.value = option_value

    def __str__(self):
        return f"--{self.name}={self.value}. Please refer to http://astyle.sourceforge.net/astyle.html.\n"


default_options = {
    # === Brace Style Options ===
    "style": None,
    # === Tab options ===
    "indent": "spaces=4",
    # === Brace Modify Options ===
    "attach-namespaces": False,
    "attach-classes": False,
    "attach-inlines": False,
    "attach-extern-c": False,
    "attach-closing-while": False,
    # === Indentation Options ===
    "indent-classes": False,
    "indent-modifiers": False,
    "indent-switches": False,
    "indent-cases": False,
    "indent-namespaces": False,
    "indent-after-parens": False,
    "indent-continuation": None,
    "indent-labels": False,
    "indent-preproc-block": False,
    "indent-preproc-define": False,
    "indent-preproc-cond": False,
    "indent-col1-comments": False,
    "min-conditional-indent": None,
    "max-continuation-indent": None,
    # === Padding Options ===
    "break-blocks": None,
    "pad-oper": False,
    "pad-comma": False,
    "pad-paren": False,
    "pad-paren-out": False,
    "pad-first-paren-out": False,
    "pad-paren-in": False,
    "pad-header": False,
    "unpad-paren": False,
    "delete-empty-lines": False,
    "fill-empty-lines": False,
    "align-pointer": "name",
    "align-reference": "type",
    # === Formatting Options ===
    "break-closing-braces": False,
    "break-elseifs": False,
    "break-one-line-headers": False,
    "add-braces": False,
    "add-one-line-braces": False,
    "remove-braces": False,
    "break-return-type": False,
    "break-return-type-decl": False,
    "attach-return-type": False,
    "attach-return-type-decl": False,
    "keep-one-line-blocks": False,
    "keep-one-line-statements": False,
    "convert-tabs": False,
    "close-templates": False,
    "remove-comment-prefix": False,
    "max-code-length": None,
    "break-after-logical": False,
    # === Objective-C Options ===
    "pad-method-prefix": False,
    "unpad-method-prefix": False,
    "pad-return-type": False,
    "unpad-return-type": False,
    "pad-param-type": False,
    "unpad-param-type": False,
    "align-method-colon": False,
    "pad-method-colon": None,
    "align-method-colon": False,
    "pad-method-colon": None
}


def filter_options(options):
    return {option: options[option] for option in options if option in default_options and options[option] != default_options[option]}


STYLE_OPTIONS = {
    "allman", "bsd", "break",
    "java", "attach",
    "kr", "k&r", "k/r",
    "stroustrup",
    "whitesmith",
    "vtk",
    "ratliff ", "banner",
    "gnu",
    "linux", "knf",
    "horstmann", "run-in",
    "1tbs", "otbs",
    "google",
    "mozilla",
    "pico", "lisp", "python"
}
INDENT_OPTIONS = {"spaces", "tab", "force-tab", "force-tab-x"}
ALIGN_POINTER_OPTIONS = {"type", "middle", "name"}
ALIGN_REFERENCE_OPTIONS = {"none", "type", "middle", "name"}
PAD_METHOD_COLON_OPTIONS = {"none", "all", "after", "before"}


def generate_astyle_options(options):
    astyle_options = []

    filtered_options = filter_options(options)

    for option_name, option_value in filtered_options.items():
        if "style" == option_name:
            if option_value is None:
                continue
            if option_value not in STYLE_OPTIONS:
                raise InvalidOption(option_name, option_value)
            astyle_options.append(f"--style={option_value}")
        elif "indent" == option_name:
            if option_value is None:
                astyle_options.append(f"--indent=spaces=4")
                continue
            option, _, spaces = option_value.partition('=')
            if option not in INDENT_OPTIONS:
                raise InvalidOption(option_name, option_value)
            if spaces == "":
                astyle_options.append(f"--indent={option}")
            elif spaces.isdigit():
                number = max(2, min(int(spaces), 20))
                astyle_options.append(f"--indent={option}={number}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "attach-namespaces" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-namespaces")
        elif "attach-classes" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-classes")
        elif "attach-inlines" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-inlines")
        elif "attach-extern-c" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-extern-c")
        elif "attach-closing-while" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-closing-while")
        elif "indent-classes" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-classes")
        elif "indent-modifiers" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-modifiers")
        elif "indent-switches" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-switches")
        elif "indent-cases" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-cases")
        elif "indent-namespaces" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-namespaces")
        elif "indent-after-parens" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-after-parens")
        elif "indent-continuation" == option_name:
            if option_value is None:
                astyle_options.append(f"--indent-continuation=1")
                continue
            if isinstance(option_value, int):
                number = max(0, min(int(option_value), 4))
                astyle_options.append(f"--indent-continuation={number}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "indent-labels" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-labels")
        elif "indent-preproc-block" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-preproc-block")
        elif "indent-preproc-define" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-preproc-define")
        elif "indent-preproc-cond" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-preproc-cond")
        elif "indent-col1-comments" == option_name:
            if option_value is True:
                astyle_options.append(f"--indent-col1-comments")
        elif "min-conditional-indent" == option_name:
            if option_value is None:
                continue
            if isinstance(option_value, int):
                number = max(0, min(int(option_value), 3))
                astyle_options.append(f"--min-conditional-indent={number}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "max-continuation-indent" == option_name:
            if option_value is None:
                continue
            if isinstance(option_value, int):
                number = max(40, min(int(option_value), 120))
                astyle_options.append(f"--max-continuation-indent={number}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "break-blocks" == option_name:
            if option_value is None:
                continue
            if option_value == "":
                astyle_options.append(f"--break-blocks")
            elif option_value == "all":
                astyle_options.append(f"--break-blocks={option_value}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "pad-oper" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-oper")
        elif "pad-comma" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-comma")
        elif "pad-paren" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-paren")
        elif "pad-paren-out" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-paren-out")
        elif "pad-first-paren-out" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-first-paren-out")
        elif "pad-paren-in" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-paren-in")
        elif "pad-header" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-header")
        elif "unpad-paren" == option_name:
            if option_value is True:
                astyle_options.append(f"--unpad-paren")
        elif "delete-empty-lines" == option_name:
            if option_value is True:
                astyle_options.append(f"--delete-empty-lines")
        elif "fill-empty-lines" == option_name:
            if option_value is True:
                astyle_options.append(f"--fill-empty-lines")
        elif "align-pointer" == option_name:
            if option_value is None:
                continue
            if option_value in ALIGN_POINTER_OPTIONS:
                astyle_options.append(f"--align-pointer={option_value}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "align-reference" == option_name:
            if option_value is None:
                continue
            if option_value in ALIGN_REFERENCE_OPTIONS:
                astyle_options.append(f"--align-reference={option_value}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "break-closing-braces" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-closing-braces")
        elif "break-elseifs" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-elseifs")
        elif "break-one-line-headers" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-one-line-headers")
        elif "add-braces" == option_name:
            if option_value is True:
                astyle_options.append(f"--add-braces")
        elif "add-one-line-braces" == option_name:
            if option_value is True:
                astyle_options.append(f"--add-one-line-braces")
        elif "remove-braces" == option_name:
            if option_value is True:
                astyle_options.append(f"--remove-braces")
        elif "break-return-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-return-type")
        elif "break-return-type-decl" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-return-type-decl")
        elif "attach-return-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-return-type")
        elif "attach-return-type-decl" == option_name:
            if option_value is True:
                astyle_options.append(f"--attach-return-type-decl")
        elif "keep-one-line-blocks" == option_name:
            if option_value is True:
                astyle_options.append(f"--keep-one-line-blocks")
        elif "keep-one-line-statements" == option_name:
            if option_value is True:
                astyle_options.append(f"--keep-one-line-statements")
        elif "convert-tabs" == option_name:
            if option_value is True:
                astyle_options.append(f"--convert-tabs")
        elif "close-templates" == option_name:
            if option_value is True:
                astyle_options.append(f"--close-templates")
        elif "remove-comment-prefix" == option_name:
            if option_value is True:
                astyle_options.append(f"--remove-comment-prefix")
        elif "max-code-length" == option_name:
            if option_value is None:
                continue
            if isinstance(option_value, int):
                number = max(50, min(option_value, 200))
                astyle_options.append(f"--max-code-length={number}")
            else:
                raise InvalidOption(option_name, option_value)
        elif "break-after-logical" == option_name:
            if option_value is True:
                astyle_options.append(f"--break-after-logical")
        elif "pad-method-prefix" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-method-prefix")
        elif "unpad-method-prefix" == option_name:
            if option_value is True:
                astyle_options.append(f"--unpad-method-prefix")
        elif "pad-return-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-return-type")
        elif "unpad-return-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--unpad-return-type")
        elif "pad-param-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-param-type")
        elif "unpad-param-type" == option_name:
            if option_value is True:
                astyle_options.append(f"--unpad-param-type")
        elif "align-method-colon" == option_name:
            if option_value is True:
                astyle_options.append(f"--align-method-colon")
        elif "pad-method-colon" == option_name:
            if option_value is True:
                astyle_options.append(f"--pad-method-colon")
        elif "align-method-colon" == option_name:
            if option_value is True:
                astyle_options.append(f"--align-method-colon")
        elif "pad-method-colon" == option_name:
            if option_value is None:
                continue
            if option_value in PAD_METHOD_COLON_OPTIONS:
                astyle_options.append(f"--pad-method-colon={option_value}")
            else:
                raise InvalidOption(option_name, option_value)
        else:
            pass

    return filtered_options, astyle_options


def parse_file_options(file_name):
    options = dict()
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            match = re.match(r"(--)([a-z0-9\-=]+)", line)
            if match is not None:
                option_name, _, option_value = match.group(2).partition("=")
                if option_value == "":
                    option_value = True
                else:
                    option_value = int(option_value) if option_value.isdigit() else option_value
                options[option_name] = option_value

    filtered_options, _ = generate_astyle_options(options)

    return filtered_options


def parse_default_file_options(option_file):
    options = dict()
    if option_file == "none" or option_file is None:
        return None
    file_name = option_file if option_file != "" and os.path.isfile(option_file) and os.path.exists(option_file) else ""
    if file_name == "":
        file_name = os.environ.get("ARTISTIC_STYLE_OPTIONS", "")
        file_name = file_name if file_name != "" and os.path.isfile(file_name) and os.path.exists(file_name) else ""
    if file_name == "":
        home_path = os.environ.get("HOME", "")
        file_name = os.path.join(home_path, ".astylerc") if home_path != "" else ""
        file_name = file_name if os.path.exists(file_name) else ""
    if file_name == "":
        appdata_path = os.environ.get("APPDATA", "")
        file_name = os.path.join(appdata_path, "astylerc") if appdata_path != "" else ""
        file_name = file_name if os.path.exists(file_name) else ""
    if file_name != "":
        options = parse_file_options(file_name)
    else:
        raise

    return options


def parse_project_file_options(option_file, project_path):
    options = dict()
    if project_path == "":
        return None
    if option_file == "none" or option_file is None:
        return None
    file_name = option_file if option_file != "" and os.path.isfile(option_file) and os.path.exists(option_file) else ""
    if file_name == "":
        file_name = os.path.join(project_path, ".astylerc")
        file_name = file_name if os.path.exists(file_name) else ""
    if file_name == "":
        file_name = os.environ.get("ARTISTIC_STYLE_PROJECT_OPTIONS", "")
        file_name = file_name if file_name != "" and os.path.isfile(file_name) and os.path.exists(file_name) else ""
    if file_name != "":
        options = parse_file_options(file_name)
    else:
        raise

    return options
