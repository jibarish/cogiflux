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



at      = pp.Literal('@')  # pp.Word("@", exact=1)
strlit  = pp.Word(pp.alphanums)
tag     = at + strlit
inline_content = pp.CharsNotIn('\n')
# block_content =
# block   =
cfunit  = pp.LineStart() + pp.OneOrMore(tag) \
                    + pp.OneOrMore(inline_content) + pp.LineEnd()



doc     = pp.OneOrMore(cfunit)

# Code
testList = [
    # Valid cfunits
    '@idea make a superintelligent machine\n',
    '@quote "The best laid plans..." - RB\n',
    '@watch @steph scotland, pa\n',
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

def main():
    for text in testList:
        test(text)

if __name__ == "__main__":
    main()
