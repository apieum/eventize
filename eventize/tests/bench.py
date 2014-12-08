#!/bin/env python
import sys, os
import profile, pstats

sys_version = '%s.%s.%s' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])

if 'bench.py' in __file__:
    root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
else:
    root_dir = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..'))

examples_dir = os.path.join(root_dir, 'eventize', 'tests', 'examples')
if not os.path.isdir(examples_dir):
    raise RuntimeError("Can't load example dir: %s" % examples_dir)

sys.path.insert(1, root_dir)

def profile_example(example_name, sort_by='cumulative'):
    example = open(os.path.join(examples_dir, '%s.py' % example_name), 'r').read()
    profiler = profile.Profile()
    profiler.run(example)
    stats = pstats.Stats(profiler).sort_stats(sort_by)
    bench_file = os.path.join(examples_dir, '%s_%s.bench' % (example_name, sys_version))
    stats.dump_stats(bench_file)
    print("Bench results written to:%s  %s" %(os.linesep, bench_file))

profile_example('subject_observer')
profile_example('method')
profile_example('attribute')
profile_example('inheritance1')
