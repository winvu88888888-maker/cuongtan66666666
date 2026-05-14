
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
from question_parser import QTYPE_RULES
for rule in QTYPE_RULES:
    kw = rule.get('keywords', [])
    kw_str = ', '.join(kw[:3]) + '...'
    print(rule['qtype'] + ': ' + kw_str)

