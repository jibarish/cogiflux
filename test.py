#!/usr/bin/env python3

import pyparsing as pp

# ----------------------------------------------------
#       BNF
# ----------------------------------------------------
# at             ::= "@"
# lcb            ::= "{"
# rcb            ::= "}"
# us             ::= "_"
# strlit         ::= ( A-Ba-b0-9 )
# taghead        ::= at | us
# tag            ::= taghead strlit
# taglist        ::= { tag }
# inline_content ::= { ^( \n ) }
# block_content  ::= { ^( \{\} ) }
# inline         ::= { inline_content }
# block          ::= lcb { block_content } rcb
# content        ::= block | inline
# cfunit         ::= taglist + [ content ]
# cfdoc          ::= { cfunit }
# ----------------------------------------------------

#
# Grammar
#
at             = pp.Literal('@').suppress()
lcb            = pp.Literal('{').suppress()
rcb            = pp.Literal('}').suppress()
us             = pp.Literal('_').suppress()
strlit         = pp.Word(pp.alphanums)
taghead        = at | us
tag            = taghead + strlit
taglist        = pp.Group(pp.OneOrMore(tag)).setResultsName('tags')
inline_content = pp.CharsNotIn('\n')
block_content  = pp.CharsNotIn([lcb, rcb])
inline         = pp.OneOrMore(inline_content)
block          = lcb + pp.OneOrMore(block_content) + rcb
content        = (block | inline).setResultsName('content')
cfunit         = pp.Group(taglist + pp.Optional(content, default=''))
cfdoc          = pp.OneOrMore(cfunit)

#
# Testing
#
def test_cfunit():
    testlist = [
        # Valid cfunits
        '@idea make a superintelligent machine',
        '@quote "The best laid plans..." - RB',
        '@watch @steph scotland, pa',
        '@ok {ant bee crow}',
        '@todo { water tree, play with peps, holla }',
        '@todo {\nwater tree\nplay with peps\nholla\n}',
        # Not valid
        "", "1", "$*", "a_#"
    ]
    for text in testlist:
        test_one(text)

def test_one(s):
    print ("---Test for '{0}'".format(s))
    try:
        result = cfunit.parseString(s)
        # Printing
        print ("\ttags: {0}".format(result[0]['tags']))
        print ("\tcontent: {0}".format(result[0]['content']))
    except pp.ParseException as x:
        print ("  No match: {0}".format(str(x)))
    print ()

def test_cfdoc(filename):
    try:
        result = cfdoc.parseFile(filename, parseAll=False)
        # Printing
        i = 1
        for each in result:
            print ("Entry {0}:".format(i))
            print ("\ttags: {0}".format(each['tags']))
            print ("\tcontent: {0}".format(each['content']))
            print ()
            i += 1
    except pp.ParseException as x:
        print ("  No match: {0}".format(str(x)))
    print ()

def main():
    # test_cfunit()
    test_cfdoc("input.cflux")

if __name__ == "__main__":
    main()
