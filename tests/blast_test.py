from itertools import *
import unittest
from testlib import testutil, SkipTest, PygrTestProgram
from pygr import worldbase
from pygr import sequence, cnestedlist, seqdb, blast, logger

def check_results(results, correct, formatter, delta=0.01):
    found = []
    for result in results:
        for t in result.edges():
            found.append(formatter(t))

    # order it identically
    correct.sort()
    found.sort()

    # this is to help troubleshooting the mismatches if there are any
    mismatch = [ (a, b) for a, b in zip(correct, found) if
                 testutil.approximate_cmp([a], [b], delta)]
    if mismatch:
        logger.warn('blast mismatches found')
        for m in mismatch:
            logger.warn('%s != %s' % m)

    # this is the actual test
    assert testutil.approximate_cmp(correct, found, delta) == 0

class BlastBase(unittest.TestCase):
    def setUp(self):
        if not testutil.blast_enabled():
            raise SkipTest, "no BLAST installed"
        
        hbb1_mouse = testutil.datafile('hbb1_mouse.fa')
        sp_hbb1 = testutil.datafile('sp_hbb1')

        self.dna = seqdb.SequenceFileDB(hbb1_mouse)
        self.prot = seqdb.SequenceFileDB(sp_hbb1)


class Blast_Test(BlastBase):
    def test_blastp(self):
        "Testing blastp"
        raise SkipTest

        blastmap = blast.BlastMapping(self.prot, verbose=False)
        results = blastmap[self.prot['HBB1_XENLA']]
        correct = [('HBB1_XENLA', 'MYG_ELEMA', 0.38095238095238093),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.39130434782608697),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.39130434782608697),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.39130434782608697),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.375),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.38636363636363635),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.35714285714285715),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.30434782608695654),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.30434782608695654),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.2608695652173913),
                   ('HBB1_XENLA', 'MYG_ELEMA', 0.22535211267605634),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.30985915492957744),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.29999999999999999),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ELEMA', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.21052631578947367),
                   ('HBB1_XENLA', 'HBB1_ANAMI', 0.45323741007194246),
                   ('HBB1_XENLA', 'HBB1_ONCMY', 0.39436619718309857),
                   ('HBB1_XENLA', 'HBB1_XENBO', 0.96551724137931039),
                   ('HBB1_XENLA', 'HBB1_XENTR', 0.75),
                   ('HBB1_XENLA', 'HBB1_IGUIG', 0.48951048951048953),
                   ('HBB1_XENLA', 'HBB1_VAREX', 0.5174825174825175),
                   ('HBB1_XENLA', 'HBB1_TRICR', 0.49650349650349651),
                   ('HBB1_XENLA', 'HBB1_SPHPU', 0.4825174825174825),
                   ('HBB1_XENLA', 'HBB1_RAT', 0.45833333333333331),
                   ('HBB1_XENLA', 'HBB1_TAPTE', 0.47222222222222221),
                   ('HBB1_XENLA', 'HBB1_MOUSE', 0.44444444444444442),
                   ('HBB1_XENLA', 'HBB1_PAGBO', 0.44055944055944057),
                   ('HBB1_XENLA', 'HBB0_PAGBO', 0.44055944055944057),
                   ('HBB1_XENLA', 'HBB1_CYGMA', 0.46715328467153283),
                   ('HBB1_XENLA', 'HBB1_UROHA', 0.3776223776223776),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.33333333333333331)]

        check_results([results], correct,
                      lambda t:(t[0].id, t[1].id, t[2].pIdentity()))
    def test_multiblast(self):
        "testing multi sequence blast"
        raise SkipTest

        blastmap = blast.BlastMapping(self.prot, verbose=False)
        al = cnestedlist.NLMSA('blasthits', 'memory', pairwiseMode=True,
                               bidirectional=False)
        blastmap(None, al, queryDB=self.prot) # all vs all
        al.build() # construct the alignment indexes
        results = [al[seq] for seq in self.prot.values()]
        correct = [('HBB0_PAGBO', 'MYG_ELEMA', 0.2857142857142857),
                   ('HBB0_PAGBO', 'MYG_GALCR', 0.30434782608695654),
                   ('HBB0_PAGBO', 'MYG_DIDMA', 0.2608695652173913),
                   ('HBB0_PAGBO', 'MYG_ERIEU', 0.2608695652173913),
                   ('HBB0_PAGBO', 'MYG_ESCGI', 0.33333333333333331),
                   ('HBB0_PAGBO', 'HBB1_TORMA', 0.34615384615384615),
                   ('HBB0_PAGBO', 'HBB1_ANAMI', 0.66896551724137931),
                   ('HBB0_PAGBO', 'HBB1_ONCMY', 0.55172413793103448),
                   ('HBB0_PAGBO', 'MYG_GALCR', 0.23529411764705882),
                   ('HBB0_PAGBO', 'MYG_ESCGI', 0.23728813559322035),
                   ('HBB0_PAGBO', 'MYG_DIDMA', 0.21848739495798319),
                   ('HBB0_PAGBO', 'MYG_ERIEU', 0.21008403361344538),
                   ('HBB0_PAGBO', 'MYG_ELEMA', 0.19834710743801653),
                   ('HBB0_PAGBO', 'HBB1_PAGBO', 0.69178082191780821),
                   ('HBB0_PAGBO', 'HBB1_CYGMA', 0.68493150684931503),
                   ('HBB0_PAGBO', 'HBB1_TAPTE', 0.4863013698630137),
                   ('HBB0_PAGBO', 'HBB1_VAREX', 0.49315068493150682),
                   ('HBB0_PAGBO', 'HBB1_IGUIG', 0.4863013698630137),
                   ('HBB0_PAGBO', 'HBB1_RAT', 0.4589041095890411),
                   ('HBB0_PAGBO', 'HBB1_MOUSE', 0.45205479452054792),
                   ('HBB0_PAGBO', 'HBB1_SPHPU', 0.4589041095890411),
                   ('HBB0_PAGBO', 'HBB1_XENTR', 0.4726027397260274),
                   ('HBB0_PAGBO', 'HBB1_TRICR', 0.4375),
                   ('HBB0_PAGBO', 'HBB1_XENLA', 0.44055944055944057),
                   ('HBB0_PAGBO', 'HBB1_XENBO', 0.43356643356643354),
                   ('HBB0_PAGBO', 'HBB1_UROHA', 0.4041095890410959),
                   ('HBB0_PAGBO', 'HBB1_TORMA', 0.31111111111111112),
                   ('HBB1_ANAMI', 'HBB1_TORMA', 0.36538461538461536),
                   ('HBB1_ANAMI', 'HBB0_PAGBO', 0.66896551724137931),
                   ('HBB1_ANAMI', 'HBB1_PAGBO', 0.75862068965517238),
                   ('HBB1_ANAMI', 'HBB1_CYGMA', 0.75862068965517238),
                   ('HBB1_ANAMI', 'HBB1_ONCMY', 0.59310344827586203),
                   ('HBB1_ANAMI', 'HBB1_TAPTE', 0.48965517241379308),
                   ('HBB1_ANAMI', 'HBB1_VAREX', 0.48275862068965519),
                   ('HBB1_ANAMI', 'HBB1_IGUIG', 0.47586206896551725),
                   ('HBB1_ANAMI', 'HBB1_RAT', 0.48965517241379308),
                   ('HBB1_ANAMI', 'HBB1_MOUSE', 0.45517241379310347),
                   ('HBB1_ANAMI', 'HBB1_SPHPU', 0.46206896551724136),
                   ('HBB1_ANAMI', 'HBB1_XENTR', 0.4689655172413793),
                   ('HBB1_ANAMI', 'HBB1_TRICR', 0.41258741258741261),
                   ('HBB1_ANAMI', 'HBB1_XENLA', 0.45323741007194246),
                   ('HBB1_ANAMI', 'HBB1_XENBO', 0.4460431654676259),
                   ('HBB1_ANAMI', 'HBB1_UROHA', 0.38620689655172413),
                   ('HBB1_ANAMI', 'HBB1_TORMA', 0.29213483146067415),
                   ('HBB1_CYGMA', 'MYG_ESCGI', 0.5),
                   ('HBB1_CYGMA', 'MYG_ESCGI', 0.40000000000000002),
                   ('HBB1_CYGMA', 'HBB1_TORMA', 0.36538461538461536),
                   ('HBB1_CYGMA', 'HBB1_ANAMI', 0.75862068965517238),
                   ('HBB1_CYGMA', 'HBB1_ONCMY', 0.53103448275862064),
                   ('HBB1_CYGMA', 'MYG_ESCGI', 0.24590163934426229),
                   ('HBB1_CYGMA', 'HBB0_PAGBO', 0.68493150684931503),
                   ('HBB1_CYGMA', 'HBB1_PAGBO', 0.86986301369863017),
                   ('HBB1_CYGMA', 'HBB1_TAPTE', 0.4726027397260274),
                   ('HBB1_CYGMA', 'HBB1_VAREX', 0.4863013698630137),
                   ('HBB1_CYGMA', 'HBB1_IGUIG', 0.5),
                   ('HBB1_CYGMA', 'HBB1_RAT', 0.50684931506849318),
                   ('HBB1_CYGMA', 'HBB1_MOUSE', 0.47945205479452052),
                   ('HBB1_CYGMA', 'HBB1_SPHPU', 0.47945205479452052),
                   ('HBB1_CYGMA', 'HBB1_XENTR', 0.47945205479452052),
                   ('HBB1_CYGMA', 'HBB1_TRICR', 0.45588235294117646),
                   ('HBB1_CYGMA', 'HBB1_XENLA', 0.46715328467153283),
                   ('HBB1_CYGMA', 'HBB1_XENBO', 0.45985401459854014),
                   ('HBB1_CYGMA', 'HBB1_UROHA', 0.36986301369863012),
                   ('HBB1_CYGMA', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_IGUIG', 'MYG_GALCR', 0.5),
                   ('HBB1_IGUIG', 'MYG_ESCGI', 0.41666666666666669),
                   ('HBB1_IGUIG', 'MYG_DIDMA', 0.5),
                   ('HBB1_IGUIG', 'MYG_ERIEU', 0.58333333333333337),
                   ('HBB1_IGUIG', 'HBB1_TORMA', 0.36538461538461536),
                   ('HBB1_IGUIG', 'MYG_GALCR', 0.29870129870129869),
                   ('HBB1_IGUIG', 'MYG_ESCGI', 0.29870129870129869),
                   ('HBB1_IGUIG', 'MYG_ERIEU', 0.2857142857142857),
                   ('HBB1_IGUIG', 'MYG_GALCR', 0.42857142857142855),
                   ('HBB1_IGUIG', 'MYG_ESCGI', 0.2857142857142857),
                   ('HBB1_IGUIG', 'MYG_ERIEU', 0.42857142857142855),
                   ('HBB1_IGUIG', 'HBB1_ANAMI', 0.47586206896551725),
                   ('HBB1_IGUIG', 'HBB1_ONCMY', 0.51034482758620692),
                   ('HBB1_IGUIG', 'MYG_GALCR', 0.19047619047619047),
                   ('HBB1_IGUIG', 'MYG_ESCGI', 0.21428571428571427),
                   ('HBB1_IGUIG', 'MYG_DIDMA', 0.23622047244094488),
                   ('HBB1_IGUIG', 'MYG_ERIEU', 0.19047619047619047),
                   ('HBB1_IGUIG', 'HBB0_PAGBO', 0.4863013698630137),
                   ('HBB1_IGUIG', 'HBB1_PAGBO', 0.4863013698630137),
                   ('HBB1_IGUIG', 'HBB1_CYGMA', 0.5),
                   ('HBB1_IGUIG', 'HBB1_TAPTE', 0.64383561643835618),
                   ('HBB1_IGUIG', 'HBB1_VAREX', 0.77397260273972601),
                   ('HBB1_IGUIG', 'HBB1_RAT', 0.61643835616438358),
                   ('HBB1_IGUIG', 'HBB1_MOUSE', 0.63013698630136983),
                   ('HBB1_IGUIG', 'HBB1_SPHPU', 0.71232876712328763),
                   ('HBB1_IGUIG', 'HBB1_XENTR', 0.49315068493150682),
                   ('HBB1_IGUIG', 'HBB1_TRICR', 0.47916666666666669),
                   ('HBB1_IGUIG', 'HBB1_XENLA', 0.48951048951048953),
                   ('HBB1_IGUIG', 'HBB1_XENBO', 0.4825174825174825),
                   ('HBB1_IGUIG', 'HBB1_UROHA', 0.64383561643835618),
                   ('HBB1_IGUIG', 'HBB1_TORMA', 0.37777777777777777),
                   ('HBB1_MOUSE', 'MYG_ELEMA', 0.45454545454545453),
                   ('HBB1_MOUSE', 'MYG_GALCR', 0.43478260869565216),
                   ('HBB1_MOUSE', 'MYG_ESCGI', 0.43478260869565216),
                   ('HBB1_MOUSE', 'MYG_DIDMA', 0.43478260869565216),
                   ('HBB1_MOUSE', 'MYG_ERIEU', 0.43478260869565216),
                   ('HBB1_MOUSE', 'MYG_ELEMA', 0.40000000000000002),
                   ('HBB1_MOUSE', 'HBB1_TORMA', 0.44230769230769229),
                   ('HBB1_MOUSE', 'HBB1_ANAMI', 0.45517241379310347),
                   ('HBB1_MOUSE', 'HBB1_ONCMY', 0.50344827586206897),
                   ('HBB1_MOUSE', 'MYG_GALCR', 0.25833333333333336),
                   ('HBB1_MOUSE', 'MYG_ESCGI', 0.26666666666666666),
                   ('HBB1_MOUSE', 'MYG_DIDMA', 0.27500000000000002),
                   ('HBB1_MOUSE', 'MYG_ERIEU', 0.28333333333333333),
                   ('HBB1_MOUSE', 'MYG_ELEMA', 0.2413793103448276),
                   ('HBB1_MOUSE', 'HBB0_PAGBO', 0.45205479452054792),
                   ('HBB1_MOUSE', 'HBB1_PAGBO', 0.4726027397260274),
                   ('HBB1_MOUSE', 'HBB1_CYGMA', 0.47945205479452052),
                   ('HBB1_MOUSE', 'HBB1_TAPTE', 0.76027397260273977),
                   ('HBB1_MOUSE', 'HBB1_VAREX', 0.6095890410958904),
                   ('HBB1_MOUSE', 'HBB1_IGUIG', 0.63013698630136983),
                   ('HBB1_MOUSE', 'HBB1_RAT', 0.9178082191780822),
                   ('HBB1_MOUSE', 'HBB1_SPHPU', 0.65753424657534243),
                   ('HBB1_MOUSE', 'HBB1_XENTR', 0.4589041095890411),
                   ('HBB1_MOUSE', 'HBB1_TRICR', 0.52447552447552448),
                   ('HBB1_MOUSE', 'HBB1_XENLA', 0.44444444444444442),
                   ('HBB1_MOUSE', 'HBB1_XENBO', 0.44444444444444442),
                   ('HBB1_MOUSE', 'HBB1_UROHA', 0.47945205479452052),
                   ('HBB1_MOUSE', 'HBB1_TORMA', 0.32222222222222224),
                   ('HBB1_ONCMY', 'MYG_DIDMA', 0.3888888888888889),
                   ('HBB1_ONCMY', 'MYG_ERIEU', 0.44444444444444442),
                   ('HBB1_ONCMY', 'MYG_GALCR', 0.38095238095238093),
                   ('HBB1_ONCMY', 'MYG_ESCGI', 0.38095238095238093),
                   ('HBB1_ONCMY', 'HBB1_TORMA', 0.44230769230769229),
                   ('HBB1_ONCMY', 'HBB0_PAGBO', 0.55172413793103448),
                   ('HBB1_ONCMY', 'HBB1_PAGBO', 0.56551724137931036),
                   ('HBB1_ONCMY', 'HBB1_CYGMA', 0.53103448275862064),
                   ('HBB1_ONCMY', 'HBB1_ANAMI', 0.59310344827586203),
                   ('HBB1_ONCMY', 'HBB1_TAPTE', 0.50344827586206897),
                   ('HBB1_ONCMY', 'HBB1_VAREX', 0.48965517241379308),
                   ('HBB1_ONCMY', 'HBB1_IGUIG', 0.51034482758620692),
                   ('HBB1_ONCMY', 'HBB1_RAT', 0.50344827586206897),
                   ('HBB1_ONCMY', 'HBB1_MOUSE', 0.50344827586206897),
                   ('HBB1_ONCMY', 'HBB1_SPHPU', 0.46206896551724136),
                   ('HBB1_ONCMY', 'HBB1_XENTR', 0.39310344827586208),
                   ('HBB1_ONCMY', 'HBB1_TRICR', 0.41258741258741261),
                   ('HBB1_ONCMY', 'HBB1_XENLA', 0.39436619718309857),
                   ('HBB1_ONCMY', 'HBB1_XENBO', 0.40140845070422537),
                   ('HBB1_ONCMY', 'HBB1_UROHA', 0.44827586206896552),
                   ('HBB1_ONCMY', 'HBB1_TORMA', 0.29213483146067415),
                   ('HBB1_ONCMY', 'MYG_GALCR', 0.2231404958677686),
                   ('HBB1_ONCMY', 'MYG_ESCGI', 0.23140495867768596),
                   ('HBB1_ONCMY', 'MYG_DIDMA', 0.24193548387096775),
                   ('HBB1_ONCMY', 'MYG_ERIEU', 0.20967741935483872),
                   ('HBB1_PAGBO', 'HBB1_TORMA', 0.40384615384615385),
                   ('HBB1_PAGBO', 'HBB1_ANAMI', 0.75862068965517238),
                   ('HBB1_PAGBO', 'HBB1_ONCMY', 0.56551724137931036),
                   ('HBB1_PAGBO', 'HBB0_PAGBO', 0.69178082191780821),
                   ('HBB1_PAGBO', 'HBB1_CYGMA', 0.86986301369863017),
                   ('HBB1_PAGBO', 'HBB1_TAPTE', 0.46575342465753422),
                   ('HBB1_PAGBO', 'HBB1_VAREX', 0.4726027397260274),
                   ('HBB1_PAGBO', 'HBB1_IGUIG', 0.4863013698630137),
                   ('HBB1_PAGBO', 'HBB1_RAT', 0.4863013698630137),
                   ('HBB1_PAGBO', 'HBB1_MOUSE', 0.4726027397260274),
                   ('HBB1_PAGBO', 'HBB1_SPHPU', 0.4726027397260274),
                   ('HBB1_PAGBO', 'HBB1_XENTR', 0.47945205479452052),
                   ('HBB1_PAGBO', 'HBB1_TRICR', 0.4375),
                   ('HBB1_PAGBO', 'HBB1_XENLA', 0.44055944055944057),
                   ('HBB1_PAGBO', 'HBB1_XENBO', 0.43356643356643354),
                   ('HBB1_PAGBO', 'HBB1_UROHA', 0.35616438356164382),
                   ('HBB1_PAGBO', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_RAT', 'MYG_DIDMA', 0.47368421052631576),
                   ('HBB1_RAT', 'MYG_ERIEU', 0.47368421052631576),
                   ('HBB1_RAT', 'MYG_ELEMA', 0.45454545454545453),
                   ('HBB1_RAT', 'MYG_GALCR', 0.43478260869565216),
                   ('HBB1_RAT', 'MYG_ESCGI', 0.43478260869565216),
                   ('HBB1_RAT', 'MYG_ELEMA', 0.5),
                   ('HBB1_RAT', 'HBB1_TORMA', 0.42307692307692307),
                   ('HBB1_RAT', 'HBB1_ANAMI', 0.48965517241379308),
                   ('HBB1_RAT', 'HBB1_ONCMY', 0.50344827586206897),
                   ('HBB1_RAT', 'MYG_GALCR', 0.25),
                   ('HBB1_RAT', 'MYG_ESCGI', 0.25833333333333336),
                   ('HBB1_RAT', 'MYG_DIDMA', 0.27419354838709675),
                   ('HBB1_RAT', 'MYG_ERIEU', 0.27419354838709675),
                   ('HBB1_RAT', 'MYG_ELEMA', 0.24786324786324787),
                   ('HBB1_RAT', 'HBB0_PAGBO', 0.4589041095890411),
                   ('HBB1_RAT', 'HBB1_PAGBO', 0.4863013698630137),
                   ('HBB1_RAT', 'HBB1_CYGMA', 0.50684931506849318),
                   ('HBB1_RAT', 'HBB1_TAPTE', 0.76712328767123283),
                   ('HBB1_RAT', 'HBB1_VAREX', 0.62328767123287676),
                   ('HBB1_RAT', 'HBB1_IGUIG', 0.61643835616438358),
                   ('HBB1_RAT', 'HBB1_MOUSE', 0.9178082191780822),
                   ('HBB1_RAT', 'HBB1_SPHPU', 0.66438356164383561),
                   ('HBB1_RAT', 'HBB1_XENTR', 0.45205479452054792),
                   ('HBB1_RAT', 'HBB1_TRICR', 0.53146853146853146),
                   ('HBB1_RAT', 'HBB1_XENLA', 0.45833333333333331),
                   ('HBB1_RAT', 'HBB1_XENBO', 0.45833333333333331),
                   ('HBB1_RAT', 'HBB1_UROHA', 0.5),
                   ('HBB1_RAT', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_SPHPU', 'HBB1_TORMA', 0.40384615384615385),
                   ('HBB1_SPHPU', 'HBB1_ANAMI', 0.46206896551724136),
                   ('HBB1_SPHPU', 'HBB1_ONCMY', 0.46206896551724136),
                   ('HBB1_SPHPU', 'HBB0_PAGBO', 0.4589041095890411),
                   ('HBB1_SPHPU', 'HBB1_PAGBO', 0.4726027397260274),
                   ('HBB1_SPHPU', 'HBB1_CYGMA', 0.47945205479452052),
                   ('HBB1_SPHPU', 'HBB1_TAPTE', 0.63698630136986301),
                   ('HBB1_SPHPU', 'HBB1_VAREX', 0.69178082191780821),
                   ('HBB1_SPHPU', 'HBB1_IGUIG', 0.71232876712328763),
                   ('HBB1_SPHPU', 'HBB1_RAT', 0.66438356164383561),
                   ('HBB1_SPHPU', 'HBB1_MOUSE', 0.65753424657534243),
                   ('HBB1_SPHPU', 'HBB1_XENTR', 0.4726027397260274),
                   ('HBB1_SPHPU', 'HBB1_TRICR', 0.47916666666666669),
                   ('HBB1_SPHPU', 'HBB1_XENLA', 0.4825174825174825),
                   ('HBB1_SPHPU', 'HBB1_XENBO', 0.48951048951048953),
                   ('HBB1_SPHPU', 'HBB1_UROHA', 0.54109589041095896),
                   ('HBB1_SPHPU', 'HBB1_TORMA', 0.3888888888888889),
                   ('HBB1_TAPTE', 'MYG_GALCR', 0.39130434782608697),
                   ('HBB1_TAPTE', 'MYG_ESCGI', 0.39130434782608697),
                   ('HBB1_TAPTE', 'MYG_DIDMA', 0.39130434782608697),
                   ('HBB1_TAPTE', 'MYG_ERIEU', 0.39130434782608697),
                   ('HBB1_TAPTE', 'HBB1_TORMA', 0.38461538461538464),
                   ('HBB1_TAPTE', 'MYG_ESCGI', 0.36170212765957449),
                   ('HBB1_TAPTE', 'MYG_ESCGI', 0.5),
                   ('HBB1_TAPTE', 'MYG_ESCGI', 0.5714285714285714),
                   ('HBB1_TAPTE', 'HBB1_ANAMI', 0.48965517241379308),
                   ('HBB1_TAPTE', 'HBB1_ONCMY', 0.50344827586206897),
                   ('HBB1_TAPTE', 'MYG_GALCR', 0.25),
                   ('HBB1_TAPTE', 'MYG_ESCGI', 0.22033898305084745),
                   ('HBB1_TAPTE', 'MYG_DIDMA', 0.24166666666666667),
                   ('HBB1_TAPTE', 'MYG_ERIEU', 0.25),
                   ('HBB1_TAPTE', 'HBB0_PAGBO', 0.4863013698630137),
                   ('HBB1_TAPTE', 'HBB1_PAGBO', 0.46575342465753422),
                   ('HBB1_TAPTE', 'HBB1_CYGMA', 0.4726027397260274),
                   ('HBB1_TAPTE', 'HBB1_VAREX', 0.62328767123287676),
                   ('HBB1_TAPTE', 'HBB1_IGUIG', 0.64383561643835618),
                   ('HBB1_TAPTE', 'HBB1_RAT', 0.76712328767123283),
                   ('HBB1_TAPTE', 'HBB1_MOUSE', 0.76027397260273977),
                   ('HBB1_TAPTE', 'HBB1_SPHPU', 0.63698630136986301),
                   ('HBB1_TAPTE', 'HBB1_XENTR', 0.45205479452054792),
                   ('HBB1_TAPTE', 'HBB1_TRICR', 0.48951048951048953),
                   ('HBB1_TAPTE', 'HBB1_XENLA', 0.47222222222222221),
                   ('HBB1_TAPTE', 'HBB1_XENBO', 0.4861111111111111),
                   ('HBB1_TAPTE', 'HBB1_UROHA', 0.51369863013698636),
                   ('HBB1_TAPTE', 'HBB1_TORMA', 0.34444444444444444),
                   ('HBB1_TORMA', 'MYG_ESCGI', 0.4375),
                   ('HBB1_TORMA', 'HBB1_XENTR', 0.41304347826086957),
                   ('HBB1_TORMA', 'HBB1_XENLA', 0.38636363636363635),
                   ('HBB1_TORMA', 'HBB1_XENBO', 0.40909090909090912),
                   ('HBB1_TORMA', 'HBB1_VAREX', 0.34000000000000002),
                   ('HBB1_TORMA', 'HBB0_PAGBO', 0.34615384615384615),
                   ('HBB1_TORMA', 'HBB1_PAGBO', 0.40384615384615385),
                   ('HBB1_TORMA', 'HBB1_CYGMA', 0.36538461538461536),
                   ('HBB1_TORMA', 'HBB1_ANAMI', 0.36538461538461536),
                   ('HBB1_TORMA', 'HBB1_ONCMY', 0.44230769230769229),
                   ('HBB1_TORMA', 'HBB1_TAPTE', 0.38461538461538464),
                   ('HBB1_TORMA', 'HBB1_IGUIG', 0.36538461538461536),
                   ('HBB1_TORMA', 'HBB1_RAT', 0.42307692307692307),
                   ('HBB1_TORMA', 'HBB1_MOUSE', 0.44230769230769229),
                   ('HBB1_TORMA', 'HBB1_SPHPU', 0.40384615384615385),
                   ('HBB1_TORMA', 'HBB1_TRICR', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_UROHA', 0.36538461538461536),
                   ('HBB1_TORMA', 'HBB1_XENTR', 0.2857142857142857),
                   ('HBB1_TORMA', 'HBB1_XENLA', 0.35714285714285715),
                   ('HBB1_TORMA', 'HBB1_XENBO', 0.35714285714285715),
                   ('HBB1_TORMA', 'MYG_ESCGI', 0.20000000000000001),
                   ('HBB1_TORMA', 'HBB1_ANAMI', 0.29213483146067415),
                   ('HBB1_TORMA', 'HBB1_ONCMY', 0.29213483146067415),
                   ('HBB1_TORMA', 'MYG_ESCGI', 0.17241379310344829),
                   ('HBB1_TORMA', 'HBB0_PAGBO', 0.31111111111111112),
                   ('HBB1_TORMA', 'HBB1_PAGBO', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_CYGMA', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_TAPTE', 0.34444444444444444),
                   ('HBB1_TORMA', 'HBB1_VAREX', 0.38043478260869568),
                   ('HBB1_TORMA', 'HBB1_IGUIG', 0.37777777777777777),
                   ('HBB1_TORMA', 'HBB1_RAT', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_MOUSE', 0.32222222222222224),
                   ('HBB1_TORMA', 'HBB1_SPHPU', 0.3888888888888889),
                   ('HBB1_TORMA', 'HBB1_XENTR', 0.32098765432098764),
                   ('HBB1_TORMA', 'HBB1_TRICR', 0.32222222222222224),
                   ('HBB1_TORMA', 'HBB1_XENLA', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_XENBO', 0.33333333333333331),
                   ('HBB1_TORMA', 'HBB1_UROHA', 0.26666666666666666),
                   ('HBB1_TRICR', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_TRICR', 'HBB1_ANAMI', 0.41258741258741261),
                   ('HBB1_TRICR', 'HBB1_ONCMY', 0.41258741258741261),
                   ('HBB1_TRICR', 'HBB0_PAGBO', 0.4375),
                   ('HBB1_TRICR', 'HBB1_PAGBO', 0.4375),
                   ('HBB1_TRICR', 'HBB1_CYGMA', 0.45588235294117646),
                   ('HBB1_TRICR', 'HBB1_TAPTE', 0.48951048951048953),
                   ('HBB1_TRICR', 'HBB1_VAREX', 0.4513888888888889),
                   ('HBB1_TRICR', 'HBB1_IGUIG', 0.47916666666666669),
                   ('HBB1_TRICR', 'HBB1_RAT', 0.53146853146853146),
                   ('HBB1_TRICR', 'HBB1_MOUSE', 0.52447552447552448),
                   ('HBB1_TRICR', 'HBB1_SPHPU', 0.47916666666666669),
                   ('HBB1_TRICR', 'HBB1_XENTR', 0.49650349650349651),
                   ('HBB1_TRICR', 'HBB1_XENLA', 0.49650349650349651),
                   ('HBB1_TRICR', 'HBB1_XENBO', 0.48951048951048953),
                   ('HBB1_TRICR', 'HBB1_UROHA', 0.3611111111111111),
                   ('HBB1_TRICR', 'HBB1_TORMA', 0.32222222222222224),
                   ('HBB1_UROHA', 'MYG_ERIEU', 0.5),
                   ('HBB1_UROHA', 'HBB1_TORMA', 0.36538461538461536),
                   ('HBB1_UROHA', 'MYG_ERIEU', 0.24675324675324675),
                   ('HBB1_UROHA', 'MYG_ERIEU', 0.42857142857142855),
                   ('HBB1_UROHA', 'HBB1_XENTR', 0.42307692307692307),
                   ('HBB1_UROHA', 'HBB1_TORMA', 0.28333333333333333),
                   ('HBB1_UROHA', 'HBB1_XENLA', 0.41739130434782606),
                   ('HBB1_UROHA', 'HBB1_XENBO', 0.42608695652173911),
                   ('HBB1_UROHA', 'HBB1_ANAMI', 0.42857142857142855),
                   ('HBB1_UROHA', 'HBB1_ONCMY', 0.50420168067226889),
                   ('HBB1_UROHA', 'HBB1_TRICR', 0.39316239316239315),
                   ('HBB1_UROHA', 'MYG_ERIEU', 0.3125),
                   ('HBB1_UROHA', 'HBB0_PAGBO', 0.4041095890410959),
                   ('HBB1_UROHA', 'HBB1_PAGBO', 0.35616438356164382),
                   ('HBB1_UROHA', 'HBB1_CYGMA', 0.36986301369863012),
                   ('HBB1_UROHA', 'HBB1_TAPTE', 0.51369863013698636),
                   ('HBB1_UROHA', 'HBB1_VAREX', 0.59589041095890416),
                   ('HBB1_UROHA', 'HBB1_IGUIG', 0.64383561643835618),
                   ('HBB1_UROHA', 'HBB1_RAT', 0.5),
                   ('HBB1_UROHA', 'HBB1_MOUSE', 0.47945205479452052),
                   ('HBB1_UROHA', 'HBB1_SPHPU', 0.54109589041095896),
                   ('HBB1_VAREX', 'MYG_ESCGI', 0.41666666666666669),
                   ('HBB1_VAREX', 'MYG_GALCR', 0.42105263157894735),
                   ('HBB1_VAREX', 'MYG_DIDMA', 0.36842105263157893),
                   ('HBB1_VAREX', 'MYG_ERIEU', 0.36842105263157893),
                   ('HBB1_VAREX', 'HBB1_TORMA', 0.34000000000000002),
                   ('HBB1_VAREX', 'HBB1_ANAMI', 0.48275862068965519),
                   ('HBB1_VAREX', 'HBB1_ONCMY', 0.48965517241379308),
                   ('HBB1_VAREX', 'MYG_GALCR', 0.22500000000000001),
                   ('HBB1_VAREX', 'MYG_ESCGI', 0.23622047244094488),
                   ('HBB1_VAREX', 'MYG_DIDMA', 0.24166666666666667),
                   ('HBB1_VAREX', 'MYG_ERIEU', 0.24166666666666667),
                   ('HBB1_VAREX', 'HBB0_PAGBO', 0.49315068493150682),
                   ('HBB1_VAREX', 'HBB1_PAGBO', 0.4726027397260274),
                   ('HBB1_VAREX', 'HBB1_CYGMA', 0.4863013698630137),
                   ('HBB1_VAREX', 'HBB1_TAPTE', 0.62328767123287676),
                   ('HBB1_VAREX', 'HBB1_IGUIG', 0.77397260273972601),
                   ('HBB1_VAREX', 'HBB1_RAT', 0.62328767123287676),
                   ('HBB1_VAREX', 'HBB1_MOUSE', 0.6095890410958904),
                   ('HBB1_VAREX', 'HBB1_SPHPU', 0.69178082191780821),
                   ('HBB1_VAREX', 'HBB1_XENTR', 0.4726027397260274),
                   ('HBB1_VAREX', 'HBB1_TRICR', 0.4513888888888889),
                   ('HBB1_VAREX', 'HBB1_XENLA', 0.5174825174825175),
                   ('HBB1_VAREX', 'HBB1_XENBO', 0.51048951048951052),
                   ('HBB1_VAREX', 'HBB1_UROHA', 0.59589041095890416),
                   ('HBB1_VAREX', 'HBB1_TORMA', 0.38043478260869568),
                   ('HBB1_XENBO', 'MYG_ELEMA', 0.42857142857142855),
                   ('HBB1_XENBO', 'MYG_GALCR', 0.43478260869565216),
                   ('HBB1_XENBO', 'MYG_DIDMA', 0.43478260869565216),
                   ('HBB1_XENBO', 'MYG_ERIEU', 0.43478260869565216),
                   ('HBB1_XENBO', 'HBB1_TORMA', 0.40909090909090912),
                   ('HBB1_XENBO', 'HBB1_TORMA', 0.35714285714285715),
                   ('HBB1_XENBO', 'MYG_GALCR', 0.28985507246376813),
                   ('HBB1_XENBO', 'MYG_DIDMA', 0.28985507246376813),
                   ('HBB1_XENBO', 'MYG_ELEMA', 0.22535211267605634),
                   ('HBB1_XENBO', 'MYG_ERIEU', 0.29577464788732394),
                   ('HBB1_XENBO', 'MYG_GALCR', 0.33333333333333331),
                   ('HBB1_XENBO', 'MYG_DIDMA', 0.33333333333333331),
                   ('HBB1_XENBO', 'MYG_ERIEU', 0.29999999999999999),
                   ('HBB1_XENBO', 'MYG_ELEMA', 0.33333333333333331),
                   ('HBB1_XENBO', 'HBB1_ANAMI', 0.4460431654676259),
                   ('HBB1_XENBO', 'HBB1_ONCMY', 0.40140845070422537),
                   ('HBB1_XENBO', 'HBB0_PAGBO', 0.43356643356643354),
                   ('HBB1_XENBO', 'HBB1_PAGBO', 0.43356643356643354),
                   ('HBB1_XENBO', 'HBB1_CYGMA', 0.45985401459854014),
                   ('HBB1_XENBO', 'HBB1_TAPTE', 0.4861111111111111),
                   ('HBB1_XENBO', 'HBB1_VAREX', 0.51048951048951052),
                   ('HBB1_XENBO', 'HBB1_IGUIG', 0.4825174825174825),
                   ('HBB1_XENBO', 'HBB1_RAT', 0.45833333333333331),
                   ('HBB1_XENBO', 'HBB1_MOUSE', 0.44444444444444442),
                   ('HBB1_XENBO', 'HBB1_SPHPU', 0.48951048951048953),
                   ('HBB1_XENBO', 'HBB1_XENTR', 0.76388888888888884),
                   ('HBB1_XENBO', 'HBB1_TRICR', 0.48951048951048953),
                   ('HBB1_XENBO', 'HBB1_XENLA', 0.96551724137931039),
                   ('HBB1_XENBO', 'HBB1_UROHA', 0.38461538461538464),
                   ('HBB1_XENBO', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ELEMA', 0.38095238095238093),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.39130434782608697),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.375),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.39130434782608697),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.39130434782608697),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.38636363636363635),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.35714285714285715),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.30434782608695654),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.2608695652173913),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.30434782608695654),
                   ('HBB1_XENLA', 'MYG_ELEMA', 0.22535211267605634),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.30985915492957744),
                   ('HBB1_XENLA', 'MYG_GALCR', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_DIDMA', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ERIEU', 0.29999999999999999),
                   ('HBB1_XENLA', 'MYG_ELEMA', 0.33333333333333331),
                   ('HBB1_XENLA', 'MYG_ESCGI', 0.21052631578947367),
                   ('HBB1_XENLA', 'HBB1_ANAMI', 0.45323741007194246),
                   ('HBB1_XENLA', 'HBB1_ONCMY', 0.39436619718309857),
                   ('HBB1_XENLA', 'HBB0_PAGBO', 0.44055944055944057),
                   ('HBB1_XENLA', 'HBB1_PAGBO', 0.44055944055944057),
                   ('HBB1_XENLA', 'HBB1_CYGMA', 0.46715328467153283),
                   ('HBB1_XENLA', 'HBB1_TAPTE', 0.47222222222222221),
                   ('HBB1_XENLA', 'HBB1_VAREX', 0.5174825174825175),
                   ('HBB1_XENLA', 'HBB1_IGUIG', 0.48951048951048953),
                   ('HBB1_XENLA', 'HBB1_RAT', 0.45833333333333331),
                   ('HBB1_XENLA', 'HBB1_MOUSE', 0.44444444444444442),
                   ('HBB1_XENLA', 'HBB1_SPHPU', 0.4825174825174825),
                   ('HBB1_XENLA', 'HBB1_XENTR', 0.75),
                   ('HBB1_XENLA', 'HBB1_TRICR', 0.49650349650349651),
                   ('HBB1_XENLA', 'HBB1_XENBO', 0.96551724137931039),
                   ('HBB1_XENLA', 'HBB1_UROHA', 0.3776223776223776),
                   ('HBB1_XENLA', 'HBB1_TORMA', 0.33333333333333331),
                   ('HBB1_XENTR', 'MYG_GALCR', 0.36363636363636365),
                   ('HBB1_XENTR', 'MYG_ESCGI', 0.36363636363636365),
                   ('HBB1_XENTR', 'MYG_DIDMA', 0.36363636363636365),
                   ('HBB1_XENTR', 'MYG_ERIEU', 0.36363636363636365),
                   ('HBB1_XENTR', 'HBB1_TORMA', 0.41304347826086957),
                   ('HBB1_XENTR', 'HBB1_TORMA', 0.2857142857142857),
                   ('HBB1_XENTR', 'MYG_GALCR', 0.2318840579710145),
                   ('HBB1_XENTR', 'MYG_ESCGI', 0.21739130434782608),
                   ('HBB1_XENTR', 'MYG_DIDMA', 0.2318840579710145),
                   ('HBB1_XENTR', 'MYG_ERIEU', 0.23943661971830985),
                   ('HBB1_XENTR', 'MYG_GALCR', 0.30769230769230771),
                   ('HBB1_XENTR', 'MYG_ESCGI', 0.26923076923076922),
                   ('HBB1_XENTR', 'MYG_DIDMA', 0.30769230769230771),
                   ('HBB1_XENTR', 'MYG_ERIEU', 0.25),
                   ('HBB1_XENTR', 'MYG_ESCGI', 0.5),
                   ('HBB1_XENTR', 'HBB1_ANAMI', 0.4689655172413793),
                   ('HBB1_XENTR', 'HBB1_ONCMY', 0.39310344827586208),
                   ('HBB1_XENTR', 'MYG_GALCR', 0.23999999999999999),
                   ('HBB1_XENTR', 'MYG_DIDMA', 0.28000000000000003),
                   ('HBB1_XENTR', 'MYG_ERIEU', 0.23999999999999999),
                   ('HBB1_XENTR', 'HBB0_PAGBO', 0.4726027397260274),
                   ('HBB1_XENTR', 'HBB1_PAGBO', 0.47945205479452052),
                   ('HBB1_XENTR', 'HBB1_CYGMA', 0.47945205479452052),
                   ('HBB1_XENTR', 'HBB1_TAPTE', 0.45205479452054792),
                   ('HBB1_XENTR', 'HBB1_VAREX', 0.4726027397260274),
                   ('HBB1_XENTR', 'HBB1_IGUIG', 0.49315068493150682),
                   ('HBB1_XENTR', 'HBB1_RAT', 0.45205479452054792),
                   ('HBB1_XENTR', 'HBB1_MOUSE', 0.4589041095890411),
                   ('HBB1_XENTR', 'HBB1_SPHPU', 0.4726027397260274),
                   ('HBB1_XENTR', 'HBB1_TRICR', 0.49650349650349651),
                   ('HBB1_XENTR', 'HBB1_XENLA', 0.75),
                   ('HBB1_XENTR', 'HBB1_XENBO', 0.76388888888888884),
                   ('HBB1_XENTR', 'HBB1_UROHA', 0.35616438356164382),
                   ('HBB1_XENTR', 'HBB1_TORMA', 0.32098765432098764),
                   ('MYG_DIDMA', 'HBB1_IGUIG', 0.5),
                   ('MYG_DIDMA', 'HBB1_ONCMY', 0.3888888888888889),
                   ('MYG_DIDMA', 'HBB1_RAT', 0.47368421052631576),
                   ('MYG_DIDMA', 'HBB1_XENTR', 0.36363636363636365),
                   ('MYG_DIDMA', 'HBB1_XENLA', 0.39130434782608697),
                   ('MYG_DIDMA', 'HBB1_XENBO', 0.43478260869565216),
                   ('MYG_DIDMA', 'HBB1_TAPTE', 0.39130434782608697),
                   ('MYG_DIDMA', 'HBB1_VAREX', 0.36842105263157893),
                   ('MYG_DIDMA', 'HBB1_MOUSE', 0.43478260869565216),
                   ('MYG_DIDMA', 'HBB0_PAGBO', 0.2608695652173913),
                   ('MYG_DIDMA', 'HBB1_XENTR', 0.2318840579710145),
                   ('MYG_DIDMA', 'HBB1_XENLA', 0.30434782608695654),
                   ('MYG_DIDMA', 'HBB1_XENBO', 0.28985507246376813),
                   ('MYG_DIDMA', 'HBB1_XENLA', 0.33333333333333331),
                   ('MYG_DIDMA', 'HBB1_XENBO', 0.33333333333333331),
                   ('MYG_DIDMA', 'HBB1_XENTR', 0.30769230769230771),
                   ('MYG_DIDMA', 'HBB0_PAGBO', 0.21848739495798319),
                   ('MYG_DIDMA', 'HBB1_ONCMY', 0.24193548387096775),
                   ('MYG_DIDMA', 'HBB1_TAPTE', 0.24166666666666667),
                   ('MYG_DIDMA', 'HBB1_VAREX', 0.24166666666666667),
                   ('MYG_DIDMA', 'HBB1_IGUIG', 0.23622047244094488),
                   ('MYG_DIDMA', 'HBB1_RAT', 0.27419354838709675),
                   ('MYG_DIDMA', 'HBB1_MOUSE', 0.27500000000000002),
                   ('MYG_DIDMA', 'HBB1_XENTR', 0.28000000000000003),
                   ('MYG_DIDMA', 'MYG_GALCR', 0.83006535947712423),
                   ('MYG_DIDMA', 'MYG_ESCGI', 0.83552631578947367),
                   ('MYG_DIDMA', 'MYG_ERIEU', 0.87581699346405228),
                   ('MYG_DIDMA', 'MYG_ELEMA', 0.81045751633986929),
                   ('MYG_ELEMA', 'HBB1_XENLA', 0.38095238095238093),
                   ('MYG_ELEMA', 'HBB1_XENBO', 0.42857142857142855),
                   ('MYG_ELEMA', 'HBB0_PAGBO', 0.2857142857142857),
                   ('MYG_ELEMA', 'HBB1_RAT', 0.45454545454545453),
                   ('MYG_ELEMA', 'HBB1_MOUSE', 0.45454545454545453),
                   ('MYG_ELEMA', 'HBB1_RAT', 0.5),
                   ('MYG_ELEMA', 'HBB1_MOUSE', 0.40000000000000002),
                   ('MYG_ELEMA', 'HBB1_XENLA', 0.22535211267605634),
                   ('MYG_ELEMA', 'HBB1_XENBO', 0.22535211267605634),
                   ('MYG_ELEMA', 'HBB1_XENLA', 0.33333333333333331),
                   ('MYG_ELEMA', 'HBB1_XENBO', 0.33333333333333331),
                   ('MYG_ELEMA', 'HBB0_PAGBO', 0.19834710743801653),
                   ('MYG_ELEMA', 'HBB1_RAT', 0.24786324786324787),
                   ('MYG_ELEMA', 'HBB1_MOUSE', 0.2413793103448276),
                   ('MYG_ELEMA', 'MYG_GALCR', 0.84313725490196079),
                   ('MYG_ELEMA', 'MYG_ESCGI', 0.83552631578947367),
                   ('MYG_ELEMA', 'MYG_DIDMA', 0.81045751633986929),
                   ('MYG_ELEMA', 'MYG_ERIEU', 0.82352941176470584),
                   ('MYG_ERIEU', 'HBB1_IGUIG', 0.58333333333333337),
                   ('MYG_ERIEU', 'HBB1_UROHA', 0.5),
                   ('MYG_ERIEU', 'HBB1_ONCMY', 0.44444444444444442),
                   ('MYG_ERIEU', 'HBB1_RAT', 0.47368421052631576),
                   ('MYG_ERIEU', 'HBB1_XENTR', 0.36363636363636365),
                   ('MYG_ERIEU', 'HBB1_XENLA', 0.39130434782608697),
                   ('MYG_ERIEU', 'HBB1_XENBO', 0.43478260869565216),
                   ('MYG_ERIEU', 'HBB1_TAPTE', 0.39130434782608697),
                   ('MYG_ERIEU', 'HBB1_VAREX', 0.36842105263157893),
                   ('MYG_ERIEU', 'HBB1_MOUSE', 0.43478260869565216),
                   ('MYG_ERIEU', 'HBB0_PAGBO', 0.2608695652173913),
                   ('MYG_ERIEU', 'HBB1_IGUIG', 0.2857142857142857),
                   ('MYG_ERIEU', 'HBB1_XENTR', 0.23943661971830985),
                   ('MYG_ERIEU', 'HBB1_XENLA', 0.30985915492957744),
                   ('MYG_ERIEU', 'HBB1_XENBO', 0.29577464788732394),
                   ('MYG_ERIEU', 'HBB1_UROHA', 0.24675324675324675),
                   ('MYG_ERIEU', 'HBB1_IGUIG', 0.42857142857142855),
                   ('MYG_ERIEU', 'HBB1_UROHA', 0.42857142857142855),
                   ('MYG_ERIEU', 'HBB1_XENLA', 0.29999999999999999),
                   ('MYG_ERIEU', 'HBB1_XENBO', 0.29999999999999999),
                   ('MYG_ERIEU', 'HBB1_XENTR', 0.25),
                   ('MYG_ERIEU', 'HBB1_UROHA', 0.3125),
                   ('MYG_ERIEU', 'HBB0_PAGBO', 0.21008403361344538),
                   ('MYG_ERIEU', 'HBB1_ONCMY', 0.20967741935483872),
                   ('MYG_ERIEU', 'HBB1_TAPTE', 0.25),
                   ('MYG_ERIEU', 'HBB1_VAREX', 0.24166666666666667),
                   ('MYG_ERIEU', 'HBB1_IGUIG', 0.19047619047619047),
                   ('MYG_ERIEU', 'HBB1_RAT', 0.27419354838709675),
                   ('MYG_ERIEU', 'HBB1_MOUSE', 0.28333333333333333),
                   ('MYG_ERIEU', 'HBB1_XENTR', 0.23999999999999999),
                   ('MYG_ERIEU', 'MYG_GALCR', 0.85620915032679734),
                   ('MYG_ERIEU', 'MYG_ESCGI', 0.83552631578947367),
                   ('MYG_ERIEU', 'MYG_DIDMA', 0.87581699346405228),
                   ('MYG_ERIEU', 'MYG_ELEMA', 0.82352941176470584),
                   ('MYG_ESCGI', 'HBB1_VAREX', 0.41666666666666669),
                   ('MYG_ESCGI', 'HBB1_IGUIG', 0.41666666666666669),
                   ('MYG_ESCGI', 'HBB1_TORMA', 0.4375),
                   ('MYG_ESCGI', 'HBB1_CYGMA', 0.5),
                   ('MYG_ESCGI', 'HBB1_ONCMY', 0.38095238095238093),
                   ('MYG_ESCGI', 'HBB1_XENTR', 0.36363636363636365),
                   ('MYG_ESCGI', 'HBB1_XENLA', 0.375),
                   ('MYG_ESCGI', 'HBB1_CYGMA', 0.40000000000000002),
                   ('MYG_ESCGI', 'HBB1_TAPTE', 0.39130434782608697),
                   ('MYG_ESCGI', 'HBB1_RAT', 0.43478260869565216),
                   ('MYG_ESCGI', 'HBB1_MOUSE', 0.43478260869565216),
                   ('MYG_ESCGI', 'HBB0_PAGBO', 0.33333333333333331),
                   ('MYG_ESCGI', 'HBB1_TAPTE', 0.36170212765957449),
                   ('MYG_ESCGI', 'HBB1_TAPTE', 0.5),
                   ('MYG_ESCGI', 'HBB1_TORMA', 0.20000000000000001),
                   ('MYG_ESCGI', 'HBB1_TAPTE', 0.5714285714285714),
                   ('MYG_ESCGI', 'HBB1_XENTR', 0.21739130434782608),
                   ('MYG_ESCGI', 'HBB1_XENLA', 0.2608695652173913),
                   ('MYG_ESCGI', 'HBB1_IGUIG', 0.29870129870129869),
                   ('MYG_ESCGI', 'HBB1_IGUIG', 0.2857142857142857),
                   ('MYG_ESCGI', 'HBB1_XENLA', 0.33333333333333331),
                   ('MYG_ESCGI', 'HBB1_XENTR', 0.26923076923076922),
                   ('MYG_ESCGI', 'HBB1_XENLA', 0.21052631578947367),
                   ('MYG_ESCGI', 'HBB1_XENTR', 0.5),
                   ('MYG_ESCGI', 'HBB0_PAGBO', 0.23728813559322035),
                   ('MYG_ESCGI', 'HBB1_CYGMA', 0.24590163934426229),
                   ('MYG_ESCGI', 'HBB1_ONCMY', 0.23140495867768596),
                   ('MYG_ESCGI', 'HBB1_TAPTE', 0.22033898305084745),
                   ('MYG_ESCGI', 'HBB1_VAREX', 0.23622047244094488),
                   ('MYG_ESCGI', 'HBB1_IGUIG', 0.21428571428571427),
                   ('MYG_ESCGI', 'HBB1_RAT', 0.25833333333333336),
                   ('MYG_ESCGI', 'HBB1_MOUSE', 0.26666666666666666),
                   ('MYG_ESCGI', 'HBB1_TORMA', 0.17241379310344829),
                   ('MYG_ESCGI', 'MYG_GALCR', 0.84210526315789469),
                   ('MYG_ESCGI', 'MYG_DIDMA', 0.83552631578947367),
                   ('MYG_ESCGI', 'MYG_ERIEU', 0.83552631578947367),
                   ('MYG_ESCGI', 'MYG_ELEMA', 0.83552631578947367),
                   ('MYG_GALCR', 'HBB1_IGUIG', 0.5),
                   ('MYG_GALCR', 'HBB1_ONCMY', 0.38095238095238093),
                   ('MYG_GALCR', 'HBB1_XENTR', 0.36363636363636365),
                   ('MYG_GALCR', 'HBB1_XENLA', 0.39130434782608697),
                   ('MYG_GALCR', 'HBB1_XENBO', 0.43478260869565216),
                   ('MYG_GALCR', 'HBB1_TAPTE', 0.39130434782608697),
                   ('MYG_GALCR', 'HBB1_VAREX', 0.42105263157894735),
                   ('MYG_GALCR', 'HBB1_RAT', 0.43478260869565216),
                   ('MYG_GALCR', 'HBB1_MOUSE', 0.43478260869565216),
                   ('MYG_GALCR', 'HBB0_PAGBO', 0.30434782608695654),
                   ('MYG_GALCR', 'HBB1_XENTR', 0.2318840579710145),
                   ('MYG_GALCR', 'HBB1_XENLA', 0.30434782608695654),
                   ('MYG_GALCR', 'HBB1_XENBO', 0.28985507246376813),
                   ('MYG_GALCR', 'HBB1_IGUIG', 0.29870129870129869),
                   ('MYG_GALCR', 'HBB1_IGUIG', 0.42857142857142855),
                   ('MYG_GALCR', 'HBB1_XENLA', 0.33333333333333331),
                   ('MYG_GALCR', 'HBB1_XENBO', 0.33333333333333331),
                   ('MYG_GALCR', 'HBB1_XENTR', 0.30769230769230771),
                   ('MYG_GALCR', 'HBB0_PAGBO', 0.23529411764705882),
                   ('MYG_GALCR', 'HBB1_ONCMY', 0.2231404958677686),
                   ('MYG_GALCR', 'HBB1_TAPTE', 0.25),
                   ('MYG_GALCR', 'HBB1_VAREX', 0.22500000000000001),
                   ('MYG_GALCR', 'HBB1_IGUIG', 0.19047619047619047),
                   ('MYG_GALCR', 'HBB1_RAT', 0.25),
                   ('MYG_GALCR', 'HBB1_MOUSE', 0.25833333333333336),
                   ('MYG_GALCR', 'HBB1_XENTR', 0.23999999999999999),
                   ('MYG_GALCR', 'MYG_ESCGI', 0.84210526315789469),
                   ('MYG_GALCR', 'MYG_DIDMA', 0.83006535947712423),
                   ('MYG_GALCR', 'MYG_ERIEU', 0.85620915032679734),
                   ('MYG_GALCR', 'MYG_ELEMA', 0.84313725490196079),
                   ('PRCA_ANASP', 'PRCA_ANAVA', 0.97199341021416807),
                   ('PRCA_ANASP', 'PRCA_ANAVA', 1.0),
                   ('PRCA_ANAVA', 'PRCA_ANASP', 0.97199341021416807),
                   ('PRCA_ANAVA', 'PRCA_ANASP', 1.0)]

        check_results(results, correct,
                      lambda t:(t[0].id, t[1].id, t[2].pIdentity()))
    def test_multiblast_long(self):
        "testing multi sequence blast with long db to assess thread safety, see issue 79"
        raise SkipTest

        longerFile = testutil.datafile('sp_all_hbb')

        sp_all_hbb = seqdb.SequenceFileDB(longerFile)
        blastmap = blast.BlastMapping(self.prot, verbose=False)
        al = cnestedlist.NLMSA('blasthits', 'memory', pairwiseMode=True,
                               bidirectional=False)
        blastmap(None, al, queryDB=sp_all_hbb) # all vs all
        al.build() # construct the alignment indexes

class Blastx_Test(BlastBase):
    def test_blastx(self):
        "Testing blastx"
        blastmap = blast.BlastxMapping(self.prot, verbose=False)
        
        correct = [(146, 146, 438, 0.979), (146, 146, 438, 0.911),
                   (146, 146, 438, 0.747), (146, 146, 438, 0.664),
                   (146, 146, 438, 0.623), (146, 146, 438, 0.596),
                   (145, 145, 435, 0.510), (143, 143, 429, 0.531),
                   (146, 146, 438, 0.473), (146, 146, 438, 0.473),
                   (146, 146, 438, 0.486), (144, 144, 432, 0.451),
                   (145, 145, 435, 0.455), (144, 144, 432, 0.451),
                   (146, 146, 438, 0.466), (146, 146, 438, 0.459),
                   (52, 52, 156, 0.442), (90, 90, 270, 0.322),
                   (23, 23, 69, 0.435), (120, 120, 360, 0.283),
                   (23, 23, 69, 0.435), (120, 120, 360, 0.258),
                   (23, 23, 69, 0.435), (120, 120, 360, 0.275),
                   (23, 23, 69, 0.435), (120, 120, 360, 0.267)]
        
        results = blastmap[self.dna['gi|171854975|dbj|AB364477.1|']]
        check_results(results, correct,
                      lambda t:(len(t[0]), len(t[1]), len(t[0].sequence),
                                t[2].pIdentity()))

        try:
            results = blastmap[self.prot['HBB1_MOUSE']]
            raise AssertionError('failed to trap blastp in BlastxMapping')
        except ValueError:
            pass
                

class Blastn_Test(BlastBase):
    def test_tblastn(self):
        "Blastn test"
        blastmap = blast.BlastMapping(self.dna, verbose=False)
        result = blastmap[self.prot['HBB1_XENLA']]
        src,dest,edge = iter(result.edges()).next()
        
        self.assertEqual(str(src),
            'LTAHDRQLINSTWGKLCAKTIGQEALGRLLWTYPWTQRYFSSFGNLNSADAVFHNEAVAAHGEK'
            'VVTSIGEAIKHMDDIKGYYAQLSKYHSETLHVDPLNFKRFGGCLSIALARHFHEEYTPELHAAY'
            'EHLFDAIADALGKGYH')
        self.assertEqual(str(dest),
            'LTDAEKAAVSGLWGKVNSDEVGGEALGRLLVVYPWTQRYFDSFGDLSSASAIMGNAKVKAHGKK'
            'VITAFNEGLNHLDSLKGTFASLSELHCDKLHVDPENFRLLGNMIVIVLGHHLGKDFTPAAQAAF'
            'QKVMAGVATALAHKYH')
        self.assertEqual(str(dest.sequence),
            'CTGACTGATGCTGAGAAGGCTGCTGTCTCTGGCCTGTGGGGAAAGGTGAACTCCGATGAAGTTG'
            'GTGGTGAGGCCCTGGGCAGGCTGCTGGTTGTCTACCCTTGGACCCAGAGGTACTTTGATAGCTT'
            'TGGAGACCTATCCTCTGCCTCTGCTATCATGGGTAATGCCAAAGTGAAGGCCCATGGCAAGAAA'
            'GTGATAACTGCCTTTAACGAGGGCCTGAATCACTTGGACAGCCTCAAGGGCACCTTTGCCAGCC'
            'TCAGTGAGCTCCACTGTGACAAGCTCCATGTGGATCCTGAGAACTTCAGGCTCCTGGGCAATAT'
            'GATCGTGATTGTGCTGGGCCACCACCTGGGCAAGGATTTCACCCCCGCTGCACAGGCTGCCTTC'
            'CAGAAGGTGATGGCTGGAGTGGCCACTGCCCTGGCTCACAAGTACCAC')
        
        self.assertAlmostEqual(edge.pIdentity(), 0.451, 3)

        blastmap = blast.BlastMapping(self.prot)
        try:
            results = blastmap[self.dna['gi|171854975|dbj|AB364477.1|']]
            raise AssertionError('failed to trap blastx in BlastMapping')
        except ValueError:
            pass

    def test_megablast(self):
        'test megablast'
        blastmap = blast.MegablastMapping(self.dna, verbose=False)
        from pygr.sequence import Sequence
        # must use copy of sequence to get "self matches" from NLMSA...
        query = Sequence(str(self.dna['gi|171854975|dbj|AB364477.1|']),
                         'foo')
        try:
            result = blastmap[query]
        except OSError: # silently ignore missing RepeatMasker, megablast
            return
        found = [(len(t[0]),len(t[1])) for t in result.edges()]
        assert found == [(444, 444)]

    def test_bad_subject(self):
        "Test bad subjects"

        # file not added to repository
        from pygr import parse_blast
        from pygr.nlmsa_utils import CoordsGroupStart,CoordsGroupEnd

        correctCoords = ((12,63,99508,99661),
                 (65,96,99661,99754),
                 (96,108,99778,99814),
                 (108,181,99826,100045))
        
        fp = file(testutil.datafile('bad_tblastn.txt'))
        try:
            p = parse_blast.BlastHitParser()
            it = iter(correctCoords)
            for ival in p.parse_file(fp):
                if not isinstance(ival,(CoordsGroupStart,
                            CoordsGroupEnd)):
                    assert (ival.src_start,ival.src_end,
                        ival.dest_start,ival.dest_end) \
                        == it.next()
        finally:
            fp.close()

# not used currently
def all_vs_all_blast_save():
    """
    Creates the blast files used during testing. 
    Must be called before running the tests
    """

    tempdir = testutil.TempDir('blast-test')
    testutil.change_pygrdatapath(tempdir.path)

    sp_hbb1 = testutil.datafile('sp_hbb1')
    all_vs_all = testutil.tempdatafile('all_vs_all')

    sp = seqdb.BlastDB(sp_hbb1)
    msa = cnestedlist.NLMSA(all_vs_all ,mode='w', pairwiseMode=True, bidirectional=False)
    
    # get strong homologs, save alignment in msa for every sequence
    reader = islice(sp.iteritems(), None)
    for id, s in reader:
        sp.blast(s, msa, expmax=1e-10, verbose=False) 

    # done constructing the alignment, so build the alignment db indexes
    msa.build(saveSeqDict=True) 

    db = msa.seqDict.dicts.keys()[0]
    working, result = {}, {}
    for k in db.values():
        edges = msa[k].edges(minAlignSize=12, pIdentityMin=0.5)
        for t in edges:
            assert len(t[0]) >= 12
        tmpdict = dict(map(lambda x:(x, None), [(str(t[0]), str(t[1]), t[2].pIdentity(trapOverflow=False)) for t in edges]))
        result[repr(k)] = tmpdict.keys()
        result[repr(k)].sort()
    
    # save it into worldbase
    data = testutil.TestData()
    data.__doc__ = 'sp_allvall'
    data.result = result
    worldbase.Bio.Blast = data
    worldbase.commit()

    #return msa

if __name__ == '__main__':
    PygrTestProgram(verbosity=2)

