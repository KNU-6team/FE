async function loadHTML(selector, file) {
    const res = await fetch(file);
    const html = await res.text();
    document.querySelector(selector).innerHTML = html;
}

function getNested(obj, path) {
  if (!obj || !path) return null;
  return path.split('.').reduce((acc, key) => (acc && acc[key] !== undefined) ? acc[key] : null, obj);
}

function populateReportFromData(report) {
  if (!report) return;

  document.querySelectorAll('[data-field]').forEach(el => {
    const key = el.getAttribute('data-field');
    const val = getNested(report, key);
    if (val !== null && val !== undefined) {
      // 이미지 태그면 src 업데이트
      if (el.tagName === 'IMG') {
        el.src = String(val);
        return;
      }

      // 원본문자에서 단위나 순위 접미사(예: '번째', '순위')를 찾아 보존하는 로직
      const original = el.textContent || '';
      // '번째' 또는 '순위' 같은 접미사가 있으면 정수로 표기 후 접미사 붙이기
      const rankMatch = original.match(/(번째|순위)/);
      if (rankMatch) {
        const suffix = rankMatch[1];
        const intVal = parseInt(String(val), 10);
        if (!Number.isNaN(intVal)) {
          el.textContent = `${intVal}${suffix}`;
          return;
        }
      }

      // 단위(예: cm, kg, %, kg/m²)가 원본문자에 포함되어 있으면 유지
      const unitMatch = original.match(/(cm|kg|%|kg\/m²)/);
      if (unitMatch) {
        el.textContent = String(val) + unitMatch[0];
      } else {
        el.textContent = String(val);
      }
    }
  });

  document.querySelectorAll('[data-field-prefix]').forEach(el => {
    const key = el.getAttribute('data-field-prefix');
    const val = getNested(report, key);
    if (val !== null && val !== undefined) {
      const original = el.textContent || '';
      const parts = original.split(/\s+/);
      parts[0] = String(val);
      el.textContent = parts.join(' ');
    }
  });
}

function positionBMIIndicator(report) {
  if (!report) return;
  const rate = getNested(report, 'weight_info.obesity_rate');
  if (rate === null || rate === undefined) return;
  
  const numeric = parseFloat(String(rate));
  if (Number.isNaN(numeric)) return;

  // bodymass.js의 calculateBmiPosition 함수 사용
  const position = calculateBmiPosition(numeric);

  // Find indicator element inside loaded page-bodymass fragment
  const indicator = document.querySelector('.bmi-indicator');
  if (!indicator) return;

  // Position indicator relative to its parent
  indicator.style.left = position + '%';
}

// rank-bar 포인터 위치를 계산/갱신하는 유틸
function updateRankPointer(rankBars, bucket) {
  if (!rankBars) return;
  try {
    const bars = rankBars.querySelectorAll('.bars span');
    const idx = Math.max(0, Math.min(bars.length - 1, bucket - 1));
    const oldPointer = rankBars.querySelector('.rank-pointer');

    // 포인터가 없다면 생성
    let pointer = oldPointer;
    if (!pointer) {
      pointer = document.createElement('div');
      pointer.className = 'rank-pointer';
      pointer.textContent = '▼';
      pointer.style.position = 'absolute';
      pointer.style.fontSize = '14px';
      pointer.style.pointerEvents = 'none';
      pointer.style.color = '#1f3c88';
      pointer.style.zIndex = '999';
      // ensure parent is positioned
      if (getComputedStyle(rankBars).position === 'static') rankBars.style.position = 'relative';
      rankBars.appendChild(pointer);
    }

    if (!bars || !bars[idx]) {
      pointer.style.display = 'none';
      return;
    }

    // 하이라이트 적용
    bars.forEach(s => s.classList.remove('active-rank'));
    bars[idx].classList.add('active-rank');

    // 위치 계산: bars[idx]의 bounding rect을 사용해서 rankBars 내부 좌표로 변환
    const barRect = bars[idx].getBoundingClientRect();
    const containerRect = rankBars.getBoundingClientRect();
    const left = (barRect.left - containerRect.left) + (barRect.width / 2);
    const top = (barRect.top - containerRect.top) - 20; // 20px 위에 포인터

    pointer.style.left = left + 'px';
    pointer.style.top = top + 'px';
    pointer.style.display = 'block';
    pointer.style.transform = 'translateX(-50%)';
  } catch (err) {
    console.warn('updateRankPointer error', err);
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  // 1️⃣ 모든 페이지 HTML 로드
  await Promise.all([
    loadHTML('#page-cover', 'page_cover.html'),
    loadHTML('#page-summary', 'page_summary.html'),
    loadHTML('#page-height', 'page_height.html'),
    loadHTML('#page-weight', 'page_weight.html'),
    loadHTML('#page-bodymass', 'page_bodymass.html'),
    loadHTML('#page-expected-height', 'page_expected_height.html'),
    loadHTML('#page-xray', 'page_xray.html')
  ]);

  // 서버에서 전달된 데이터로 로드된 조각들 채우기
  if (window.REPORT_DATA) {
    populateReportFromData(window.REPORT_DATA);
    // BMI 지표 위치 업데이트
    positionBMIIndicator(window.REPORT_DATA);
    // 차트 모듈 동적 임포트 및 렌더링
    try {
      const [heightMod, weightMod, bmiMod] = await Promise.all([
        import('./charts/heightChart.js'),
        import('./charts/weightChart.js'),
        import('./charts/bmiChart.js')
      ]);
      if (heightMod && typeof heightMod.renderHeightChart === 'function') {
        heightMod.renderHeightChart(window.REPORT_DATA, 'heightChart');
      }
      if (weightMod && typeof weightMod.renderWeightChart === 'function') {
        weightMod.renderWeightChart(window.REPORT_DATA, 'weightChart');
      }
      if (bmiMod && typeof bmiMod.renderBmiChart === 'function') {
        bmiMod.renderBmiChart(window.REPORT_DATA, 'bmiChart');
      }
    } catch (err) {
      console.warn('Failed to load chart modules', err);
    }
    // 요약 rank-bar 업데이트: height_percentile.percentile 값을 1..100에서 1..8 구간으로 매핑
    try {
      const rawPct = getNested(window.REPORT_DATA, 'height_percentile.percentile');
      const pct = (rawPct === null || rawPct === undefined) ? null : parseInt(String(rawPct), 10);
      if (pct !== null && !Number.isNaN(pct)) {
        // 1..100 -> 1..8 (각 구간은 12.5)
        const bucket = Math.min(8, Math.max(1, Math.ceil(pct / 12.5)));

        const rankBars = document.querySelector('.rank-bars');
        if (rankBars) {
          // 기존 rank-* 클래스 제거
          Array.from(rankBars.classList).forEach(c => {
            if (c.startsWith('rank-')) rankBars.classList.remove(c);
          });
          rankBars.classList.add(`rank-${bucket}`);
          // 추가 안전장치: CSS 의사요소가 보이지 않을 경우를 대비해
          // 포인터 엘리먼트를 직접 생성하여 선택된 막대 위에 표시
          // 포인터 위치 업데이트 (더 안정적인 계산 함수 사용)
          updateRankPointer(rankBars, bucket);
        }
      }
    } catch (e) {
      console.warn('Failed to update rank bars:', e);
    }
  }

  // 2️⃣ page-bodymass 전용 초기화
  // 실제 데이터가 있으면 전달, 없으면 기본값 사용
  const obesityRate = window.REPORT_DATA?.weight_info?.obesity_rate || 105.82;
  initBodymassPage(obesityRate);

  initSummaryNavigation();

  // 3️⃣ 모든 page 수집
  const pages = document.querySelectorAll('.page');
  const currentPageEl = document.getElementById('currentPage');
  const totalPageEl = document.getElementById('totalPage');

  const total = pages.length;
  totalPageEl.textContent = total;

  // 4️⃣ 페이지 footer 자동 생성 (n / total)
  pages.forEach((page, index) => {
    let footer = page.querySelector('.page-footer');
    if (index === 0) return; // 커버 페이지는 제외
    if (!footer) {
      footer = document.createElement('div');
      footer.className = 'page-footer';
      page.appendChild(footer);
    }
    footer.textContent = `${index + 1} / ${total}`;
  });

  // 5️⃣ 스크롤 기반 현재 페이지 표시
  window.addEventListener('scroll', () => {
    const scrollPosition = window.pageYOffset + window.innerHeight / 2;

    pages.forEach((page, index) => {
      const pageTop = page.offsetTop;
      const pageBottom = pageTop + page.offsetHeight;

      if (scrollPosition >= pageTop && scrollPosition < pageBottom) {
        currentPageEl.textContent = index + 1;
      }
    });
  });

  // 윈도우 리사이즈 시에도 BMI 지표 재배치
  window.addEventListener('resize', () => {
    if (window.REPORT_DATA) positionBMIIndicator(window.REPORT_DATA);
    // rank pointer 재배치
    try {
      const rawPct = getNested(window.REPORT_DATA, 'height_percentile.percentile');
      const pct = (rawPct === null || rawPct === undefined) ? null : parseInt(String(rawPct), 10);
      if (pct !== null && !Number.isNaN(pct)) {
        const bucket = Math.min(8, Math.max(1, Math.ceil(pct / 12.5)));
        const rankBars = document.querySelector('.rank-bars');
        if (rankBars) updateRankPointer(rankBars, bucket);
      }
    } catch (e) {
      // ignore
    }
  });
});

function initSummaryNavigation() {
  const cards = document.querySelectorAll('.page-hint[data-target]');
  
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const targetId = card.dataset.target;
      const targetPage = document.getElementById(targetId);

      if (targetPage) {
        targetPage.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

document.getElementById('printButton').addEventListener('click', function() {
    window.print();
});

const backBtn = document.getElementById('backToSummaryBtn');

if (backBtn) {
    backBtn.addEventListener('click', function () {

        document.querySelector('.page-summary').scrollIntoView({
            behavior: 'smooth'
        });

    });
}