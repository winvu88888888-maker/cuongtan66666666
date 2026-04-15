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
# PHẦN 2: DANH MỤC BỔ SUNG — NỘI THẤT, Y TẾ, TÔN GIÁO,
# ĐỊA LÝ, BỘ PHẬN CƠ THỂ, NÔNG NGHIỆP, VĂN PHÒNG, GIA DỤNG
# ═══════════════════════════════════════════════════════════════

VAN_VAT_BO_SUNG = {
    'Kim': {
        # 🛋️ NỘI THẤT
        'noi_that': ['Kệ inox', 'Giá treo quần áo kim loại', 'Gương khung bạc', 'Đèn chùm pha lê',
                     'Bàn kính khung sắt', 'Ghế xoay kim loại', 'Tủ sắt hồ sơ', 'Kệ giày inox',
                     'Móc treo tường', 'Rèm cửa kim tuyến', 'Bệ lavabo inox', 'Vòi sen inox'],
        
        # 🏥 Y TẾ / DƯỢC
        'y_te': ['Dao mổ', 'Kim tiêm', 'Kéo phẫu thuật', 'Kẹp y tế', 'Nẹp xương', 
                 'Máy MRI', 'Máy X-quang', 'Stent tim', 'Implant titan', 'Răng giả kim loại',
                 'Ống nghe y tế', 'Nhiệt kế thủy ngân', 'Xe lăn (khung sắt)', 'Nạng inox',
                 'Thuốc viên nén', 'Thuốc bọc vỏ nhôm', 'Bình oxy', 'Máy thở'],
        
        # ⛪ TÔN GIÁO
        'ton_giao': ['Chuông chùa/nhà thờ', 'Thánh giá bạc/vàng', 'Lư hương đồng', 
                     'Kiếm phát ấn', 'Chén thánh', 'Gương phong thủy bát quái',
                     'Tượng Phật đồng', 'Chuông gió phong thủy', 'La bàn/Kinh Dịch'],
        
        # 🗻 ĐỊA LÝ
        'dia_ly': ['Mỏ vàng', 'Mỏ bạc', 'Mỏ sắt', 'Núi đá vôi', 'Sa mạc (cát kim loại)',
                   'Khu công nghiệp', 'Nhà máy', 'Ngân hàng', 'Sở giao dịch chứng khoán'],
        
        # 🦴 BỘ PHẬN CƠ THỂ
        'bo_phan_co_the': ['Phổi', 'Ruột già', 'Da', 'Xương', 'Răng', 'Mũi', 'Lông/tóc',
                           'Móng tay', 'Cột sống', 'Sụn', 'Thanh quản'],
        
        # 🌾 NÔNG NGHIỆP
        'nong_nghiep': ['Liềm', 'Cuốc sắt', 'Xẻng sắt', 'Dao phát cỏ', 'Cày sắt',
                        'Bừa', 'Máy gặt liên hợp', 'Máy cày', 'Hệ thống tưới phun'],
        
        # 📎 VĂN PHÒNG
        'van_phong': ['Ghim', 'Kẹp giấy', 'Dao rọc giấy', 'Kéo văn phòng', 'Máy dập ghim',
                      'Khóa tủ hồ sơ', 'Bấm lỗ', 'Thước kẻ kim loại', 'Sọt rác inox'],
        
        # 🏡 GIA DỤNG
        'gia_dung': ['Nồi', 'Chảo', 'Dao bếp', 'Thìa', 'Dĩa', 'Mở nắp chai', 
                     'Nhíp', 'Bấm móng tay', 'Cạo râu', 'Muỗng canh', 'Vá múc',
                     'Máy xay sinh tố (lưỡi)', 'Máy ép trái cây', 'Ấm siêu tốc (inox)',
                     'Bình giữ nhiệt', 'Khay inox', 'Rổ rá inox', 'Kệ gia vị'],
        
        # 🖼️ NGHỆ THUẬT
        'nghe_thuat': ['Tranh đồng đúc', 'Tượng inox', 'Sculpture kim loại', 'Jewelry art',
                       'Chạm khắc bạc', 'Đúc đồng nghệ thuật', 'Khắc laser trên kim loại'],
        
        # 💻 KỸ THUẬT SỐ
        'ky_thuat_so': ['Bitcoin', 'Cryptocurrency', 'Blockchain', 'Fintech', 'NFT vàng',
                        'App ngân hàng', 'Ví điện tử', 'Thanh toán contactless'],
    },
    
    'Mộc': {
        'noi_that': ['Bàn gỗ', 'Ghế gỗ', 'Tủ gỗ', 'Kệ sách gỗ', 'Khung ảnh gỗ',
                     'Rèm vải cotton', 'Thảm cói', 'Chiếu tre', 'Gối bông', 'Chăn len',
                     'Đệm cao su', 'Ghế mây', 'Bàn tre', 'Giá sách tre', 'Bình hoa gỗ'],
        
        'y_te': ['Thuốc thảo dược', 'Thuốc Đông y', 'Châm cứu (cây kim nhưng kỹ thuật Mộc)',
                 'Xoa bóp bấm huyệt', 'Yoga', 'Thiền', 'Mát-xa', 'Bó thuốc nam',
                 'Dầu gió', 'Cao dán', 'Viên uống vitamin tự nhiên', 'Probiotic',
                 'Thực phẩm chức năng hữu cơ', 'Trà thảo dược', 'Tinh dầu chữa bệnh'],
        
        'ton_giao': ['Kinh sách', 'Tràng hạt gỗ', 'Mõ gỗ', 'Bàn thờ gỗ', 'Bài vị gỗ',
                     'Tượng gỗ', 'Hương trầm', 'Giấy sớ', 'Nón lá tu hành', 'Áo cà sa vải'],
        
        'dia_ly': ['Rừng', 'Vườn', 'Công viên', 'Đồng lúa', 'Nương rẫy', 'Rừng nhiệt đới',
                   'Rừng thông', 'Rừng tre', 'Đồi chè', 'Vườn hoa', 'Nhà kính trồng cây'],
        
        'bo_phan_co_the': ['Gan', 'Mật', 'Mắt', 'Gân', 'Cơ bắp', 'Ngón tay', 'Ngón chân',
                           'Đầu gối', 'Vai', 'Cánh tay', 'Cẳng chân', 'Móng tay (keratin)'],
        
        'nong_nghiep': ['Cuốc gỗ', 'Cày gỗ', 'Rổ tre', 'Gánh tre', 'Thúng mủng',
                        'Hạt giống', 'Phân bón hữu cơ', 'Máy xay lúa gỗ', 'Bồ đựng thóc',
                        'Nong nia', 'Quang gánh', 'Đòn gánh', 'Liếp tre'],
        
        'van_phong': ['Bút chì', 'Bút mực', 'Tập vở', 'Sổ tay', 'Phong bì', 'Giấy note',
                      'Thước gỗ', 'Hồ dán', 'Băng keo giấy', 'Bìa hồ sơ', 'File đựng tài liệu'],
        
        'gia_dung': ['Thớt gỗ', 'Đũa tre', 'Muỗng gỗ', 'Rổ mây', 'Giỏ tre',
                     'Hộp gỗ đựng trà', 'Giá đỡ nồi tre', 'Lót nồi tre', 'Khay trà gỗ',
                     'Chổi que', 'Cây lau nhà', 'Thùng gỗ', 'Giỏ đi chợ mây tre'],
        
        'nghe_thuat': ['Tranh thủy mặc', 'Thư pháp', 'Điêu khắc gỗ', 'Tranh lụa',
                       'Tranh giấy dó', 'Origami', 'Ikebana (cắm hoa)', 'Bonsai nghệ thuật'],
        
        'ky_thuat_so': ['Ebook', 'Blog', 'Website tin tức', 'App đọc sách', 'Podcast giáo dục',
                        'Khóa học online', 'Notion', 'Google Docs', 'App trồng cây ảo'],
    },
    
    'Thủy': {
        'noi_that': ['Bể cá', 'Đài phun nước mini', 'Gương soi', 'Rèm xanh navy',
                     'Thảm xanh đậm', 'Đèn nước (lava lamp)', 'Bình thủy sinh',
                     'Tranh biển', 'Đồng hồ cát', 'Bình hoa thủy tinh'],
        
        'y_te': ['Thuốc nước/siro', 'Dịch truyền', 'Nước muối sinh lý', 'Thuốc nhỏ mắt',
                 'Thuốc nhỏ mũi', 'Oxy già', 'Cồn sát trùng', 'Gel khử khuẩn',
                 'Nước súc miệng', 'Thuốc tẩy giun (lỏng)', 'Kem bôi da', 'Mỡ tra mắt',
                 'Huyết tương', 'Máu truyền', 'Nước ối', 'Thụt rửa'],
        
        'ton_giao': ['Nước thánh', 'Rửa tội', 'Bình tịnh thủy (Quan Âm)', 'Hồ sen chùa',
                     'Sông Hằng (Ấn Độ)', 'Phép rửa', 'Nước cúng', 'Cốc nước thờ'],
        
        'dia_ly': ['Sông', 'Suối', 'Hồ', 'Biển', 'Đại dương', 'Ao', 'Đầm lầy', 'Thác nước',
                   'Sông ngầm', 'Mạch nước ngầm', 'Vịnh', 'Eo biển', 'Phá', 'Lagoon',
                   'Bắc Cực', 'Nam Cực', 'Sông Mekong', 'Sông Amazon', 'Biển Đông'],
        
        'bo_phan_co_the': ['Thận', 'Bàng quang', 'Tai', 'Xương tủy', 'Tử cung', 'Tinh hoàn',
                           'Tuyến tiền liệt', 'Niệu đạo', 'Bọng đái', 'Máu', 'Nước bọt',
                           'Mồ hôi', 'Nước mắt', 'Dịch não tủy'],
        
        'nong_nghiep': ['Hệ thống tưới nhỏ giọt', 'Ao nuôi cá', 'Bè nuôi tôm', 'Ruộng muối',
                        'Trại nuôi tôm hùm', 'Đầm nuôi ngao', 'Hồ nuôi cá tra', 'Bè cá lồng'],
        
        'van_phong': ['Mực in', 'Bút bi (mực lỏng)', 'Bút máy', 'Sơn marker', 'Bảng trắng (xóa ướt)',
                      'Máy hủy giấy (dầu bôi trơn)', 'Bình xịt khử mùi văn phòng'],
        
        'gia_dung': ['Bồn rửa', 'Bồn tắm', 'Vòi nước', 'Máy giặt', 'Chậu rửa', 'Xô nước',
                     'Bình nước nóng', 'Bình lọc nước', 'Giá phơi đồ', 'Bàn ủi hơi nước',
                     'Nồi áp suất (hơi)', 'Máy làm đá', 'Tủ lạnh', 'Máy hút ẩm'],
        
        'nghe_thuat': ['Tranh phong cảnh biển', 'Tranh thủy mặc (nước)', 'Nghệ thuật đá lỏng (resin art)',
                       'Thủy tinh nghệ thuật', 'Điêu khắc băng (ice sculpture)', 'Múa đương đại (flowing)'],
        
        'ky_thuat_so': ['Cloud computing', 'Streaming', 'Flow/pipeline data', 'VPN (tunnel)',
                        'Crypto liquidity', 'Dark web', 'Deep web', 'Torrent', 'Spotify/Apple Music'],
    },
    
    'Hỏa': {
        'noi_that': ['Đèn chùm', 'Đèn bàn', 'Đèn ngủ', 'Nến thơm', 'Lò sưởi trang trí',
                     'Rèm đỏ', 'Thảm đỏ', 'Gương có đèn LED', 'Đèn strip LED',
                     'Quạt trần (có đèn)', 'Kệ đèn', 'Tranh đèn neon'],
        
        'y_te': ['Laser phẫu thuật', 'Đốt điện trị bệnh', 'Xạ trị', 'Hóa trị',
                 'Tia UV khuẩn', 'Đèn trị liệu ánh sáng', 'Châm cứu (đốt moxa/ngải cứu)',
                 'Sấy khô vết thương', 'Thuốc viêm/sốt', 'Paracetamol', 'Ibuprofen',
                 'Vitamin C (chống oxy hóa)', 'Kem chống bỏng', 'Gel hạ sốt'],
        
        'ton_giao': ['Hương', 'Nến thờ', 'Đèn dầu', 'Đuốc hỏa', 'Lửa thiêng',
                     'Pháo (đốt vàng mã)', 'Giấy tiền vàng bạc', 'Bếp thắp hương',
                     'Đèn hoa đăng', 'Đèn lồng Phật đản', 'Đèn cầy', 'Nhang trầm'],
        
        'dia_ly': ['Sa mạc Sahara', 'Thung lũng Chết', 'Miệng núi lửa', 'Suối nước nóng',
                   'Vùng xích đạo', 'Dubai', 'Death Valley', 'Đảo Hawaii (núi lửa)'],
        
        'bo_phan_co_the': ['Tim', 'Ruột non', 'Mắt (viêm)', 'Lưỡi', 'Mạch máu', 'Não',
                           'Hệ thần kinh', 'Tuyến thượng thận', 'Da (viêm đỏ)'],
        
        'nong_nghiep': ['Đốt đồng', 'Phát rẫy đốt nương', 'Lò sấy nông sản', 'Máy sấy thóc',
                        'Lò hun khói', 'Lò nướng bánh', 'Hệ thống sưởi nhà kính'],
        
        'van_phong': ['Máy hủy tài liệu (nhiệt)', 'Máy ép plastic', 'Bảng LED thông báo',
                      'Đèn bàn', 'Máy photocopy (nhiệt)', 'Máy fax', 'Máy scan'],
        
        'gia_dung': ['Bếp gas', 'Bếp điện', 'Bếp từ', 'Lò nướng', 'Lò vi sóng', 'Nồi chiên không dầu',
                     'Máy nướng bánh mì', 'Ấm đun siêu tốc', 'Lò sưởi', 'Quạt sưởi',
                     'Bàn ủi', 'Máy sấy tóc', 'Máy uốn tóc', 'Bếp nướng BBQ'],
        
        'nghe_thuat': ['Sơn dầu', 'Tranh acrylic', 'Múa lửa', 'Graffiti (spray paint)',
                       'Neon art', 'Light painting (nhiếp ảnh)', 'Fire dance', 'Fireworks art'],
        
        'ky_thuat_so': ['Social media (viral)', 'YouTube', 'TikTok', 'Instagram', 'Livestream',
                        'Gaming esports', 'Trending', 'Viral marketing', 'Influencer', 'Meme'],
    },
    
    'Thổ': {
        'noi_that': ['Tường gạch trần', 'Sàn gạch', 'Bàn đá marble', 'Bếp đá granite',
                     'Chậu sứ', 'Bình gốm', 'Tượng trang trí đá', 'Gạch mosaic',
                     'Sàn đá hoa', 'Kệ gạch xây', 'Bồn cầu sứ', 'Bồn rửa đá'],
        
        'y_te': ['Bó bột (xương gãy)', 'Đắp bùn khoáng', 'Tắm bùn trị liệu',
                 'Thuốc chống dạ dày (antacid)', 'Thuốc dạ dày Gaviscon', 'Thuốc tiêu hóa',
                 'Probiotic đường ruột', 'Viên sắt bổ máu', 'Canxi (xương)',
                 'Thạch cao bó bột', 'Đất sét trị liệu', 'Bùn nóng onsen'],
        
        'ton_giao': ['Tượng Phật đá', 'Đền đài', 'Chùa/nhà thờ (bê tông/đá)', 'Mộ phần',
                     'Lăng tẩm', 'Kim tự tháp', 'Bàn thờ đá', 'Bia đá khắc', 'Bùa đất',
                     'Tháp Chàm', 'Stonehenge', 'Angkor Wat', 'Đền Parthenon'],
        
        'dia_ly': ['Đồng bằng', 'Cao nguyên', 'Thung lũng', 'Hang động', 'Sa mạc',
                   'Đồi', 'Núi', 'Đảo', 'Bãi biển (cát)', 'Đồng ruộng', 'Rẫy',
                   'Trung tâm lục địa', 'Lòng chảo', 'Truông', 'Bãi bồi'],
        
        'bo_phan_co_the': ['Dạ dày', 'Lách', 'Miệng', 'Cơ bắp', 'Mô mỡ', 'Da thịt',
                           'Môi', 'Nướu', 'Tuyến nước bọt', 'Tụy', 'Ruột non (phần dưới)'],
        
        'nong_nghiep': ['Cày bừa', 'San lấp đất', 'Đào ao', 'Đắp đê', 'Bón phân',
                        'Ủ phân compost', 'Hệ thống thoát nước ruộng', 'Gieo hạt trực tiếp',
                        'Trồng khoai', 'Trồng ngô', 'Nuôi giun đất', 'Trại nấm'],
        
        'van_phong': ['Chặn giấy đá', 'Ly sứ uống trà', 'Chậu cây văn phòng', 'Pot cây sen đá',
                      'Máy pha cà phê (gốm)', 'Art ceramic trang trí bàn', 'Đĩa đựng card'],
        
        'gia_dung': ['Bát sứ', 'Đĩa sứ', 'Chén trà', 'Ấm trà gốm', 'Bình hoa gốm',
                     'Chậu rửa đá', 'Thớt đá', 'Cối xay', 'Cối giã', 'Ống đũa gốm',
                     'Hũ muối chua', 'Chum sành', 'Vại sành', 'Nồi đất', 'Siêu thuốc đất'],
        
        'nghe_thuat': ['Gốm sứ Bát Tràng', 'Pottery art', 'Điêu khắc đá', 'Sand art (tranh cát)',
                       'Mosaic art', 'Terrazzo art', 'Tạc tượng', 'Tranh gạch ceramic'],
        
        'ky_thuat_so': ['Database/storage', 'Data center', 'Hard drive', 'Backup & archive',
                        'App bất động sản', 'Google Maps/Earth', 'CAD (thiết kế xây dựng)',
                        'Metaverse real estate', 'Digital twin (xây dựng)'],
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
    hanh_bs = VAN_VAT_BO_SUNG.get(hanh, {})
    
    # Merge 2 sources
    merged = {}
    merged.update(hanh_data)
    merged.update(hanh_bs)
    
    if not merged:
        return ""
    
    lines = []
    lines.append(f"=== MỞ RỘNG VẠN VẬT: {hanh} ===")
    
    label_map = {
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
        # Bổ sung V31.5
        'noi_that': '🛋️ Nội thất',
        'y_te': '🏥 Y tế/Dược',
        'ton_giao': '⛪ Tôn giáo',
        'dia_ly': '🗻 Địa lý',
        'bo_phan_co_the': '🦴 Bộ phận cơ thể',
        'nong_nghiep': '🌾 Nông nghiệp',
        'van_phong': '📎 Văn phòng',
        'gia_dung': '🏡 Gia dụng',
        'nghe_thuat': '🖼️ Nghệ thuật',
        'ky_thuat_so': '💻 Kỹ thuật số',
    }
    
    for category, data in merged.items():
        label = label_map.get(category, category)
        
        if isinstance(data, list):
            lines.append(f"{label}: {', '.join(data[:10])}")
        elif isinstance(data, dict):
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
