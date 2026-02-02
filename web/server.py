"""
Flask Server cho Web App Kỳ Môn Độn Giáp
Tích hợp tất cả tính năng từ code hiện có
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import datetime as dt_module
import sys
import os

# Add dist to path - go up one level from web folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
dist_path = os.path.join(parent_dir, 'dist')
if dist_path not in sys.path:
    sys.path.insert(0, dist_path)

# Import all modules
try:
    from qmdg_data import *
    from qmdg_data import KY_MON_DATA, TOPIC_INTERPRETATIONS
    import qmdg_calc
    from qmdg_detailed_analysis import phan_tich_chi_tiet_cung, so_sanh_chi_tiet_chu_khach
    from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de, tao_phan_tich_lien_mach
    from integrated_knowledge_base import (
        get_comprehensive_palace_info, 
        format_info_for_display,
        get_qua_info,
        get_sao_info,
        get_mon_info,
        get_can_info
    )
    from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, tinh_qua_ngau_nhien, giai_qua
    from luc_hao_kinh_dich import lap_qua_luc_hao
    
    try:
        from dung_than_200_chu_de_day_du import (
            DUNG_THAN_200_CHU_DE,
            hien_thi_dung_than_200,
            lay_dung_than_200
        )
        USE_200_TOPICS = True
    except ImportError:
        USE_200_TOPICS = False
    
    try:
        from database_tuong_tac import (
            LUC_THAN_MAPPING,
            SINH_KHAC_MATRIX,
            TUONG_TAC_SAO_MON,
            QUY_TAC_CHON_DUNG_THAN,
            ANH_HUONG_MUA,
            TRONG_SO_PHAN_TICH,
            TRONG_SO_YEU_TO,
            LUC_THAN_THEO_CHU_DE,
            goi_y_doi_tuong_theo_chu_de
        )
        from phan_tich_da_tang import (
            chon_dung_than_theo_chu_de,
            xac_dinh_luc_than,
            phan_tich_sinh_khac_hop,
            phan_tich_tuong_tac_trong_cung,
            phan_tich_tuong_tac_giua_cac_cung,
            phan_tich_yeu_to_thoi_gian,
            tinh_diem_tong_hop,
            phan_tich_toan_dien
        )
        USE_MULTI_LAYER = True
    except ImportError:
        USE_MULTI_LAYER = False

    # AI Factory Modules
    try:
        from ai_modules.autonomous_miner import run_mining_cycle, load_config
        from ai_modules.shard_manager import get_hub_stats
    except ImportError:
        try:
            from autonomous_miner import run_mining_cycle, load_config
            from shard_manager import get_hub_stats
        except: pass
        
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

app = Flask(__name__, static_folder='static', template_folder='.')
CORS(app)

# Password
PASSWORD = "1987"

# ==================== API ENDPOINTS ====================

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Login authentication"""
    data = request.json
    password = data.get('password', '')
    
    if password == PASSWORD:
        return jsonify({'success': True, 'message': 'Đăng nhập thành công'})
    else:
        return jsonify({'success': False, 'message': 'Mật khẩu không đúng'})

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get all topics"""
    topics = sorted(list(TOPIC_INTERPRETATIONS.keys()))
    return jsonify(topics)

@app.route('/api/search-topics', methods=['GET'])
def search_topics():
    """Search topics"""
    query = request.args.get('q', '').lower()
    all_topics = sorted(list(TOPIC_INTERPRETATIONS.keys()))
    
    if not query:
        return jsonify(all_topics)
    
    filtered = [t for t in all_topics if query in t.lower()]
    return jsonify(filtered)

@app.route('/api/current-time', methods=['GET'])
def get_current_time():
    """Get current time"""
    now = dt_module.datetime.now()
    return jsonify({
        'currentTime': now.strftime('%H:%M'),
        'fullTime': now.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/initial-data', methods=['GET'])
def get_initial_data():
    """Get initial QMDG data"""
    now = dt_module.datetime.now()
    
    try:
        params = qmdg_calc.calculate_qmdg_params(now)
        
        return jsonify({
            'ju': params.get('cuc', '1 Cục'),
            'zhifu': params.get('truc_phu', 'Thiên Tâm'),
            'zhishi': params.get('truc_su', 'Sinh'),
            'hourBranch': params.get('chi_gio', 'Dần'),
            'solarTerm': params.get('tiet_khi', 'Lập Xuân'),
            'isYang': params.get('is_duong_don', True),
            'canGio': params.get('can_gio', 'Giáp'),
            'canNgay': params.get('can_ngay', 'Ất'),
            'canThang': params.get('can_thang', 'Bính'),
            'canNam': params.get('can_nam', 'Đinh'),
            'chiGio': params.get('chi_gio', 'Dần'),
            'chiNgay': params.get('chi_ngay', 'Mão'),
            'chiThang': params.get('chi_thang', 'Thìn'),
            'chiNam': params.get('chi_nam', 'Tỵ')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate QMDG chart with full details"""
    data = request.json
    
    try:
        # Get current time params
        now = dt_module.datetime.now()
        params = qmdg_calc.calculate_qmdg_params(now)
        
        # Get Can Gio for calculations
        CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        CAN_CHI_Gio = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        
        map_can_ngay = {"Giáp": 0, "Kỷ": 0, "Ất": 1, "Canh": 1, "Bính": 2, "Tân": 2, 
                        "Đinh": 3, "Nhâm": 3, "Mậu": 4, "Quý": 4}
        idx_start = map_can_ngay.get(params['can_ngay'], 0)
        idx_chi = CAN_CHI_Gio.index(params['chi_gio'])
        can_gio_idx = (idx_start * 2 + idx_chi) % 10
        can_gio = CAN_10[can_gio_idx]
        
        # Calculate boards
        from qmdg_data import an_bai_luc_nghi, lap_ban_qmdg, tinh_khong_vong, tinh_dich_ma
        
        dia_can = an_bai_luc_nghi(params['cuc'], params['is_duong_don'])
        thien_ban, can_thien_ban, nhan_ban, than_ban, truc_phu_cung = lap_ban_qmdg(
            params['cuc'], params['truc_phu'], params['truc_su'], 
            can_gio, params['chi_gio'], params['is_duong_don']
        )
        
        # Calculate special palaces
        khong_vong = tinh_khong_vong(can_gio, params['chi_gio'])
        dich_ma = tinh_dich_ma(params['chi_gio'])
        
        # Format palaces with full information
        palaces = []
        for i in range(1, 10):
            sao = thien_ban.get(i, '')
            cua = nhan_ban.get(i, '')
            than = than_ban.get(i, '')
            can_thien = can_thien_ban.get(i, '')
            can_dia = dia_can.get(i, '')
            
            # Calculate auspiciousness score (1-10)
            auspiciousness = 5  # Default neutral
            
            # Check door auspiciousness
            door_data = KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua + " Môn", {})
            cat_hung = door_data.get("Cát_Hung", "Bình")
            
            if cat_hung == "Đại Cát":
                auspiciousness = 9
            elif cat_hung == "Cát":
                auspiciousness = 7
            elif cat_hung == "Hung":
                auspiciousness = 3
            elif cat_hung == "Đại Hung":
                auspiciousness = 1
            
            # Check star quality
            star_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(sao, {})
            star_cat_hung = star_data.get('Cát_Hung', 'Bình')
            if star_cat_hung == "Cát":
                auspiciousness = min(10, auspiciousness + 1)
            elif star_cat_hung == "Hung":
                auspiciousness = max(1, auspiciousness - 1)
            
            palaces.append({
                'number': i,
                'name': QUAI_TUONG.get(i, ''),
                'element': CUNG_NGU_HANH.get(i, ''),
                'star': sao,
                'door': cua,
                'deity': than,
                'stemHeaven': can_thien,
                'stemEarth': can_dia,
                'isKongWang': i in khong_vong,
                'isDiMa': i == dich_ma,
                'auspiciousness': auspiciousness,
                'catHung': cat_hung
            })
        
        return jsonify({
            'ju': f"{params.get('cuc', 1)} Cục",
            'solarTerm': params.get('tiet_khi', 'Lập Xuân'),
            'isYang': params.get('is_duong_don', True),
            'can_gio': can_gio,
            'can_ngay': params.get('can_ngay', 'Ất'),
            'palaces': palaces,
            'zhifu': params.get('truc_phu', 'Thiên Tâm'),
            'zhishi': params.get('truc_su', 'Sinh'),
            'hourBranch': params.get('chi_gio', 'Dần')
        })
        
    except Exception as e:
        import traceback
        print(f"Error in calculate: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/palace-detail/<int:palace_num>', methods=['GET'])
def get_palace_detail(palace_num):
    """Get palace detail"""
    try:
        # Get comprehensive info
        info = get_comprehensive_palace_info(palace_num)
        
        return jsonify({
            'number': palace_num,
            'name': info.get('name', ''),
            'element': info.get('element', ''),
            'star': info.get('star', ''),
            'door': info.get('door', ''),
            'deity': info.get('deity', ''),
            'stemHeaven': info.get('stem_heaven', ''),
            'stemEarth': info.get('stem_earth', ''),
            'starDescription': info.get('star_desc', ''),
            'doorDescription': info.get('door_desc', ''),
            'deityDescription': info.get('deity_desc', ''),
            'isKongWang': info.get('is_kong_wang', False),
            'isDiMa': info.get('is_di_ma', False)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/palace-topic-analysis/<int:palace_num>/<topic>', methods=['GET'])
def get_palace_topic_analysis(palace_num, topic):
    """Get palace analysis for specific topic"""
    try:
        # Get basic palace info
        info = get_comprehensive_palace_info(palace_num)
        
        # Get topic data
        topic_data = TOPIC_INTERPRETATIONS.get(topic, {})
        dung_than_list = topic_data.get('Dụng_Thần', [])
        luan_giai = topic_data.get('Luận_Giải_Gợi_Ý', '')
        
        # Check if palace contains Dụng Thần
        palace_elements = [
            info.get('star', ''),
            info.get('door', ''),
            info.get('deity', ''),
            info.get('stem_heaven', ''),
            info.get('stem_earth', '')
        ]
        
        dung_than_found = [dt for dt in dung_than_list if any(dt in pe for pe in palace_elements)]
        has_dung_than = len(dung_than_found) > 0
        
        # Get detailed Dụng Thần if available
        topic_interpretation = luan_giai
        advice = ""
        
        if USE_200_TOPICS:
            dt_200 = lay_dung_than_200(topic)
            if dt_200 and 'ky_mon' in dt_200:
                km = dt_200['ky_mon']
                topic_interpretation = km.get('giai_thich', luan_giai)
                advice = km.get('cach_xem', '')
        
        return jsonify({
            'number': palace_num,
            'name': info.get('name', ''),
            'element': info.get('element', ''),
            'star': info.get('star', ''),
            'door': info.get('door', ''),
            'deity': info.get('deity', ''),
            'stemHeaven': info.get('stem_heaven', ''),
            'stemEarth': info.get('stem_earth', ''),
            'starDescription': info.get('star_desc', ''),
            'doorDescription': info.get('door_desc', ''),
            'deityDescription': info.get('deity_desc', ''),
            'dungThan': dung_than_list,
            'dungThanFound': dung_than_found,
            'hasDungThan': has_dung_than,
            'topicInterpretation': topic_interpretation,
            'advice': advice,
            'isKongWang': info.get('is_kong_wang', False),
            'isDiMa': info.get('is_di_ma', False)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dung-than/<topic>', methods=['GET'])
def get_dung_than(topic):
    """Get Dụng Thần for topic"""
    try:
        result = {
            'topic': topic,
            'ky_mon': {},
            'mai_hoa': {},
            'luc_hao': {}
        }
        
        # Get from 200 topics database
        if USE_200_TOPICS:
            dt_data = lay_dung_than_200(topic)
            if dt_data:
                result.update(dt_data)
        
        # Get from main database
        topic_data = TOPIC_INTERPRETATIONS.get(topic, {})
        if topic_data:
            result['ky_mon']['dung_than'] = ', '.join(topic_data.get('Dụng_Thần', []))
            result['ky_mon']['luan_giai'] = topic_data.get('Luận_Giải_Gợi_Ý', '')
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Comprehensive analysis"""
    data = request.json
    topic = data.get('topic', 'Tổng Quát')
    chu_idx = data.get('chu_idx', 5)
    khach_idx = data.get('khach_idx', 1)
    
    try:
        # Get detailed analysis
        if USE_MULTI_LAYER:
            analysis = phan_tich_toan_dien(topic, chu_idx, khach_idx)
        else:
            analysis = {
                'do_tin_cay_tong': 75,
                'phan_tich_9_phuong_phap': {
                    'ky_mon': {
                        'ket_luan': 'Phân tích cơ bản'
                    }
                }
            }
        
        # Get timeline analysis
        try:
            lien_mach = tao_phan_tich_lien_mach(topic, chu_idx, khach_idx)
            analysis['lien_mach'] = lien_mach
        except:
            pass
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare-detailed', methods=['POST'])
def compare_detailed():
    """Detailed comparison between 2 palaces"""
    data = request.json
    palace1 = data.get('palace1', 5)
    palace2 = data.get('palace2', 1)
    topic = data.get('topic', 'Tổng Quát')
    
    try:
        result = so_sanh_chi_tiet_chu_khach(palace1, palace2, topic)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mai-hoa', methods=['POST'])
def mai_hoa():
    """Mai Hoa divination with topic-specific interpretation"""
    data = request.json
    topic = data.get('topic', 'Tổng Quát')
    
    try:
        now = dt_module.datetime.now()
        qua_result = tinh_qua_theo_thoi_gian(now)
        
        # Get basic interpretation
        interpretation = ""
        if 'ten_qua' in qua_result:
            giai_qua_result = giai_qua(qua_result['ten_qua'])
            interpretation = str(giai_qua_result)
        
        # Get topic-specific Dụng Thần
        dung_than_info = {}
        if USE_200_TOPICS:
            dt_data = lay_dung_than_200(topic)
            if dt_data and 'mai_hoa' in dt_data:
                dung_than_info = dt_data['mai_hoa']
        
        return jsonify({
            'qua_ban': qua_result.get('ten_qua', ''),
            'qua_bien': qua_result.get('qua_bien', ''),
            'qua_ho': qua_result.get('qua_ho', ''),
            'dong_hao': qua_result.get('dong_hao', 0),
            'ngu_hanh': qua_result.get('ngu_hanh', ''),
            'interpretation': interpretation,
            'dung_than': dung_than_info.get('dung_than', ''),
            'giai_thich': dung_than_info.get('giai_thich', ''),
            'cach_xem': dung_than_info.get('cach_xem', '')
        })
    except Exception as e:
        import traceback
        print(f"Error in mai_hoa: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/luc-hao', methods=['POST'])
def luc_hao():
    """Lục Hào divination with Lục Thân analysis"""
    data = request.json
    topic = data.get('topic', 'Tổng Quát')
    luc_than = data.get('luc_than', 'Bản thân')
    
    try:
        now = dt_module.datetime.now()
        lh_result = lap_qua_luc_hao(now)
        
        # Get topic-specific Dụng Thần
        dung_than_info = {}
        if USE_200_TOPICS:
            dt_data = lay_dung_than_200(topic)
            if dt_data and 'luc_hao' in dt_data:
                dung_than_info = dt_data['luc_hao']
        
        # Format result
        result = {
            'qua_ban': lh_result.get('qua_ban', ''),
            'qua_bien': lh_result.get('qua_bien', ''),
            'dong_hao': lh_result.get('dong_hao', []),
            'luc_than': lh_result.get('luc_than', {}),
            'luc_thu': lh_result.get('luc_thu', {}),
            'vuong_suy': lh_result.get('vuong_suy', {}),
            'giai_thich': str(lh_result),
            'dung_than': dung_than_info.get('dung_than', ''),
            'giai_thich_dt': dung_than_info.get('giai_thich', ''),
            'cach_xem': dung_than_info.get('cach_xem', '')
        }
        
        return jsonify(result)
    except Exception as e:
        import traceback
        print(f"Error in luc_hao: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/comprehensive-analysis', methods=['POST'])
def comprehensive_analysis():
    """Comprehensive analysis integrating all 3 methods"""
    data = request.json
    topic = data.get('topic', 'Tổng Quát')
    chu_idx = data.get('chu_idx', 5)
    khach_idx = data.get('khach_idx', 1)
    
    try:
        now = datetime.now()
        
        # Get palace info helper
        def get_palace_info(idx):
            return {
                'so': idx,
                'ten': QUAI_TUONG.get(idx, 'N/A'),
                'hanh': CUNG_NGU_HANH.get(idx, 'N/A')
            }
        
        chu = get_palace_info(chu_idx)
        khach = get_palace_info(khach_idx)
        
        # Super detailed analysis
        result = {
            'topic': topic,
            'chu': chu,
            'khach': khach,
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Try to get 9-aspect analysis
        try:
            from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de, tao_phan_tich_lien_mach
            res_9pp = phan_tich_sieu_chi_tiet_chu_de(topic, chu, khach, now)
            result['phan_tich_9_phuong_dien'] = res_9pp
            
            # Get timeline analysis
            mqh = tinh_ngu_hanh_sinh_khac(chu['hanh'], khach['hanh'])
            res_lien_mach = tao_phan_tich_lien_mach(topic, chu, khach, now, res_9pp, mqh)
            result['lien_mach'] = res_lien_mach
        except Exception as e:
            print(f"Error in 9-aspect analysis: {e}")
            result['phan_tich_9_phuong_dien'] = {
                'error': 'Không thể tạo phân tích 9 phương diện'
            }
        
        # Get Mai Hoa
        try:
            qua_mh = tinh_qua_theo_thoi_gian(now)
            result['mai_hoa'] = {
                'qua_ban': qua_mh.get('ten_qua', ''),
                'qua_bien': qua_mh.get('qua_bien', ''),
                'ngu_hanh': qua_mh.get('ngu_hanh', '')
            }
        except Exception as e:
            print(f"Error in Mai Hoa: {e}")
            result['mai_hoa'] = {'error': str(e)}
        
        # Get Lục Hào
        try:
            qua_lh = lap_qua_luc_hao(now)
            result['luc_hao'] = {
                'qua_ban': qua_lh.get('qua_ban', ''),
                'qua_bien': qua_lh.get('qua_bien', '')
            }
        except Exception as e:
            print(f"Error in Lục Hào: {e}")
            result['luc_hao'] = {'error': str(e)}
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        print(f"Error in comprehensive_analysis: {e}")
        print(traceback.format_exc())
@app.route('/api/factory/stats', methods=['GET'])
def get_factory_stats():
    """Get AI Factory Stats for n8n"""
    try:
        stats = get_hub_stats()
        config = load_config()
        return jsonify({
            "status": "online",
            "shards_total": stats.get("total", 0),
            "shards_size_mb": stats.get("size_mb", 0.0),
            "autonomous_active": config.get("autonomous_247", False),
            "last_run": config.get("last_run", "N/A")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/factory/run-cycle', methods=['POST'])
def run_factory_cycle():
    """Trigger a mining cycle via n8n"""
    try:
        config = load_config()
        api_key = config.get("api_key")
        if not api_key:
            return jsonify({"success": False, "error": "API Key not configured"}), 400
        
        # Run in a separate thread to not block the request
        import threading
        thread = threading.Thread(target=run_mining_cycle, args=(api_key,))
        thread.start()
        
        return jsonify({"success": True, "message": "Mining cycle started in background"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== STATIC FILES ====================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("🔮 Starting Kỳ Môn Độn Giáp Web Server...")
    print("📍 Server: http://localhost:5000")
    print("🌐 Access from other devices: Use ngrok")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
