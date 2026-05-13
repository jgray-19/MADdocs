# -- Custom Lexer ------------------------------------------------------------
from pygments.lexers.scripting import LuaLexer
from pygments.token import Comment, Keyword, Name, Operator


class MadLexer(LuaLexer):
    """
    MAD-NG lexer, extending LuaLexer with MAD-specific syntax.

    Changes from LuaLexer:
    - ``!`` is a line comment character (in addition to ``--``).
    - ``\\`` and ``:=`` are operators.
    - MAD physics commands (track, twiss, …) are highlighted as keywords.
    - MAD built-in globals (MAD, MADX, beam, …) are highlighted as built-in names.
    """

    name = 'MAD'
    url = "https://mad.web.cern.ch/mad/"
    aliases = ['mad']
    filenames = ['*.mad']
    mimetypes = []

    # Physics / simulation commands
    _MAD_COMMANDS = {
        "track",
        "twiss",
        "survey",
        "cofind",
        "match",
        "correct",
        "sectormap",
    }

    # Core MAD globals and constructors
    _MAD_BUILTINS = {
        "MAD",
        "MADX",
        "beam",
        "sequence",
        "element",
        "damap",
        "mtable",
        "matrix",
        "vector",
        "object",
        "prototype",
    }

    # MAD standard modules / sub-namespaces
    _MAD_MODULES = {
        "MAD.element",
        "MAD.sequence",
        "MAD.beam",
        "MAD.twiss",
        "MAD.track",
        "MAD.survey",
        "MAD.cofind",
        "MAD.match",
        "MAD.gmath",
        "MAD.gfunc",
        "MAD.gtable",
        "MAD.utility",
        "MAD.utest",
        "MAD.regex",
        "MAD.complex",
        "MAD.range",
        "MAD.tpsa",
        "MAD.monomial",
        "MAD.damap",
    }

    tokens = {
        **LuaLexer.tokens,
        "ws": [
            (r"(?:!.*$)", Comment.Single),
            *LuaLexer.tokens["ws"],
        ],
        "base": [
            (r"\\", Operator),
            (r":=", Operator),
            # MAD physics commands
            (r"\b(" + "|".join(list(_MAD_COMMANDS)) + r")\b", Keyword.Declaration),
            # MAD built-in globals
            (r"\b(" + "|".join(list(_MAD_BUILTINS)) + r")\b", Name.Builtin),
            *LuaLexer.tokens["base"],
        ],
    }
