// ===== QMDG WEB APP - COMPLETE JAVASCRIPT =====

const app = {
    API_BASE: window.location.origin + '/api',
    currentChart: null,
    currentTopic: 'Tổng Quát',
    allTopics: [],
    currentPalaceIndex: 4,
    palaceOrder: [4, 9, 2, 3, 5, 7, 8, 1, 6],
    dungThanExpanded: true,
    zoomLevel: parseFloat(localStorage.getItem('zoomLevel')) || 1.0,

    // ===== INITIALIZATION =====
    async init() {
        this.showLoading(true);
        await this.loadTopics();
        await this.calculate();
        this.setupEventListeners();
        this.startClock();
        this.applyZoom();
        this.showLoading(false);
    },

    // ===== LOGIN =====
    async login() {
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${this.API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            const data = await response.json();

            if (data.success) {
                document.getElementById('login-screen').classList.add('d-none');
                document.getElementById('main-app').classList.remove('d-none');
                this.init();
            } else {
                alert(data.message || 'Mật khẩu không chính xác');
            }
        } catch (e) {
            console.error(e);
            alert('Lỗi kết nối server');
        }
    },

    // ===== EVENT LISTENERS =====
    setupEventListeners() {
        // Topic search
        const searchInput = document.getElementById('topic-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.searchTopics(e.target.value));
        }

        // Topic selection
        const topicSelect = document.getElementById('topic-select');
        if (topicSelect) {
            topicSelect.addEventListener('change', (e) => {
                this.currentTopic = e.target.value;
                this.updateDungThan();
            });
        }

        // Tab switching - load content when tab is shown
        const maihoaTab = document.getElementById('maihoa-tab');
        if (maihoaTab) {
            maihoaTab.addEventListener('shown.bs.tab', () => {
                this.loadMaiHoa();
            });
        }

        const luchaoTab = document.getElementById('luchao-tab');
        if (luchaoTab) {
            luchaoTab.addEventListener('shown.bs.tab', () => {
                this.loadLucHao();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.navigatePalace(-1);
            if (e.key === 'ArrowRight') this.navigatePalace(1);

            if ((e.ctrlKey || e.metaKey) && e.key === '+') {
                e.preventDefault();
                this.zoomIn();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === '-') {
                e.preventDefault();
                this.zoomOut();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === '0') {
                e.preventDefault();
                this.resetZoom();
            }
        });
    },

    // ===== CLOCK =====
    startClock() {
        const updateTime = () => {
            const now = new Date();
            const timeStr = now.toLocaleTimeString('vi-VN', {
                hour: '2-digit',
                minute: '2-digit'
            });
            const elem = document.getElementById('current-time');
            if (elem) elem.textContent = timeStr;
        };
        updateTime();
        setInterval(updateTime, 1000);
    },

    // ===== TOPICS =====
    async loadTopics() {
        try {
            const response = await fetch(`${this.API_BASE}/topics`);
            this.allTopics = await response.json();

            const select = document.getElementById('topic-select');
            select.innerHTML = '<option value="Tổng Quát">Tổng Quát</option>';

            this.allTopics.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t;
                opt.textContent = t;
                select.appendChild(opt);
            });
        } catch (e) {
            console.error('Lỗi tải chủ đề:', e);
        }
    },

    async searchTopics(query) {
        try {
            const response = await fetch(`${this.API_BASE}/search-topics?q=${encodeURIComponent(query)}`);
            const topics = await response.json();

            const select = document.getElementById('topic-select');
            select.innerHTML = '';

            topics.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t;
                opt.textContent = t;
                select.appendChild(opt);
            });

            if (topics.length === 1) {
                select.value = topics[0];
                this.currentTopic = topics[0];
                await this.updateDungThan();
            }
        } catch (e) {
            console.error('Lỗi tìm kiếm:', e);
        }
    },

    clearSearch() {
        document.getElementById('topic-search').value = '';
        this.loadTopics();
    },

    // ===== CALCULATE CHART =====
    async calculate() {
        try {
            this.showLoading(true);

            // Get initial data
            const initRes = await fetch(`${this.API_BASE}/initial-data`);
            const initData = await initRes.json();

            // Calculate chart
            const calcRes = await fetch(`${this.API_BASE}/calculate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            this.currentChart = await calcRes.json();
            this.updateChartInfo(initData);
            this.renderGrid();
            this.updateDungThan();
            this.updateLunarCalendar(initData);

            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi tính toán:', e);
            this.showLoading(false);
            alert('Lỗi tính toán bàn');
        }
    },

    async reloadCurrentTime() {
        await this.calculate();
    },

    // ===== UPDATE UI =====
    updateChartInfo(initData) {
        if (!this.currentChart) return;

        document.getElementById('info-ju').textContent = this.currentChart.ju || '--';
        document.getElementById('info-solar').textContent = this.currentChart.solarTerm || '--';
        document.getElementById('info-type').textContent = this.currentChart.isYang ? 'Dương Độn ☀️' : 'Âm Độn 🌙';
        document.getElementById('info-zhifu').textContent = initData.zhifu || '--';
        document.getElementById('info-zhishi').textContent = initData.zhishi || '--';
        document.getElementById('info-branch').textContent = initData.hourBranch || '--';

        const lunarText = `Giờ ${this.currentChart.can_gio || '--'} ${initData.hourBranch || '--'} | Ngày ${this.currentChart.can_ngay || '--'} | Cục ${this.currentChart.ju || '--'}`;
        document.getElementById('info-lunar').textContent = lunarText;
    },

    updateLunarCalendar(initData) {
        const lunarDiv = document.getElementById('lunar-calendar');
        if (lunarDiv) {
            lunarDiv.textContent = `Giờ ${initData.canGio} ${initData.chiGio} | Ngày ${initData.canNgay} ${initData.chiNgay} | Tháng ${initData.canThang} ${initData.chiThang} | Năm ${initData.canNam} ${initData.chiNam}`;
        }

        const tietKhi = document.getElementById('tiet-khi');
        if (tietKhi) tietKhi.textContent = initData.solarTerm || 'N/A';

        const cuc = document.getElementById('cuc-display');
        if (cuc) cuc.textContent = initData.ju || 'N/A';

        const duongAm = document.getElementById('duong-am');
        if (duongAm) duongAm.textContent = initData.isYang ? 'Dương' : 'Âm';

        const trucPhu = document.getElementById('truc-phu-display');
        if (trucPhu) trucPhu.textContent = initData.zhifu || 'N/A';

        const trucSu = document.getElementById('truc-su-display');
        if (trucSu) trucSu.textContent = initData.zhishi || 'N/A';
    },

    // ===== RENDER GRID =====
    renderGrid() {
        const grid = document.getElementById('qimen-grid');
        if (!grid || !this.currentChart) return;

        grid.innerHTML = '';
        const layout = [[4, 9, 2], [3, 5, 7], [8, 1, 6]];

        layout.forEach(row => {
            row.forEach(num => {
                const p = this.currentChart.palaces.find(x => x.number === num);
                if (!p) return;

                const div = document.createElement('div');
                div.className = 'palace-box';
                div.setAttribute('data-auspicious', p.auspiciousness >= 7 ? 'high' : (p.auspiciousness <= 4 ? 'low' : 'neutral'));

                const symbols = [];
                if (p.isKongWang) symbols.push('💀');
                if (p.isDiMa) symbols.push('🐎');

                div.innerHTML = `
                    <div style="position: absolute; top: 4px; left: 6px; font-size: 1.3rem; font-weight: bold; color: #667eea;">${num}</div>
                    <div style="text-align: center; font-weight: bold; margin-top: 24px; font-size: 0.9rem; color: #2c3e50;">${p.name}</div>
                    <div style="text-align: center; font-size: 0.7rem; color: #7f8c8d; margin-bottom: 4px;">${p.element}</div>
                    
                    <div style="color: #2980b9; font-weight: 600; font-size: 0.85rem; text-align: center;">⭐ ${p.star}</div>
                    <div style="color: #27ae60; font-weight: bold; font-size: 0.85rem; text-align: center;">🚪 ${p.door}</div>
                    <div style="color: #7f8c8d; font-style: italic; font-size: 0.75rem; text-align: center;">👤 ${p.deity}</div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 6px; padding: 0 4px;">
                        <span style="color: #8e44ad; font-weight: bold; font-size: 0.85rem;">${p.stemHeaven}</span>
                        <span style="font-size: 1rem;">${symbols.join(' ')}</span>
                        <span style="color: #c0392b; font-weight: bold; font-size: 0.85rem;">${p.stemEarth}</span>
                    </div>
                `;

                div.addEventListener('click', () => this.showPalaceDetail(num));
                grid.appendChild(div);
            });
        });
    },

    // ===== PALACE DETAIL =====
    async showPalaceDetail(palaceNum) {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.API_BASE}/palace-topic-analysis/${palaceNum}/${encodeURIComponent(this.currentTopic)}`);
            const analysis = await response.json();

            const modal = new bootstrap.Modal(document.getElementById('palaceModal'));
            document.getElementById('palace-modal-title').innerHTML =
                `🏰 Cung ${palaceNum} - ${analysis.name} <span class="badge bg-secondary">${analysis.element}</span>`;

            const body = document.getElementById('palace-body');
            let html = `<div class="palace-detail">`;

            // Dụng Thần
            if (analysis.dungThan && analysis.dungThan.length > 0) {
                html += `
                    <div class="alert ${analysis.hasDungThan ? 'alert-success' : 'alert-warning'} mb-3">
                        <h6 class="alert-heading">🎯 Dụng Thần cho "${this.currentTopic}"</h6>
                        <p class="mb-1"><strong>Cần xem:</strong> ${analysis.dungThan.join(', ')}</p>
                        ${analysis.hasDungThan ?
                        `<p class="mb-0 text-success"><strong>✅ Cung này chứa:</strong> ${analysis.dungThanFound.join(', ')}</p>` :
                        `<p class="mb-0 text-warning">⚠️ Cung này không chứa Dụng Thần chính</p>`
                    }
                    </div>
                `;
            }

            // Basic Info
            html += `
                <h6 class="text-primary border-bottom pb-2">📊 Thông Tin Cơ Bản</h6>
                <div class="row mb-3">
                    <div class="col-6"><strong>Quái Tượng:</strong> ${analysis.name}</div>
                    <div class="col-6"><strong>Ngũ Hành:</strong> <span class="badge bg-info">${analysis.element}</span></div>
                    <div class="col-6"><strong>Cửu Tinh:</strong> ⭐ ${analysis.star}</div>
                    <div class="col-6"><strong>Bát Môn:</strong> 🚪 ${analysis.door}</div>
                    <div class="col-6"><strong>Bát Thần:</strong> 👤 ${analysis.deity}</div>
                    <div class="col-6"><strong>Can Thiên/Địa:</strong> ${analysis.stemHeaven}/${analysis.stemEarth}</div>
                </div>
            `;

            // Descriptions
            html += `
                <h6 class="text-success border-bottom pb-2 mt-3">🌟 Đặc Điểm Chi Tiết</h6>
                <div class="mb-3">
                    <p class="small"><strong>⭐ ${analysis.star}:</strong> ${analysis.starDescription}</p>
                    <p class="small"><strong>🚪 ${analysis.door}:</strong> ${analysis.doorDescription}</p>
                    <p class="small"><strong>👤 ${analysis.deity}:</strong> ${analysis.deityDescription}</p>
                </div>
            `;

            // Topic Interpretation
            if (analysis.topicInterpretation) {
                html += `
                    <h6 class="text-info border-bottom pb-2 mt-3">📖 Giải Thích Theo Chủ Đề</h6>
                    <div class="alert alert-light mb-3">
                        <p class="small mb-0">${analysis.topicInterpretation}</p>
                    </div>
                `;
            }

            // Advice
            if (analysis.advice) {
                html += `
                    <h6 class="text-warning border-bottom pb-2 mt-3">💡 Lời Khuyên</h6>
                    <div class="alert alert-warning mb-3">
                        <p class="small mb-0">${analysis.advice}</p>
                    </div>
                `;
            }

            // Special Markers
            const markers = [];
            if (analysis.isKongWang) markers.push('💀 Không Vong');
            if (analysis.isDiMa) markers.push('🐎 Dịch Mã');
            if (markers.length > 0) {
                html += `
                    <div class="alert alert-secondary mt-3">
                        <strong>Đặc điểm:</strong> ${markers.join(' | ')}
                    </div>
                `;
            }

            html += `</div>`;
            body.innerHTML = html;

            modal.show();
            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi chi tiết cung:', e);
            this.showLoading(false);
            alert('Lỗi tải chi tiết cung');
        }
    },

    // ===== NAVIGATION =====
    navigatePalace(direction) {
        this.currentPalaceIndex = (this.currentPalaceIndex + direction + this.palaceOrder.length) % this.palaceOrder.length;
        const palaceNum = this.palaceOrder[this.currentPalaceIndex];

        const indicator = document.getElementById('current-palace-indicator');
        if (indicator) {
            indicator.textContent = `Cung ${palaceNum}`;
        }

        this.showPalaceDetail(palaceNum);
    },

    // ===== DỤNG THẦN =====
    async updateDungThan() {
        const panel = document.getElementById('dung-than-content');
        if (!panel) return;

        try {
            const response = await fetch(`${this.API_BASE}/dung-than/${encodeURIComponent(this.currentTopic)}`);
            const data = await response.json();

            let html = '<div class="small">';

            if (data.ky_mon && data.ky_mon.dung_than) {
                html += `<div class="mb-2"><strong>🔮 Kỳ Môn:</strong> ${data.ky_mon.dung_than}</div>`;
            }

            if (data.mai_hoa && data.mai_hoa.dung_than) {
                html += `<div class="mb-2"><strong>📖 Mai Hoa:</strong> ${data.mai_hoa.dung_than}</div>`;
            }

            if (data.luc_hao && data.luc_hao.dung_than) {
                html += `<div><strong>☯️ Lục Hào:</strong> ${data.luc_hao.dung_than}</div>`;
            }

            html += '</div>';
            panel.innerHTML = html;
        } catch (e) {
            console.error('Lỗi Dụng Thần:', e);
        }
    },

    toggleDungThan() {
        this.dungThanExpanded = !this.dungThanExpanded;
        const content = document.getElementById('dung-than-content');
        const toggle = document.getElementById('dung-than-toggle');

        if (this.dungThanExpanded) {
            content.style.display = 'block';
            toggle.textContent = '▼';
        } else {
            content.style.display = 'none';
            toggle.textContent = '▶';
        }
    },

    // ===== ANALYSIS =====
    async showAnalysis() {
        if (!this.currentChart) {
            alert('Vui lòng lập bàn trước');
            return;
        }

        try {
            this.showLoading(true);

            const findPalace = (stem) => this.currentChart.palaces.find(p => p.stemHeaven === stem)?.number || 1;
            const chu_idx = findPalace(this.currentChart.can_ngay);
            const khach_idx = findPalace(this.currentChart.can_gio);

            const res = await fetch(`${this.API_BASE}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: this.currentTopic,
                    chu_idx,
                    khach_idx
                })
            });

            const data = await res.json();
            const body = document.getElementById('analysis-body');
            let html = `<div class="analysis-result">`;

            if (data.do_tin_cay_tong) {
                html += `<div class="alert alert-info">
                    <strong>📊 Độ tin cậy:</strong> ${data.do_tin_cay_tong}%
                </div>`;
            }

            if (data.phan_tich_9_phuong_phap?.ky_mon?.ket_luan) {
                html += `<h6 class="text-primary">🔮 Vị Thế Chủ - Khách</h6>
                <p>${data.phan_tich_9_phuong_phap.ky_mon.ket_luan}</p>`;
            }

            if (data.lien_mach) {
                html += `<hr><h6 class="text-success">⏰ Dòng Chảy Thời Gian</h6>`;
                if (data.lien_mach.qua_khu) html += `<p><strong>Quá khứ:</strong> ${data.lien_mach.qua_khu}</p>`;
                if (data.lien_mach.hien_tai) html += `<p><strong>Hiện tại:</strong> ${data.lien_mach.hien_tai}</p>`;
                if (data.lien_mach.tuong_lai) html += `<p><strong>Tương lai:</strong> ${data.lien_mach.tuong_lai}</p>`;
                if (data.lien_mach.ket_luan_tong_hop) {
                    html += `<div class="alert alert-success mt-3">
                        <strong>📝 Kết luận:</strong> ${data.lien_mach.ket_luan_tong_hop}
                    </div>`;
                }
            }

            html += `</div>`;
            body.innerHTML = html;

            const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
            modal.show();
            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi phân tích:', e);
            this.showLoading(false);
            alert('Lỗi phân tích');
        }
    },

    // ===== COMPARISON =====
    showComparison() {
        const modal = new bootstrap.Modal(document.getElementById('comparisonModal'));
        modal.show();
    },

    async performComparison() {
        const palace1 = parseInt(document.getElementById('compare-palace1').value);
        const palace2 = parseInt(document.getElementById('compare-palace2').value);

        try {
            this.showLoading(true);

            const response = await fetch(`${this.API_BASE}/compare-detailed`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    palace1,
                    palace2,
                    topic: this.currentTopic
                })
            });

            const result = await response.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            this.displayComparisonResult(result);
            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi so sánh:', e);
            this.showLoading(false);
            alert('Lỗi so sánh');
        }
    },

    displayComparisonResult(data) {
        const resultDiv = document.getElementById('comparison-result');

        const html = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card border-primary mb-3">
                        <div class="card-header bg-primary text-white">
                            <h6 class="mb-0">🏠 CUNG CHỦ</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Cung:</strong> ${data.chu?.ten || 'N/A'}</p>
                            <p><strong>Sao:</strong> ${data.chu?.sao || 'N/A'}</p>
                            <p><strong>Môn:</strong> ${data.chu?.cua || 'N/A'}</p>
                            <p><strong>Thần:</strong> ${data.chu?.than || 'N/A'}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card border-danger mb-3">
                        <div class="card-header bg-danger text-white">
                            <h6 class="mb-0">👥 CUNG KHÁCH</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Cung:</strong> ${data.khach?.ten || 'N/A'}</p>
                            <p><strong>Sao:</strong> ${data.khach?.sao || 'N/A'}</p>
                            <p><strong>Môn:</strong> ${data.khach?.cua || 'N/A'}</p>
                            <p><strong>Thần:</strong> ${data.khach?.than || 'N/A'}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card border-warning">
                <div class="card-header bg-warning">
                    <h6 class="mb-0">⚖️ KẾT QUẢ</h6>
                </div>
                <div class="card-body">
                    <p><strong>Ngũ Hành:</strong> ${data.ngu_hanh_moi_quan_he || 'N/A'}</p>
                    <p><strong>Kết luận:</strong> ${data.ket_luan || 'N/A'}</p>
                    <p><strong>Lời khuyên:</strong> ${data.loi_khuyen || 'N/A'}</p>
                </div>
            </div>
        `;

        resultDiv.innerHTML = html;
    },

    // ===== ZOOM =====
    zoomIn() {
        this.zoomLevel = Math.min(this.zoomLevel + 0.1, 2.0);
        this.applyZoom();
    },

    zoomOut() {
        this.zoomLevel = Math.max(this.zoomLevel - 0.1, 0.5);
        this.applyZoom();
    },

    resetZoom() {
        this.zoomLevel = 1.0;
        this.applyZoom();
    },

    applyZoom() {
        const mainApp = document.getElementById('main-app');
        if (mainApp) {
            mainApp.style.transform = `scale(${this.zoomLevel})`;
            mainApp.style.transformOrigin = 'top center';

            const extraPadding = (this.zoomLevel - 1) * 50;
            document.body.style.paddingBottom = `${extraPadding}vh`;

            localStorage.setItem('zoomLevel', this.zoomLevel);
        }
    },

    // ===== MAI HOA =====
    async loadMaiHoa() {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.API_BASE}/mai-hoa`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: this.currentTopic })
            });

            const data = await response.json();
            this.renderMaiHoa(data);

            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi Mai Hoa:', e);
            this.showLoading(false);
        }
    },

    renderMaiHoa(data) {
        const container = document.getElementById('maihoa-content');
        if (!container) return;

        let html = `
            <div class="mai-hoa-result">
                <h5 class="text-primary">📖 Kết Quả Mai Hoa</h5>
                
                <div class="row mb-3">
                    <div class="col-md-4">
                        <div class="card border-primary">
                            <div class="card-header bg-primary text-white">Quẻ Bản</div>
                            <div class="card-body text-center">
                                <h4>${data.qua_ban || 'N/A'}</h4>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card border-success">
                            <div class="card-header bg-success text-white">Quẻ Biến</div>
                            <div class="card-body text-center">
                                <h4>${data.qua_bien || 'N/A'}</h4>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card border-info">
                            <div class="card-header bg-info text-white">Ngũ Hành</div>
                            <div class="card-body text-center">
                                <h4>${data.ngu_hanh || 'N/A'}</h4>
                            </div>
                        </div>
                    </div>
                </div>

                ${data.dung_than ? `
                    <div class="alert alert-success">
                        <h6>🎯 Dụng Thần cho "${this.currentTopic}"</h6>
                        <p><strong>Dụng Thần:</strong> ${data.dung_than}</p>
                        ${data.giai_thich ? `<p><strong>Giải thích:</strong> ${data.giai_thich}</p>` : ''}
                        ${data.cach_xem ? `<p><strong>Cách xem:</strong> ${data.cach_xem}</p>` : ''}
                    </div>
                ` : ''}

                ${data.interpretation ? `
                    <div class="card mt-3">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">📝 Giải Thích</h6>
                        </div>
                        <div class="card-body">
                            <p class="small">${data.interpretation}</p>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        container.innerHTML = html;
    },

    // ===== LỤC HÀO =====
    async loadLucHao() {
        try {
            this.showLoading(true);

            const lucThan = document.getElementById('luc-than-select')?.value || 'Bản thân';

            const response = await fetch(`${this.API_BASE}/luc-hao`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: this.currentTopic,
                    luc_than: lucThan
                })
            });

            const data = await response.json();
            this.renderLucHao(data);

            this.showLoading(false);
        } catch (e) {
            console.error('Lỗi Lục Hào:', e);
            this.showLoading(false);
        }
    },

    renderLucHao(data) {
        const container = document.getElementById('luchao-content');
        if (!container) return;

        let html = `
            <div class="luc-hao-result">
                <h5 class="text-primary">☯️ Kết Quả Lục Hào</h5>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="card border-primary">
                            <div class="card-header bg-primary text-white">Quẻ Bản</div>
                            <div class="card-body text-center">
                                <h4>${data.qua_ban || 'N/A'}</h4>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card border-success">
                            <div class="card-header bg-success text-white">Quẻ Biến</div>
                            <div class="card-body text-center">
                                <h4>${data.qua_bien || 'N/A'}</h4>
                            </div>
                        </div>
                    </div>
                </div>

                ${data.dung_than ? `
                    <div class="alert alert-success">
                        <h6>🎯 Dụng Thần cho "${this.currentTopic}"</h6>
                        <p><strong>Dụng Thần:</strong> ${data.dung_than}</p>
                        ${data.giai_thich_dt ? `<p><strong>Giải thích:</strong> ${data.giai_thich_dt}</p>` : ''}
                        ${data.cach_xem ? `<p><strong>Cách xem:</strong> ${data.cach_xem}</p>` : ''}
                    </div>
                ` : ''}

                ${data.dong_hao && data.dong_hao.length > 0 ? `
                    <div class="card mt-3">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">🔄 Hào Động</h6>
                        </div>
                        <div class="card-body">
                            <p>Hào động: ${data.dong_hao.join(', ')}</p>
                        </div>
                    </div>
                ` : ''}

                ${data.giai_thich ? `
                    <div class="card mt-3">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">📝 Giải Thích</h6>
                        </div>
                        <div class="card-body">
                            <p class="small">${data.giai_thich}</p>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        container.innerHTML = html;
    },

    // ===== LOADING =====
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            if (show) {
                overlay.classList.remove('d-none');
            } else {
                overlay.classList.add('d-none');
            }
        }
    }
};

// Auto-init when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🔮 QMDG Web App Ready');
    });
} else {
    console.log('🔮 QMDG Web App Ready');
}
