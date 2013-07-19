from docopt import docopt
from pymo import main


_PROGRAM_ARGS = """
USAGE:
    pymo [-f FORMAT -p PAD -v -n (-l|-c|-m) -t TRANSFORMS] <inputdir> <outputdir>
OPTIONS:
    -f FORMAT       Format. Default is "%p/%a/%t-%n", where:
                        %n:  Song title
                        %t:  Track number
                        %a:  Album
                        %p:  Performer
                        %g:  Genre
                        %c:  Comment
                        %y:  Release year
    -t TRANSFORMS   Text Transforms. A comma seperated list of any of the
                    following:
                        lc: lower case
                        uc: UPPER CASE
                        cc: CamelCase (removes spaces)
                        jc: javaCase (removes spaces)
                        us: Replace spaces with underscores
                        rs: Remove spaces
                        rp: Remove punctuation
                            [any of: !@#$%^&*():;?=+~`<>, ]
                        pu: Convert punctuation to underscore
    -p PAD          Width of padding (0 = Don't pad) [DEFAULT: 2]
    -v              Be verbose (prints move/link/copy commands)
    -n              Do a dry run (just print which files would be moved)
    -m              Move files (DEFAULT)
    -c              Copy files
    -l              Symlink files
"""


opts = docopt(_PROGRAM_ARGS)
main(opts)
