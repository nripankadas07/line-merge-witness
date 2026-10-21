import itertools,unittest
from line_merge_witness import analyze,hunks,materialize

class MergeTests(unittest.TestCase):
    def test_disjoint_and_adjacent_edits(self):
        self.assertEqual(analyze('a\nb\nc\n','A\nb\nc\n','a\nb\nC\n')['merged_text'],'A\nb\nC\n')
        self.assertEqual(analyze('a\nb\n','A\nb\n','a\nB\n')['merged_text'],'A\nB\n')
    def test_conflict_evidence(self):
        r=analyze('a\nb\n','a\nLEFT\n','a\nRIGHT\n')
        self.assertIsNone(r['merged_text']);self.assertEqual(r['regions'][0]['base_range'],[1,2]);self.assertEqual(r['conflict_count'],1)
    def test_identical_edit_and_insertion_order(self):
        self.assertEqual(analyze('a\n','x\na\n','x\na\n')['merged_text'],'x\na\n')
        self.assertEqual(analyze('a\n','x\na\n','A\n')['merged_text'],'x\nA\n')
        self.assertFalse(analyze('','a','b')['clean'])
    def test_crlf_eof_and_deletion(self):
        self.assertEqual(analyze('a\r\nb','a\r\nb','A\r\nb')['merged_text'],'A\r\nb')
        self.assertEqual(analyze('a\nb\n','b\n','a\nb\n')['merged_text'],'b\n')
    def test_interior_insertion_is_conservative_conflict(self):
        self.assertFalse(analyze('a\nb\nc\n','a\nX\nb\nc\n','Q\nc\n')['clean'])
    def test_exhaustive_reconstruction_and_single_side_oracles(self):
        versions=[''.join(v) for n in range(4) for v in itertools.product(['a\n','b\n'],repeat=n)]
        for base in versions:
            for version in versions:
                b=base.splitlines(keepends=True);v=version.splitlines(keepends=True)
                self.assertEqual(materialize(b,0,len(b),hunks(b,v)),v)
                self.assertEqual(analyze(base,base,version)['merged_text'],version)
                self.assertEqual(analyze(base,version,base)['merged_text'],version)
                self.assertEqual(analyze(base,version,version)['merged_text'],version)
    def test_side_swap_symmetry(self):
        versions=['','a\n','b\n','a\nb\n','b\na\n']
        for base,left,right in itertools.product(versions,repeat=3):
            a=analyze(base,left,right);b=analyze(base,right,left)
            self.assertEqual(a['clean'],b['clean']);self.assertEqual(a['merged_text'],b['merged_text'])
    def test_line_limit(self):
        with self.assertRaises(ValueError):analyze('x\n'*501,'','')

if __name__=='__main__':unittest.main()
