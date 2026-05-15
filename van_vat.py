# -*- coding: utf-8 -*-
"""
VẠN VẬT PROXY — V42.9.41
Proxy module chuyển tiếp sang van_vat_tong_hop.py
Đảm bảo import ổn định cho free_ai_helper.py
"""

from van_vat_tong_hop import (
    get_van_vat_chi_tiet,
    format_van_vat_for_ai,
    get_tham_tu_mo_ta,
    smart_van_vat_for_question,
)

__all__ = [
    'get_van_vat_chi_tiet',
    'format_van_vat_for_ai',
    'get_tham_tu_mo_ta',
    'smart_van_vat_for_question',
]
