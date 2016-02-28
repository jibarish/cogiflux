#!/usr/bin/env python3

import pyparsing as pp

# BNF
# tag     ::= "@" <strlit>
# content ::= {<strlit>}
# block   ::= "{" content "}"
# cfunit  ::= tag {tag} content "/n" | block
# doc     ::= {cfunit}

# Defs
# first = pp.Word(pp.alphas+"_", exact=1)
# rest = pp.Word(pp.alphanums+"_")
# identifier = first+pp.Optional(rest)



at     = pp.Literal('@')  # pp.Word("@", exact=1)
lcb    = pp.Literal('{')
rcb    = pp.Literal('}')
strlit = pp.Word(pp.alphanums)
tag    = at + strlit
inline_content = pp.CharsNotIn('\n')
block_content  = pp.OneOrMore(pp.CharsNotIn(['{', '}']))
inline = pp.OneOrMore(inline_content)
block  = lcb + pp.OneOrMore(block_content) + rcb
inline_unit = pp.OneOrMore(tag) + inline
block_unit  = pp.OneOrMore(tag) + block
cfunit = block_unit | inline_unit
# cfdoc  = pp.OneOrMore(cfunit)

# Code
testList = [
    # Valid cfunits
    '@idea make a superintelligent machine\n',
    '@quote "The best laid plans..." - RB\n',
    '@watch @steph scotland, pa\n',
    '@ok {ant bee crow}',
    '@todo { water tree, play with peps, holla }',
    '@todo {\nwater tree\nplay with peps\nholla\n}',
    # Not valid
    "", "1", "$*", "a_#"
]

def test(s):
    print ("---Test for '{0}'".format(s))
    try:
        result = cfunit.parseString(s)
        print ("  Matches: {0}".format(result))
    except pp.ParseException as x:
        print ("  No match: {0}".format(str(x)))
    print ()

def main():
    for text in testList:
        test(text)

if __name__ == "__main__":
    main()
