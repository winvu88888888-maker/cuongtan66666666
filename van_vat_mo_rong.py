"""
van_vat_mo_rong.py — V31.4 MỞ RỘNG VẠN VẬT ĐẾN MỌI THỨ TRÊN ĐỜI
═══════════════════════════════════════════════════════════════════
Bổ sung thêm hàng trăm loại vật cho mỗi hành, bao trùm:
- 🚗 Phương tiện giao thông
- 👔 Quần áo / Trang phục / Phụ kiện
- 🍜 Thực phẩm / Đồ uống chi tiết
- 💎 Khoáng sản / Đá quý
- 📱 Công nghệ / Điện tử
- 🎵 Nhạc cụ / Nghệ thuật
- ⚽ Thể thao / Giải trí
- 🏭 Công nghiệp / Máy móc
- 💄 Mỹ phẩm / Dược phẩm
- 🧸 Đồ trẻ em / Đồ chơi
- 🪖 Vũ khí / Quân sự
- 🌤️ Thời tiết / Thiên nhiên
- 📐 Hình học / Ký hiệu
- 🎭 Cảm xúc / Trạng thái tâm lý
- 🌍 Quốc gia / Vùng miền
"""

# ═══════════════════════════════════════════════════════════════
# BẢNG MỞ RỘNG THEO NGŨ HÀNH
# ═══════════════════════════════════════════════════════════════

VAN_VAT_MO_RONG = {
    'Kim': {
        # 🚗 PHƯƠNG TIỆN
        'phuong_tien': {
            'chung': ['Xe hơi', 'Xe máy', 'Xe đạp', 'Tàu hỏa', 'Máy bay', 'Tàu ngầm', 'Xe tăng', 'Xe bọc thép'],
            'Đế Vượng': ['Rolls Royce', 'Lamborghini', 'Private jet', 'Xe Maybach', 'Du thuyền kim loại'],
            'Lâm Quan': ['Toyota Camry', 'Honda CR-V', 'BMW 3 series', 'Xe tải Hyundai'],
            'Suy': ['Xe cũ hoen rỉ', 'Xe máy cà tàng', 'Xe đạp rỉ sét'],
            'Tử': ['Xe phế liệu', 'Ô tô bị đập', 'Xe tai nạn nát'],
        },
        
        # 👔 TRANG PHỤC
        'trang_phuc': {
            'chung': ['Áo giáp', 'Dây chuyền bạc', 'Đồng hồ kim loại', 'Kính gọng kim loại', 
                      'Thắt lưng khóa', 'Giày da bóng', 'Nón bảo hiểm', 'Áo khoác da'],
            'Đế Vượng': ['Bộ vest Armani', 'Đồng hồ Patek Philippe', 'Nhẫn kim cương 5 carat',
                         'Vương miện vàng', 'Áo giáp bạch kim', 'Kính Cartier vàng'],
            'Suy': ['Dây chuyền bạc xỉn', 'Đồng hồ cũ chạy sai', 'Kính gãy gọng'],
            'Mộ': ['Áo giáp cổ', 'Trang sức gia truyền', 'Huy chương cũ trong hộp'],
        },
        
        # 🍜 THỰC PHẨM
        'thuc_pham_chi_tiet': {
            'chung': ['Hành tây', 'Tỏi', 'Gừng', 'Ớt', 'Tiêu', 'Quế', 'Hồi', 'Rau mùi',
                      'Wasabi', 'Mustard', 'Sả', 'Riềng', 'Nghệ', 'Bạc hà',
                      'Thịt gà', 'Phổi bò', 'Thịt trắng', 'Cơm cháy giòn'],
            'do_uong': ['Rượu trắng', 'Sake', 'Vodka', 'Soju', 'Nước suối', 'Trà trắng'],
        },
        
        # 💎 KHOÁNG SẢN
        'khoang_san': ['Vàng', 'Bạc', 'Bạch kim', 'Đồng', 'Sắt', 'Nhôm', 'Niken',
                       'Thiếc', 'Kẽm', 'Titan', 'Crom', 'Molypden', 'Tungsten',
                       'Kim cương', 'Sapphire trắng', 'Ngọc trai', 'Thạch anh trắng'],
        
        # 📱 CÔNG NGHỆ
        'cong_nghe': {
            'chung': ['iPhone', 'MacBook', 'iPad', 'Apple Watch', 'AirPods', 'Samsung Galaxy',
                      'Laptop Dell', 'PC Gaming', 'Máy in laser', 'Loa bluetooth',
                      'TV OLED', 'Máy ảnh Canon', 'Drone', 'Robot hút bụi',
                      'Ổ cứng SSD', 'USB flash', 'Tai nghe', 'Sạc không dây'],
            'Đế Vượng': ['Server IBM', 'Siêu máy tính', 'Vệ tinh', 'Máy MRI', 'Robot công nghiệp'],
            'Suy': ['Điện thoại đời cũ', 'Laptop 2010', 'Máy tính bàn cũ', 'iPod cũ'],
            'Tử': ['Điện thoại chết', 'Laptop hỏng main', 'Ổ cứng bad sector'],
        },
        
        # 🪖 VŨ KHÍ
        'vu_khi': ['Kiếm', 'Dao', 'Rìu', 'Búa chiến', 'Giáo', 'Mác', 'Súng', 'Đạn',
                   'Tên lửa', 'Bom', 'Lựu đạn', 'Pháo', 'Tàu chiến', 'Xe tăng',
                   'Khiên', 'Giáp', 'Nỏ', 'Cung tên'],
        
        # 🎵 NHẠC CỤ
        'nhac_cu': ['Chuông đồng', 'Phong linh', 'Kèn đồng (trumpet)', 'Kèn trombone',
                    'Cymbal', 'Chiêng', 'Thanh la', 'Xylophone kim loại',
                    'Harmonica', 'Kèn sáo kim loại', 'Tam giác (triangle)'],
        
        # 🏭 CÔNG NGHIỆP
        'cong_nghiep': ['Cần cẩu', 'Máy tiện', 'Máy phay', 'Máy ép', 'Máy cắt laser',
                        'Dây chuyền sản xuất', 'Lò luyện thép', 'Máy hàn', 'Máy nén khí',
                        'Ống dẫn', 'Van công nghiệp', 'Bình gas', 'Thang máy'],
        
        # ⚽ THỂ THAO
        'the_thao': ['Tạ', 'Barbell', 'Dumbbell', 'Xe đạp racing', 'Kiếm fencing',
                     'Cung tên thể thao', 'Gậy golf kim loại', 'Patin ice'],
        
        # 🌤️ THỜI TIẾT
        'thoi_tiet': ['Sương giá', 'Băng tuyết', 'Gió lạnh', 'Mưa đá', 
                      'Không khí khô hanh', 'Gió thu se lạnh', 'Khí lạnh'],

        # 🎭 CẢM XÚC
        'cam_xuc': ['Buồn', 'Đau đớn', 'Nghiêm khắc', 'Cô đơn', 'Kiên cường',
                    'Dứt khoát', 'Lạnh lùng', 'Tàn nhẫn', 'Công bằng', 'Chính trực'],
        
        # 🌍 QUỐC GIA / VÙNG
        'quoc_gia': ['Phương Tây', 'Châu Âu', 'Mỹ', 'Anh', 'Đức', 'Nhật Bản (công nghệ)',
                     'Hàn Quốc (Samsung)', 'Thụy Sĩ (đồng hồ)', 'Ý (siêu xe)'],
    },
    
    'Mộc': {
        'phuong_tien': {
            'chung': ['Thuyền gỗ', 'Xe kéo gỗ', 'Xe ngựa', 'Xe bò', 'Cáng', 'Thang gỗ', 'Kiệu'],
            'Đế Vượng': ['Thuyền rồng', 'Du thuyền gỗ teak', 'Tàu buồm cổ'],
            'Lâm Quan': ['Thuyền câu gỗ', 'Xe đạp tre', 'Cáng tre'],
            'Suy': ['Thuyền cũ', 'Xe gỗ lung lay', 'Xuồng hỏng'],
        },
        
        'trang_phuc': {
            'chung': ['Áo bông', 'Áo lụa', 'Áo len', 'Quần vải', 'Váy cotton', 'Giày vải',
                      'Nón lá', 'Khăn quàng vải', 'Áo dài', 'Kimono', 'Hanbok'],
            'Đế Vượng': ['Áo dài gấm lụa', 'Kimono tơ tằm', 'Áo lông thú quý', 'Váy haute couture vải tự nhiên'],
            'Suy': ['Áo cũ sờn', 'Quần vải bạc', 'Giày vải rách', 'Khăn cũ'],
            'Mộ': ['Áo xưa cất kỹ', 'Áo gia truyền', 'Trang phục lễ hội cổ'],
        },
        
        'thuc_pham_chi_tiet': {
            'chung': ['Rau muống', 'Rau cải', 'Rau xà lách', 'Bắp cải', 'Bí xanh', 'Mướp', 
                      'Khổ qua', 'Cà chua', 'Dưa chuột', 'Đậu que', 'Ngô', 'Khoai mì',
                      'Chuối', 'Cam', 'Bưởi', 'Chanh', 'Me', 'Xoài', 'Ổi', 'Táo',
                      'Nho', 'Lê', 'Đào', 'Mận', 'Hồng', 'Dừa', 'Sầu riêng', 'Chôm chôm',
                      'Gạo', 'Lúa mì', 'Yến mạch', 'Đậu nành', 'Đậu xanh', 'Đậu phộng',
                      'Mè', 'Hạt điều', 'Hạt óc chó', 'Hạnh nhân', 'Macca',
                      'Thịt bò (gan bò)', 'Mộc nhĩ', 'Nấm hương', 'Đậu hủ', 'Tempeh'],
            'do_uong': ['Nước mía', 'Nước dừa', 'Sinh tố', 'Nước ép trái cây', 
                        'Trà xanh', 'Trà hoa cúc', 'Rượu trái cây', 'Kombucha'],
        },
        
        'khoang_san': ['Ngọc bích (jade)', 'Emerald (ngọc lục bảo)', 'Malachite',
                       'Peridot', 'Tourmaline xanh', 'Aventurine', 'Hổ phách (amber)'],
        
        'cong_nghe': {
            'chung': ['Máy tính bằng gỗ (DIY)', 'Ốp lưng gỗ', 'Bàn phím cơ gỗ',
                      'Loa gỗ', 'Tai nghe vỏ gỗ', 'Giá đỡ laptop gỗ'],
        },
        
        'nhac_cu': ['Guitar acoustic', 'Guitar classic', 'Ukulele', 'Đàn tranh', 'Đàn bầu',
                    'Sáo trúc', 'Tiêu', 'Đàn nhị', 'Piano (thân gỗ)', 'Violin (gỗ)',
                    'Cello', 'Đàn tỳ bà', 'Mõ gỗ', 'Castanets gỗ', 'Maracas gỗ',
                    'Đàn tam thập lục', 'Đàn nguyệt', 'Kèn oboe (thân gỗ)'],
        
        'cong_nghiep': ['Xưởng gỗ', 'Máy cưa', 'Máy bào', 'Máy khoan gỗ', 'Lò sấy gỗ',
                        'Xưởng giấy', 'Nhà máy dệt', 'Xưởng may', 'Nhà in'],
        
        'the_thao': ['Gậy cricket (gỗ)', 'Gậy bóng chày (gỗ)', 'Bàn bóng bàn', 
                     'Ván lướt sóng gỗ', 'Cung tre', 'Kiếm kendo gỗ (bokken)',
                     'Thảm yoga (cotton)', 'Dây thừng leo núi'],
        
        'thoi_tiet': ['Gió xuân', 'Mưa phùn', 'Sấm sét (sét đánh cây)', 'Bão lớn (cây đổ)',
                      'Thời tiết ấm áp', 'Mùa xuân hoa nở'],
        
        'cam_xuc': ['Nhân ái', 'Từ bi', 'Sáng tạo', 'Kiên nhẫn', 'Dễ thương',
                    'Mơ mộng', 'Hay giận (Can nộ)', 'Tự do', 'Phóng khoáng'],
        
        'quoc_gia': ['Phương Đông', 'Việt Nam (tre, lúa)', 'Trung Quốc (trà, gỗ)',
                     'Nhật Bản (tre/bonsai)', 'Indonesia (gỗ teak)', 'Brazil (nhiệt đới)'],
        
        # 💄 MỸ PHẨM
        'my_pham': ['Serum thiên nhiên', 'Kem dưỡng hữu cơ', 'Son môi thảo dược',
                    'Dầu dừa', 'Dầu argan', 'Tinh dầu tràm trà', 'Mặt nạ lá neem',
                    'Xà phòng handmade', 'Bột nghệ', 'Nước hoa hồng'],
        
        # 🧸 ĐỒ TRẺ EM
        'do_tre_em': ['Xích đu gỗ', 'Khối gỗ xếp hình', 'Búp bê vải', 'Cầu trượt gỗ',
                      'Xe gỗ đồ chơi', 'Bảng chữ cái gỗ', 'Xếp hình gỗ Montessori'],
    },
    
    'Thủy': {
        'phuong_tien': {
            'chung': ['Thuyền', 'Tàu thủy', 'Canoe', 'Kayak', 'Phà', 'Xuồng', 'Bè'],
            'Đế Vượng': ['Du thuyền siêu sang', 'Tàu sân bay', 'Tàu ngầm hạt nhân', 'Cruise ship'],
            'Lâm Quan': ['Thuyền máy', 'Ca nô', 'Tàu cá lớn', 'Phà chở xe'],
            'Suy': ['Thuyền cũ', 'Xuồng hỏng', 'Bè mục'],
        },
        
        'trang_phuc': {
            'chung': ['Áo tắm', 'Đồ lặn (wetsuit)', 'Áo phao', 'Ống chân nhái', 'Kính lặn',
                      'Áo mưa', 'Ủng cao su', 'Áo khoác chống nước', 'Mũ thủy thủ'],
            'Đế Vượng': ['Bộ đồ lặn chuyên nghiệp', 'Bikini nhung', 'Áo mưa Burberry'],
            'Suy': ['Áo mưa rách', 'Ủng cũ', 'Áo tắm cũ'],
        },
        
        'thuc_pham_chi_tiet': {
            'chung': ['Cá thu', 'Cá hồi', 'Cá ngừ', 'Tôm hùm', 'Cua hoàng đế', 'Sò huyết',
                      'Ốc hương', 'Bào ngư', 'Hàu', 'Mực', 'Bạch tuộc', 'Sứa',
                      'Rong biển', 'Tảo spirulina', 'Muối biển', 'Nước mắm Phú Quốc',
                      'Cá khô', 'Tôm khô', 'Mắm ruốc', 'Mắm tôm', 'Mắm cá',
                      'Dưa hấu', 'Dưa gang', 'Thạch dừa', 'Chè đậu đen',
                      'Súp (phở, bún, mì nước)', 'Canh', 'Cháo', 'Lẩu'],
            'do_uong': ['Nước suối', 'Nước khoáng', 'Nước dừa', 'Trà đá', 'Cà phê sữa đá',
                        'Bia', 'Rượu vang', 'Rum', 'Gin', 'Whisky', 'Champagne',
                        'Cocktail', 'Smoothie', 'Sinh tố', 'Sữa tươi', 'Sữa chua',
                        'Trà sữa', 'Nước ép', 'Coconut water', 'Matcha latte'],
        },
        
        'khoang_san': ['Ngọc trai đen', 'Aquamarine', 'Lapis lazuli', 'Labradorite',
                       'Obsidian đen', 'Onyx đen', 'Hematite', 'Moonstone',
                       'Sapphire xanh đậm', 'Tanzanite'],
        
        'cong_nghe': {
            'chung': ['Máy lọc nước', 'Máy giặt', 'Bình nóng lạnh', 'Máy rửa bát',
                      'Máy lọc không khí (ẩm)', 'Máy phun sương', 'Máy tạo hơi nước'],
        },
        
        'nhac_cu': ['Trống nước', 'Đàn bầu', 'Kèn ốc biển', 'Steel drum (Trinidad)',
                    'Rain stick', 'Ocean drum', 'Sáo nước', 'Waterphone'],
        
        'cong_nghiep': ['Nhà máy nước', 'Đập thủy điện', 'Trạm bơm', 'Nhà máy bia',
                        'Nhà máy nước giải khát', 'Xưởng nước mắm', 'Xưởng đá',
                        'Hệ thống tưới tiêu', 'Kênh mương', 'Đê đập'],
        
        'the_thao': ['Bơi', 'Lặn', 'Lướt ván', 'Kayak', 'Cano', 'Đua thuyền',
                     'Polo nước', 'Nhảy cầu', 'Trượt nước', 'Lướt sóng',
                     'Bóng nước', 'Câu cá thể thao'],
        
        'thoi_tiet': ['Mưa to', 'Bão biển', 'Sóng thần', 'Lũ lụt', 'Mưa phùn',
                      'Sương mù', 'Tuyết rơi', 'Mưa đá', 'Gió mùa Đông Bắc'],
        
        'cam_xuc': ['Sợ hãi', 'Lo lắng', 'Bất an', 'Linh hoạt', 'Khôn ngoan',
                    'Thâm sâu', 'Bí ẩn', 'Trầm lặng', 'Đa nghi', 'Nhạy cảm'],
        
        'quoc_gia': ['Phương Bắc', 'Bắc Cực', 'Scandinavia', 'Canada', 'Russia',
                     'New Zealand', 'Iceland', 'Nhật Bản (biển)', 'Maldives (đảo)'],
        
        'my_pham': ['Nước hoa', 'Perfume', 'Kem dưỡng ẩm', 'Serum hyaluronic',
                    'Toner', 'Micellar water', 'Sữa rửa mặt', 'Kem chống nắng dạng gel',
                    'Mặt nạ sheet', 'Xịt khoáng', 'Dầu dưỡng tóc'],
        
        'do_tre_em': ['Phao bơi', 'Súng nước', 'Bong bóng xà phòng', 'Bể bơi mini',
                      'Vịt cao su', 'Đồ chơi tắm', 'Cát kinetic'],
    },
    
    'Hỏa': {
        'phuong_tien': {
            'chung': ['Xe đua F1', 'Xe mô tô sport', 'Xe điện Tesla', 'Xe chữa cháy'],
            'Đế Vượng': ['Tên lửa SpaceX', 'Xe đua Nascar', 'Siêu xe Ferrari đỏ'],
            'Lâm Quan': ['Xe Vespa đỏ', 'Xe bus 2 tầng London', 'Xe cứu thương'],
            'Suy': ['Xe pháo cũ', 'Xe cứu hỏa nghỉ hưu'],
        },
        
        'trang_phuc': {
            'chung': ['Áo đỏ', 'Váy đỏ', 'Giày đỏ', 'Son môi đỏ', 'Kính mắt thời trang',
                      'Trang phục biểu diễn', 'Đồ sequin lấp lánh', 'Áo lông vũ',
                      'Áo vest đỏ', 'Cà vạt đỏ', 'Mũ cowboy'],
            'Đế Vượng': ['Váy dạ hội Oscar', 'Áo choàng vua/hoàng hậu đỏ', 'Bộ sưu tập Valentino đỏ'],
            'Suy': ['Áo phai màu', 'Váy cũ', 'Trang phục hết mốt'],
        },
        
        'thuc_pham_chi_tiet': {
            'chung': ['Thit nướng BBQ', 'Steak bò', 'Thịt xiên que', 'Pizza lò nướng',
                      'Bánh mì nướng', 'Cơm cháy', 'Popcorn', 'Khoai tây chiên',
                      'Gà rán KFC', 'Tempura', 'Chả giò', 'Bánh tráng nướng',
                      'Cà phê đen', 'Sô cô la đen', 'Khổ qua', 'Trà đặc', 'Thuốc đắng',
                      'Ớt hiểm', 'Tiêu Cayenne', 'Habanero', 'Tabasco'],
            'do_uong': ['Cà phê espresso', 'Cà phê đen đá', 'Trà đen Earl Grey',
                        'Rượu brandy', 'Cognac', 'Tequila', 'Mezcal',
                        'Nước tăng lực Red Bull', 'Monster Energy'],
        },
        
        'khoang_san': ['Ruby', 'Garnet', 'Fire opal', 'Sunstone', 'Carnelian',
                       'Jasper đỏ', 'Rhodolite', 'Spinel đỏ', 'Amber (hổ phách đỏ)'],
        
        'cong_nghe': {
            'chung': ['Tivi OLED', 'Màn hình LED', 'Đèn LED', 'Laser', 'Máy chiếu',
                      'Camera hồng ngoại', 'Kính AR/VR', 'Drone camera',
                      'Màn hình quảng cáo điện tử', 'Billboard LED'],
            'Đế Vượng': ['Hệ thống laser show', 'Màn hình Times Square', 'Hologram'],
            'Suy': ['TV CRT cũ', 'Đèn huỳnh quang nhấp nháy'],
        },
        
        'nhac_cu': ['Trống lớn', 'Trống snare', 'Tom-tom', 'Bongo', 'Conga',
                    'Guitar điện', 'Bass điện', 'Synthesizer', 'DJ Turntable',
                    'Kèn trumpet', 'Kèn tuba', 'Trống điện tử', 'Sampler'],
        
        'cong_nghiep': ['Lò nung', 'Lò phản ứng', 'Nhà máy điện', 'Nhà máy nhiệt',
                        'Xưởng hàn', 'Lò đúc', 'Nhà máy thủy tinh', 'Xưởng gốm nung'],
        
        'the_thao': ['Boxing', 'MMA', 'Kickboxing', 'Chạy marathon', 'Chạy nước rút',
                     'Đua xe F1', 'Đua moto', 'Bắn cung', 'Bắn súng thể thao',
                     'Thể dục dụng cụ', 'Nhảy hiện đại', 'Aerobic'],
        
        'thoi_tiet': ['Nắng gắt', 'Hạn hán', 'Cháy rừng', 'Nóng bức', 'Sét đánh',
                      'Sóng nhiệt heat wave', 'Hiện tượng El Nino'],
        
        'cam_xuc': ['Vui vẻ', 'Hạnh phúc', 'Nhiệt huyết', 'Đam mê', 'Giận dữ',
                    'Phấn khích', 'Tự hào', 'Nóng nảy', 'Bốc đồng', 'Yêu thương mãnh liệt'],
        
        'quoc_gia': ['Phương Nam', 'Úc (nắng)', 'Ấn Độ', 'Dubai', 'Bắc Phi (Sahara)',
                     'Mexico', 'Spain', 'Italy (thời trang, ẩm thực)'],
        
        'my_pham': ['Son môi đỏ', 'Mascara', 'Eyeliner', 'Phấn highlight',
                    'Bronzer', 'Blush đỏ', 'Nail polish đỏ', 'Body glitter'],
        
        'do_tre_em': ['Đèn ngủ hình sao', 'Pháo bông', 'Đèn lồng', 'Kính vạn hoa',
                      'Búp bê barbie', 'Xe đồ chơi điều khiển', 'Slime phát sáng'],
    },
    
    'Thổ': {
        'phuong_tien': {
            'chung': ['Xe tải', 'Xe ben', 'Xe ủi', 'Xe xúc', 'Xe lu', 'Xe cẩu', 'Xe trộn bê tông'],
            'Đế Vượng': ['Xe đào siêu lớn', 'Cẩu bánh xích khổng lồ', 'Máy xúc CAT lớn nhất'],
            'Lâm Quan': ['Xe tải Howo', 'Xe ben Kamaz', 'Xe lu Dynapac'],
            'Suy': ['Xe tải cũ', 'Xe ủi hỏng', 'Xe ben rỉ sét'],
        },
        
        'trang_phuc': {
            'chung': ['Áo nâu (nhà sư)', 'Quần kaki', 'Đồ bảo hộ lao động', 'Ủng xây dựng',
                      'Nón bảo hộ vàng', 'Găng tay vải', 'Yếm', 'Áo chống nắng nâu'],
            'Đế Vượng': ['Áo gấm vàng', 'Long bào (áo vua)', 'Trang phục hoàng gia màu vàng'],
            'Suy': ['Áo bảo hộ cũ', 'Quần kaki rách', 'Ủng nứt'],
            'Mộ': ['Đồ tang lễ', 'Áo xá (nhà sư)', 'Y phục cổ xưa'],
        },
        
        'thuc_pham_chi_tiet': {
            'chung': ['Khoai lang', 'Khoai tây', 'Khoai môn', 'Khoai sọ', 'Sắn', 'Dong',
                      'Cơm trắng', 'Bánh mì', 'Bánh bao', 'Mantou', 'Naan', 'Tortilla',
                      'Phở', 'Bún', 'Miến', 'Cháo', 'Xôi',
                      'Đường', 'Mật ong', 'Mật mía', 'Bánh ngọt', 'Bánh trung thu',
                      'Bí đỏ', 'Bí ngô', 'Ngô ngọt', 'Lạc (đậu phộng)', 'Khoai lang mật',
                      'Nấm hương', 'Nấm rơm', 'Nấm đùi gà', 'Nấm linh chi', 'Nấm truffle'],
            'do_uong': ['Sữa đậu nành', 'Nước mía', 'Trà sữa trân châu', 
                        'Rượu nếp', 'Rượu đế', 'Mật ong pha nước', 'Smoothie chuối'],
        },
        
        'khoang_san': ['Granite', 'Cẩm thạch (marble)', 'Đá vôi', 'Đá sa thạch', 'Slate',
                       'Tiger eye (mắt hổ)', 'Citrine', 'Topaz vàng', 'Jasper vàng',
                       'Đá thạch anh khói', 'Kim cương vàng', 'Đá mã não',
                       'Đất sét', 'Kaolin', 'Feldspar', 'Mica', 'Thạch cao'],
        
        'cong_nghe': {
            'chung': ['Máy đào', 'Máy trộn bê tông', 'Cân điện tử', 'Máy đo địa chất',
                      'GPS đo đạc', 'Drone khảo sát', 'Máy quét 3D địa hình',
                      'Sensor đo độ ẩm đất', 'Trạm quan trắc'],
        },
        
        'nhac_cu': ['Trống đất (udu drum)', 'Ocarina', 'Cồng chiêng', 'Trống đồng Đông Sơn',
                    'Djembe (gỗ+da)', 'Tabla', 'Xylophone', 'Marimba',
                    'Lithophone (đàn đá)', 'Didgeridoo'],
        
        'cong_nghiep': ['Mỏ than', 'Mỏ đá', 'Nhà máy xi măng', 'Nhà máy gạch',
                        'Xưởng gốm sứ', 'Công trường xây dựng', 'Nhà máy thủy tinh',
                        'Xưởng đúc bê tông', 'Mỏ khoáng sản', 'Hầm mỏ'],
        
        'the_thao': ['Đấu vật sumo', 'Judo', 'Wrestling', 'Cử tạ', 'Strongman',
                     'Leo núi', 'Hiking', 'Golf (trên cỏ/đất)', 'Bóng đá (sân đất)',
                     'Xe đạp địa hình MTB', 'Motocross (đất)'],
        
        'thoi_tiet': ['Động đất', 'Núi lửa phun', 'Sạt lở đất', 'Bụi cát sa mạc',
                      'Thời tiết nóng ẩm cuối hạ', 'Giao mùa', 'Oi bức'],
        
        'cam_xuc': ['Trung thực', 'Kiên nhẫn', 'Bảo thủ', 'Lo lắng', 'Tin tưởng',
                    'Chung thủy', 'Trầm tĩnh', 'Cố chấp', 'Bình tĩnh', 'Vững vàng'],
        
        'quoc_gia': ['Trung Quốc (đại lục)', 'Ai Cập (kim tự tháp)', 'Peru (Machu Picchu)',
                     'Ấn Độ (Taj Mahal)', 'Campuchia (Angkor Wat)', 'Rome (Colosseum)',
                     'Đồng bằng sông Cửu Long', 'Tây Nguyên'],
        
        'my_pham': ['Kem nền', 'Foundation', 'Concealer', 'Phấn phủ', 'Setting powder',
                    'Mặt nạ đất sét (clay mask)', 'Scrub (tẩy da chết)', 'Bùn khoáng'],
        
        'do_tre_em': ['Đất nặn Play-Doh', 'Cát động lực kinetic sand', 'Lego gạch',
                      'Đồ chơi xây dựng', 'Xe công trường đồ chơi', 'Búp bê gốm'],
    },
}


# ═══════════════════════════════════════════════════════════════
# HELPER: MERGE VỚI FILE CHÍNH van_vat_chi_tiet.py
# ═══════════════════════════════════════════════════════════════

def get_expanded_items(hanh, category):
    """Lấy danh sách mở rộng theo hành và category.
    
    Args:
        hanh: str — Kim/Mộc/Thủy/Hỏa/Thổ
        category: str — phuong_tien, trang_phuc, thuc_pham_chi_tiet, khoang_san, 
                        cong_nghe, nhac_cu, cong_nghiep, the_thao, thoi_tiet,
                        cam_xuc, quoc_gia, my_pham, do_tre_em, vu_khi
    
    Returns: dict hoặc list
    """
    hanh_data = VAN_VAT_MO_RONG.get(hanh, {})
    return hanh_data.get(category, {})


def format_expanded_for_ai(hanh, truong_sinh_stage=None):
    """Format toàn bộ dữ liệu mở rộng cho AI đọc."""
    hanh_data = VAN_VAT_MO_RONG.get(hanh, {})
    if not hanh_data:
        return ""
    
    lines = []
    lines.append(f"=== MỞ RỘNG VẠN VẬT: {hanh} ===")
    
    for category, data in hanh_data.items():
        label = {
            'phuong_tien': '🚗 Phương tiện',
            'trang_phuc': '👔 Trang phục',
            'thuc_pham_chi_tiet': '🍜 Thực phẩm',
            'khoang_san': '💎 Khoáng sản',
            'cong_nghe': '📱 Công nghệ',
            'nhac_cu': '🎵 Nhạc cụ',
            'cong_nghiep': '🏭 Công nghiệp',
            'the_thao': '⚽ Thể thao',
            'thoi_tiet': '🌤️ Thời tiết',
            'cam_xuc': '🎭 Cảm xúc',
            'quoc_gia': '🌍 Vùng miền',
            'my_pham': '💄 Mỹ phẩm',
            'do_tre_em': '🧸 Đồ trẻ em',
            'vu_khi': '🪖 Vũ khí',
        }.get(category, category)
        
        if isinstance(data, list):
            lines.append(f"{label}: {', '.join(data[:10])}")
        elif isinstance(data, dict):
            # Lấy theo tầng nếu có
            items = data.get(truong_sinh_stage, data.get('chung', []))
            if isinstance(items, list):
                lines.append(f"{label}: {', '.join(items[:10])}")
            elif isinstance(items, dict):
                for k, v in items.items():
                    if isinstance(v, list):
                        lines.append(f"{label} ({k}): {', '.join(v[:6])}")
                    else:
                        lines.append(f"{label} ({k}): {v}")
    
    return "\n".join(lines)
