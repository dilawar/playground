#include <cassert>
#include <iostream>

using namespace std;

inline bool
is_palindrome(const char* s, const size_t N)
{
    for (size_t i = 0; i < N / 2; i++)
        if (s[i] != s[N - i - 1])
            return false;
    return true;
}

string
longestPalindrome(const string& s)
{
    if (s.length() == 1)
        return s;

    for (size_t l = s.length(); l > 0; l--) {
        size_t num_substrings = s.length() - l + 1;
        for (size_t i = 0; i < num_substrings; i++) {
            const string a(s.rbegin() + i, s.rbegin() + i + l);
            if (is_palindrome(a.c_str(), a.length()))
                return a;
        }
    }
    return string("");
}

int
main()
{
    assert(is_palindrome("aba", 3));

    auto p = longestPalindrome("cbbd");
    cout.flush();
    assert(p == "bb");

    p = longestPalindrome("babad");
    assert(p == "aba");

    p = longestPalindrome("a");
    assert(p == "a");

    p = longestPalindrome("bb");
    assert(p == "bb");

    p = longestPalindrome("ac");
    assert(p == "c");

    p = longestPalindrome("aacabdkacaa");
    cout << p << endl;
    assert(p == "aca");

    p = longestPalindrome(
      "rgczcpratwyqxaszbuwwcadruayhasynuxnakpmsyhxzlnxmdtsqqlmwnbxvmgvllafrpmlf"
      "uqpbhjddmhmbcgmlyeypkfpreddyencsdmgxysctpubvgeedhurvizgqxclhpfrvxggroway"
      "nrtuwvvvwnqlowdihtrdzjffrgoeqivnprdnpvfjuhycpfydjcpfcnkpyujljiesmuxhtizz"
      "vwhvpqylvcirwqsmpptyhcqybstsfgjadicwzycswwmpluvzqdvnhkcofptqrzgjqtbvbdxy"
      "lrylinspncrkxclykccbwridpqckstxdjawvziucrswpsfmisqiozworibeycuarcidbljsl"
      "wbalcemgymnsxfziattdylrulwrybzztoxhevsdnvvljfzzrgcmagshucoalfiuapgzpqgjj"
      "gqsmcvtdsvehewrvtkeqwgmatqdpwlayjcxcavjmgpdyklrjcqvxjqbjucfubgmgpkfdxznk"
      "hcejscymuildfnuxwmuklntnyycdcscioimenaeohgpbcpogyifcsatfxeslstkjclauqmyw"
      "acizyapxlgtcchlxkvygzeucwalhvhbwkvbceqajstxzzppcxoanhyfkgwaelsfdeeviqogj"
      "presnoacegfeejyychabkhszcokdxpaqrprwfdahjqkfptwpeykgumyemgkccynxuvbdpjlr"
      "bgqtcqulxodurugofuwzudnhgxdrbbxtrvdnlodyhsifvyspejenpdckevzqrexplpcqtwtx"
      "limfrsjumiygqeemhihcxyngsemcolrnlyhqlbqbcestadoxtrdvcgucntjnfavylip");
    assert(p == "qgjjgq");

    return 0;
}
