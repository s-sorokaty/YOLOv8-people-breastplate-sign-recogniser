import cProfile
import main
import pstats
from pstats import SortKey

cProfile.run('main.main()', 'restats')
p = pstats.Stats('restats.txt')
p.sort_stats(SortKey.CUMULATIVE).print_stats(30)