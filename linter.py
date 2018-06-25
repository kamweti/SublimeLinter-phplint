import re
from SublimeLinter.lint import Linter


class PHPLint(Linter):
    cmd = 'phpl --print-path relative --print-column-number --no-overall ${args} ${file}'
    regex = (
        r'(?i)^(?:'
        r'\t.*?\r?\n)?'
        r'==== (?P<line>\d+):(?P<col>.*): '
        r'(?:(?P<error>error)|(?P<warning>warning|notice)): '
        r'(?P<message>[^`\r\n]*(?:`(?P<near>[^\']+)\')?[^\r\n]*)'
    )
    multiline = True
    tempfile_suffix = '-'
    defaults = {
        'selector': 'source.php, text.html.basic'
    }

    def should_message_be_ignored(message):
        matches_to_ignore = [
            "'if\\(EXPR\\)':",
            "'while\\(EXPR\\)': expected expression",
            "embedded variable in string",
            "found EXPR of type mixed, expected a string",
            "expected number or array but found mixed",
            "the method.*?does not exist",
            "method.*?with signature",
            "invalid argument of type",
            "'EXPR . ...",
            "'... . EXPR",
            "invalid array index",
            "undefined class",
            "unknown class",
            "undefined type for argument",
            "'->' operator applied to a value of type mixed",
            "method .*?: expected return type boolean, found expression of type",
            "undeclared constant 'MYSQL_ASSOC'",
            "cannot assign a value of type string to a variable of type",
            "using unassigned variable",
            "comparing \\(string",
            "'...\\? EXPR1 : EXPR2': type mismatch",
            "variable .*? might not have been",
            ".*?too many arguments",
            "invalid PHPLint",
            ".*?requires more arguments",
            "variable .*? has not been assigned",
            "undeclared parent class",
            "property .*? does not exist",
            "unknown line tag",
            "invalid scope for documentation",
            "undeclared constant",
            "undefined type for property",
            "invalid parameter name",
            "invalid DocBlock",
            "missing statement terminator",
            "invalid variable-name function",
            ".*? requires arguments",
            "EXPR ? ...:...: expected expression of the type boolean",
            "'\\+\\+' applied to mixed",
            "unknown type",
            "unknown constant",
            "unknown method",
            "unresolved function",
            "invalid file",
            "'foreach\\(EXPR",
            "'->' operator applied"
        ]

        for match in matches_to_ignore:
            if re.search(match, message) != None:
                return True

    def split_match(self, match):
        """Return the match with ` quotes transformed to '."""
        match, line, col, error, warning, message, near = super().split_match(match)

        if message == 'no PHP code found at all':
            match = None
        elif PHPLint.should_message_be_ignored(message):
            match = None
        else:
            message = message.replace('`', '\'')

            # If the message contains a complaint about a function
            # and near looks like a function reference, remove the trailing
            # () so it can be found.
            if 'function \'' in message and near and near.endswith('()'):
                near = near[:-2]

        return match, line, col, error, warning, message, near
