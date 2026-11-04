# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

print("TEST 1: MU vs Liverpool ai thắng?")
res1 = helper.answer_question("MU vs Liverpool ai thắng?")
with open("test_out_mu.txt", "w", encoding="utf-8") as f:
    f.write(res1)

print("TEST 2: Tôi có nên đầu tư bất động sản không?")
res2 = helper.answer_question("Tôi có nên đầu tư bất động sản không?")
with open("test_out_dautu.txt", "w", encoding="utf-8") as f:
    f.write(res2)

print("DONE")
