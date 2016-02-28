#!/usr/bin/env python3

import pyparsing as pp

# ----------------------------------------------------
#       BNF
# ----------------------------------------------------
# at             ::= "@"
# lcb            ::= "{"
# rcb            ::= "}"
# strlit         ::= ( A-Ba-b0-9 )
# tag            ::= at strlit
# inline_content ::= { ^( \n ) }
# block_content  ::= { ^( \{\} ) }
# inline         ::= { inline_content }
# block          ::= lcb { block_content } rcb
# inline_unit    ::= { tag } inline
# block_unit     ::= { tag } block
# cfunit         ::= block_unit | inline_unit
# cfdoc          ::= { cfunit }
# ----------------------------------------------------

#
# Grammar
#
at             = pp.Literal('@')
lcb            = pp.Literal('{')
rcb            = pp.Literal('}')
strlit         = pp.Word(pp.alphanums)
tag            = at + strlit
inline_content = pp.CharsNotIn('\n')
block_content  = pp.OneOrMore(pp.CharsNotIn(['{', '}']))
inline         = pp.OneOrMore(inline_content)
block          = lcb + pp.OneOrMore(block_content) + rcb
inline_unit    = pp.OneOrMore(tag) + inline
block_unit     = pp.OneOrMore(tag) + block
cfunit         = block_unit | inline_unit
cfdoc          = pp.OneOrMore(cfunit)

#
# Testing
#
def test_singles():
    testlist = [
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
    for text in testlist:
        test_single(text)

def test_single(s):
    print ("---Test for '{0}'".format(s))
    try:
        result = cfunit.parseString(s)
        print ("  Matches: {0}".format(result))
    except pp.ParseException as x:
        print ("  No match: {0}".format(str(x)))
    print ()

def test_file(filename):
    with open(filename, 'r') as infile:
        s = infile.read()

    print ("---Test for '{0}'".format(s))
    try:
        result = cfdoc.parseString(s)
        # print ("  Matches: {0}".format(result))
        for each in result:
            print ("  Matches: {0}".format(each))
    except pp.ParseException as x:
        print ("  No match: {0}".format(str(x)))
    print ()

def main():
    # test_singles()
    # test_file("input.cflux")

if __name__ == "__main__":
    main()
