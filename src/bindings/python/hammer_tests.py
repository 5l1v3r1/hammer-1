import unittest
import hammer as h

class TestTokenParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_token("95\xa2", 3)
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "95\xa2", 3).ast.token_data.bytes, "95\xa2")
    def test_partial_fails(self):
        self.assertEqual(h.h_parse(self.parser, "95", 2), None)

class TestChParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_int = h.h_ch(0xa2)
        cls.parser_chr = h.h_ch("\xa2")
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser_int, "\xa2", 1).ast.token_data.uint, 0xa2)
        self.assertEqual(h.h_parse(self.parser_chr, "\xa2", 1).ast.token_data.uint, ord("\xa2"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser_int, "\xa3", 1), None)
        self.assertEqual(h.h_parse(self.parser_chr, "\xa3", 1), None)

class TestChRange(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_ch_range("a", "c")
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "b", 1).ast.token_data.uint, ord("b"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "d", 1), None)

class TestInt64(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_int64()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\xff\xff\xff\xfe\x00\x00\x00\x00", 8).ast.token_data.sint, -0x200000000)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\xff\xff\xff\xfe\x00\x00\x00", 7), None)

class TestInt32(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_int32()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\xff\xfe\x00\x00", 4).ast.token_data.sint, -0x20000)
        self.assertEqual(h.h_parse(self.parser, "\x00\x02\x00\x00", 4).ast.token_data.sint, 0x20000)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\xff\xfe\x00", 3), None)
        self.assertEqual(h.h_parse(self.parser, "\x00\x02\x00", 3), None)

class TestInt16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_int16()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\xfe\x00", 2).ast.token_data.sint, -0x200)
        self.assertEqual(h.h_parse(self.parser, "\x02\x00", 2).ast.token_data.sint, 0x200)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\xfe", 1), None)
        self.assertEqual(h.h_parse(self.parser, "\x02", 1), None)

class TestInt8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_int8()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x88", 1).ast.token_data.sint, -0x78)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "", 0), None)

class TestUint64(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_uint64()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x00\x00\x00\x02\x00\x00\x00\x00", 8).ast.token_data.uint, 0x200000000)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\x00\x00\x00\x02\x00\x00\x00", 7), None)

class TestUint32(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_uint32()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x00\x02\x00\x00", 4).ast.token_data.uint, 0x20000)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\x00\x02\x00", 3), None)

class TestUint16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_uint16()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x02\x00", 2).ast.token_data.uint, 0x200)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\x02", 1), None)

class TestUint8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_uint8()
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x78", 1).ast.token_data.uint, 0x78)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "", 0), None)
        
class TestIntRange(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_int_range(h.h_uint8(), 3, 10)
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "\x05", 1).ast.token_data.uint, 5)
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "\x0b", 1), None)

class TestWhitespace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_whitespace(h.h_ch("a"))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1).ast.token_data.uint, ord("a"))
        self.assertEqual(h.h_parse(self.parser, " a", 2).ast.token_data.uint, ord("a"))
        self.assertEqual(h.h_parse(self.parser, "  a", 3).ast.token_data.uint, ord("a"))
        self.assertEqual(h.h_parse(self.parser, "\ta", 2).ast.token_data.uint, ord("a"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "_a", 2), None)

class TestWhitespaceEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_whitespace(h.h_end_p())
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "", 0).ast, None) # empty string
        self.assertEqual(h.h_parse(self.parser, "  ", 2).ast, None) # empty string
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "  x", 3), None)

class TestLeft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_left(h.h_ch("a"), h.h_ch(" "))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "a ", 2).ast.token_data.uint, ord("a"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)
        self.assertEqual(h.h_parse(self.parser, " ", 1), None)
        self.assertEqual(h.h_parse(self.parser, "ab", 2), None)

class TestRight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_right(h.h_ch(" "), h.h_ch("a"))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, " a", 2).ast.token_data.uint, ord("a"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)
        self.assertEqual(h.h_parse(self.parser, " ", 1), None)
        self.assertEqual(h.h_parse(self.parser, "ba", 2), None)

class TestMiddle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_middle(h.h_ch(" "), h.h_ch("a"), h.h_ch(" "))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, " a ", 3).ast.token_data.uint, ord("a"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)
        self.assertEqual(h.h_parse(self.parser, " ", 1), None)
        self.assertEqual(h.h_parse(self.parser, " a", 2), None)
        self.assertEqual(h.h_parse(self.parser, "a ", 2), None)
        self.assertEqual(h.h_parse(self.parser, " b ", 3), None)
        self.assertEqual(h.h_parse(self.parser, "ba ", 3), None)
        self.assertEqual(h.h_parse(self.parser, " ab", 3), None)

# class TestAction(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.parser = h.h_action(h.h_sequence__a([h.h_choice__a([h.h_ch("a"), h.h_ch("A"), None]), h.h_choice__a([h.h_ch("b"), h.h_ch("B"), None]), None]), lambda x: [y.upper() for y in x])
#     def test_success(self):
#         self.assertEqual(h.h_parse(self.parser, "ab", 2).ast.token_data.seq, ["A", "B"])
#         self.assertEqual(h.h_parse(self.parser, "AB", 2).ast.token_data.seq, ["A", "B"])
#     def test_failure(self):
#         self.assertEqual(h.h_parse(self.parser, "XX", 2), None)

class TestIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_in("abc", 3)
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "b", 1).ast.token_data.uint, ord("b")) 
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "d", 1), None)

class TestNotIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_not_in("abc", 3)
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "d", 1).ast.token_data.uint, ord("d"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)

class TestEndP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_end_p(), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a", 1).ast.token_data.seq], [ord(y) for y in ["a"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "aa", 2), None)

class TestNothingP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_nothing_p()
    def test_success(self):
        pass
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)

class TestSequence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_ch("b"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "ab", 2).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)
        self.assertEqual(h.h_parse(self.parser, "b", 1), None)

class TestSequenceWhitespace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_whitespace(h.h_ch("b")), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "ab", 2).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a b", 3).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a  b", 4).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a  c", 4), None)

class TestChoice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_choice__a([h.h_ch("a"), h.h_ch("b"), None])
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1).ast.token_data.uint, ord("a"))
        self.assertEqual(h.h_parse(self.parser, "b", 1).ast.token_data.uint, ord("b"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "c", 1), None)

class TestButNot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_butnot(h.h_ch("a"), h.h_token("ab", 2))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1).ast.token_data.uint, ord("a"))
        self.assertEqual(h.h_parse(self.parser, "aa", 2).ast.token_data.uint, ord("a"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "ab", 2), None)

class TestButNotRange(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_butnot(h.h_ch_range("0", "9"), h.h_ch("6"))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "4", 1).ast.token_data.uint, ord("4"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "6", 1), None)

class TestDifference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_difference(h.h_token("ab", 2), h.h_ch("a"))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "ab", 2).ast.token_data.bytes, "ab")
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)

class TestXor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_xor(h.h_ch_range("0", "6"), h.h_ch_range("5", "9"))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "0", 1).ast.token_data.uint, ord("0"))
        self.assertEqual(h.h_parse(self.parser, "9", 1).ast.token_data.uint, ord("9"))
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "5", 1), None)
        self.assertEqual(h.h_parse(self.parser, "a", 1), None)

class TestMany(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_many(h.h_choice__a([h.h_ch("a"), h.h_ch("b"), None]))
    def test_success(self):
        self.assertEqual(h.h_parse(self.parser, "", 0).ast.token_data.seq, [])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a", 1).ast.token_data.seq], [ord(y) for y in ["a"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "b", 1).ast.token_data.seq], [ord(y) for y in ["b"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "aabbaba", 7).ast.token_data.seq], [ord(y) for y in ["a", "a", "b", "b", "a", "b", "a"]])
    def test_failure(self):
        pass

class TestMany1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_many1(h.h_choice__a([h.h_ch("a"), h.h_ch("b"), None]))
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a", 1).ast.token_data.seq], [ord(y) for y in ["a"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "b", 1).ast.token_data.seq], [ord(y) for y in ["b"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "aabbaba", 7).ast.token_data.seq], [ord(y) for y in ["a", "a", "b", "b", "a", "b", "a"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "", 0), None)
        self.assertEqual(h.h_parse(self.parser, "daabbabadef", 11), None)

class TestRepeatN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_repeat_n(h.h_choice__a([h.h_ch("a"), h.h_ch("b"), None]), 2)
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "abdef", 5).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "adef", 4), None)
        self.assertEqual(h.h_parse(self.parser, "dabdef", 5), None)

class TestOptional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_optional(h.h_choice__a([h.h_ch("b"), h.h_ch("c"), None])), h.h_ch("d"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "abd", 3).ast.token_data.seq], [ord(y) for y in ["a", "b", "d"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "acd", 3).ast.token_data.seq], [ord(y) for y in ["a", "c", "d"]])
        ### FIXME check this out in repl, what does tree look like
        #self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "ad", 2).ast.token_data.seq], [ord(y)["a", None, "d"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "aed", 3), None)
        self.assertEqual(h.h_parse(self.parser, "ab", 2), None)
        self.assertEqual(h.h_parse(self.parser, "ac", 2), None)

class TestIgnore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_ignore(h.h_ch("b")), h.h_ch("c"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "abc", 3).ast.token_data.seq], [ord(y) for y in ["a", "c"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "ac", 2), None)

class TestSepBy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sepBy(h.h_choice__a([h.h_ch("1"), h.h_ch("2"), h.h_ch("3"), None]), h.h_ch(","))
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,2,3", 5).ast.token_data.seq], [ord(y) for y in ["1", "2", "3"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,3,2", 5).ast.token_data.seq], [ord(y) for y in ["1", "3", "2"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,3", 3).ast.token_data.seq], [ord(y) for y in ["1", "3"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "3", 1).ast.token_data.seq], [ord(y) for y in ["3"]])
        self.assertEqual(h.h_parse(self.parser, "", 0).ast.token_data.seq, [])
    def test_failure(self):
        pass

class TestSepBy1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sepBy1(h.h_choice__a([h.h_ch("1"), h.h_ch("2"), h.h_ch("3"), None]), h.h_ch(","))
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,2,3", 5).ast.token_data.seq], [ord(y) for y in ["1", "2", "3"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,3,2", 5).ast.token_data.seq], [ord(y) for y in ["1", "3", "2"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "1,3", 3).ast.token_data.seq], [ord(y) for y in ["1", "3"]])
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "3", 1).ast.token_data.seq], [ord(y) for y in ["3"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "", 0), None)

### segfaults
class TestEpsilonP1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_epsilon_p(), h.h_ch("b"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "ab", 2).ast.token_data.seq], [ord(y) for y in ["a", "b"]])
    def test_failure(self):
        pass

class TestEpsilonP2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_epsilon_p(), h.h_ch("a"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a", 1).ast.token_data.seq], [ord(y) for y in ["a"]])
    def test_failure(self):
        pass

class TestEpsilonP3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_epsilon_p(), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a", 1).ast.token_data.seq], [ord(y) for y in ["a"]])
    def test_failure(self):
        pass

# class TestAttrBool(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.parser = h.h_attr_bool(h.h_many1(h.h_choice__a([h.h_ch("a"), h.h_ch("b"), None])), lambda x: x[0] == x[1])
#     def test_success(self):
#         self.assertEqual(h.h_parse(self.parser, "aa", 2).ast.token_data.seq, ["a", "a"])
#         self.assertEqual(h.h_parse(self.parser, "bb", 2).ast.token_data.seq, ["b", "b"])
#     def test_failure(self):
#         self.assertEqual(h.h_parse(self.parser, "ab", 2), None)

class TestAnd1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_and(h.h_ch("0")), h.h_ch("0"), None])
    def test_success(self):
         self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "0", 1).ast.token_data.seq], [ord(y) for y in ["0"]])
    def test_failure(self):
        pass

class TestAnd2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_and(h.h_ch("0")), h.h_ch("1"), None])
    def test_success(self):
        pass
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "0", 1), None)

class TestAnd3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("1"), h.h_and(h.h_ch("2")), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "12", 2).ast.token_data.seq], [ord(y) for y in ["1"]])
    def test_failure(self):
        pass

class TestNot1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_choice__a([h.h_ch("+"), h.h_token("++", 2), None]), h.h_ch("b"), None])
    def test_success(self):
        self.assertEqual([x.token_data.uint for x in h.h_parse(self.parser, "a+b", 3).ast.token_data.seq], [ord(y) for y in ["a", "+", "b"]])
    def test_failure(self):
        self.assertEqual(h.h_parse(self.parser, "a++b", 4), None)

class TestNot2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_sequence__a([h.h_ch("a"), h.h_choice__a([h.h_sequence__a([h.h_ch("+"), h.h_not(h.h_ch("+")), None]), h.h_token("++", 2), None]), h.h_ch("b"), None])
    def test_success(self):
        tree = h.h_parse(self.parser, "a+b", 3).ast.token_data.seq
        tree[1] = tree[1].token_data.seq[0]
        self.assertEqual([x.token_data.uint for x in tree], [ord(y) for y in ["a", "+", "b"]])
        tree = h.h_parse(self.parser, "a++b", 4).ast.token_data.seq
        tree[0] = chr(tree[0].token_data.uint)
        tree[1] = tree[1].token_data.bytes
        tree[2] = chr(tree[2].token_data.uint)
        self.assertEqual(tree, ["a", "++", "b"])
    def test_failure(self):
        pass

# ### this is commented out for packrat in C ...
# #class TestLeftrec(unittest.TestCase):
# #    @classmethod
# #    def setUpClass(cls):
# #        cls.parser = h.h_indirect()
# #        a = h.h_ch("a")
# #        h.h_bind_indirect(cls.parser, h.h_choice(h.h_sequence(cls.parser, a), a))
# #    def test_success(self):
# #        self.assertEqual(h.h_parse(self.parser, "a", 1).ast.token_data.bytes, "a")
# #        self.assertEqual(h.h_parse(self.parser, "aa", 2).ast.token_data.seq, ["a", "a"])
# #        self.assertEqual(h.h_parse(self.parser, "aaa", 3).ast.token_data.seq, ["a", "a", "a"])
# #    def test_failure(self):
# #        pass

class TestARightrec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = h.h_indirect()
        a = h.h_ch("a")
        h.h_bind_indirect(cls.parser, h.h_choice__a([h.h_sequence__a([a, cls.parser, None]), h.h_epsilon_p(), None]))
    def test_success(self):
        tree = h.h_parse(self.parser, "a", 1).ast.token_data.seq
        self.assertEqual(tree[0].token_data.uint, ord("a"))
        tree = h_parse(self.parser, "aa", 2).ast.token_data.seq
        self.assertEqual(tree[0].token_data.uint, ord("a"))
        self.assertEqual(tree[1].token_data.seq[0].token_data.uint, ord("a"))
        tree = h_parse(self.parser, "aaa", 3).ast.token_data.seq
        self.assertEqual(tree[0].token_data.uint, ord("a"))
        self.assertEqual(tree[1].token_data.seq[0].token_data.uint, ord("a"))
        self.assertEqual(tree[1].token_data.seq[1].token_data.seq[0].uint, ord("a"))
    def test_failure(self):
        pass

# ### this is just for GLR
# #class TestAmbiguous(unittest.TestCase):
# #    @classmethod
# #    def setUpClass(cls):
# #        cls.parser = h.h_indirect()
# #        d = h.h_ch("d")
# #        p = h.h_ch("+")
# #        h.h_bind_indirect(cls.parser, h.h_choice(h.h_sequence(cls.parser, p, cls.parser), d))
# #        # this is supposed to be flattened
# #    def test_success(self):
# #        self.assertEqual(h.h_parse(self.parser, "d", 1).ast.token_data.seq, ["d"])
# #        self.assertEqual(h.h_parse(self.parser, "d+d", 3).ast.token_data.seq, ["d", "+", "d"])
# #        self.assertEqual(h.h_parse(self.parser, "d+d+d", 5).ast.token_data.seq, ["d", "+", "d", "+", "d"])
# #    def test_failure(self):
# #        self.assertEqual(h.h_parse(self.parser, "d+", 2), None)

