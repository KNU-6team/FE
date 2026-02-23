/**
 * 신장 백분위수 차트 렌더러
 * Chart.js를 사용해 3-18세 성장곡선을 그립니다.
 * 성별별 백분위 데이터와 현재 환자의 위치를 표시합니다.
 */

import { ages as maleAges, maleHeightPercentiles } from '../data/maleHeightPercentile.js';
import { ages as femaleAges, femaleHeightPercentiles } from '../data/femaleHeightPercentile.js';

/**
 * 나이 정보에서 소수점 연령으로 변환
 * 예: "11세 5개월" → 11.42
 */
function parseAgeToNumeric(ageStr) {
  if (typeof ageStr === 'number') return ageStr;
  if (!ageStr) return null;
  
  // "11세 5개월" 형식 파싱
  const match = ageStr.match(/(\d+)세\s*(\d+)개월/);
  if (match) {
    const years = parseInt(match[1], 10);
    const months = parseInt(match[2], 10);
    return years + months / 12;
  }
  
  return parseFloat(ageStr);
}

/**
 * 성별에 따라 적절한 데이터 선택
 */
function getPercentileData(gender) {
  const isMale = gender && (gender === 'M' || gender === '남자');
  return isMale ? maleHeightPercentiles : femaleHeightPercentiles;
}

/**
 * Chart.js 데이터셋 생성 (백분위 곡선)
 */
function createPercentileDatasets(percentileData, ages) {
  const percentiles = [
    { key: 'p3', label: '3rd', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 },
    { key: 'p10', label: '10th', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 },
    { key: 'p25', label: '25th', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 },
    { key: 'p50', label: '50th (Median)', color: 'rgba(0, 0, 0, 0.9)', borderWidth: 3 },
    { key: 'p75', label: '75th', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 },
    { key: 'p90', label: '90th', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 },
    { key: 'p97', label: '97th', color: 'rgba(173, 216, 230, 0.8)', borderWidth: 1.5 }
  ];

  return percentiles.map(p => ({
    label: p.label,
    data: ages.map((_, idx) => ({
      x: ages[idx],
      y: percentileData[p.key][idx]
    })),
    borderColor: p.color,
    backgroundColor: 'transparent',
    fill: false,
    tension: 0.4, // 부드러운 커브
    pointRadius: 0, // 포인트 숨김 (곡선만 표시)
    borderWidth: p.borderWidth,
    showLine: true
  }));
}

/**
 * 환자 포인트 데이터셋 생성
 */
function createPatientDataset(ageNumeric, height) {
  return {
    label: 'Patient',
    data: [{ x: ageNumeric, y: height }],
    pointBackgroundColor: '#000',
    pointBorderColor: 'rgba(255, 255, 255, 1)',
    pointBorderWidth: 2,
    pointRadius: 6,
    showLine: false,
    fill: false
  };
}

/**
 * Chart.js scatter 차트 구성 객체 생성
 */
function createChartConfig(datasets, ages) {
  return {
    type: 'scatter',
    data: {
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          display: true,
          position: 'right',
          labels: {
            usePointStyle: true,   // ⭐ 이거 핵심
            pointStyle: 'line',     // 선 모양으로 표시
            padding: 15,
            font: {
              size: 15
            }
          }
        },
        tooltip: {
          enabled: true,
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || '';
              const x = context.parsed.x.toFixed(1);
              const y = context.parsed.y.toFixed(1);
              return `${label}: ${x}y, ${y}cm`;
            }
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          title: {
            display: true,
            text: '나이 (년)',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          min: 3,
          max: 18,
          grid: {
            display: true,
            color: 'rgba(200, 200, 200, 0.2)'
          }
        },
        y: {
          title: {
            display: true,
            text: '키 (cm)',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          min: 85,
          max: 200,
          grid: {
            display: true,
            color: 'rgba(200, 200, 200, 0.2)'
          }
        }
      }
    }
  };
}

/**
 * 높이 백분위수 차트 렌더
 * @param {Object} data - 환자 데이터 (patient, bone_age, report 포함)
 * @param {string} canvasId - 캔버스 ID
 */
export function renderHeightChart(data, canvasId = 'heightChart') {
  if (!data) {
    console.warn('renderHeightChart: No data provided');
    return;
  }

  const canvas = document.getElementById(canvasId);
  if (!canvas) {
    console.warn(`renderHeightChart: Canvas with id "${canvasId}" not found`);
    return;
  }

  // Canvas의 실제 해상도를 부모 컨테이너에 맞게 설정
  const parent = canvas.parentElement;
  if (parent) {
    canvas.width = parent.offsetWidth;
    canvas.height = parent.offsetHeight;
  }

  // 환자 데이터 추출
  const gender = data.patient?.gender;
  const ageStr = data.bone_age?.chronological_age;
  const height = parseFloat(data.bone_age?.current_height);

  if (!ageStr || isNaN(height)) {
    console.warn('renderHeightChart: Missing or invalid patient data');
    return;
  }

  const ageNumeric = parseAgeToNumeric(ageStr);
  if (ageNumeric === null) {
    console.warn('renderHeightChart: Could not parse age');
    return;
  }

  // 성별별 데이터 선택
  const percentileData = getPercentileData(gender);
  const ages = gender === 'M' || gender === '남자' ? maleAges : femaleAges;

  // 데이터셋 생성: 백분위 곡선 + 환자 포인트
  const percentileDatasets = createPercentileDatasets(percentileData, ages);
  const patientDataset = createPatientDataset(ageNumeric, height);
  const allDatasets = [...percentileDatasets, patientDataset];

  // 차트 구성
  const chartConfig = createChartConfig(allDatasets, ages);

  // 기존 차트 인스턴스가 있으면 제거
  if (window._heightChartInstance) {
    window._heightChartInstance.destroy();
  }

  // 새 차트 생성
  const ctx = canvas.getContext('2d');
  window._heightChartInstance = new Chart(ctx, chartConfig);
}

export default { renderHeightChart };
