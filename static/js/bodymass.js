/* =========================
   BMI 페이지 초기화
========================= */

function initBodymassPage(bmiPercent) {
  const indicator = document.querySelector('.bmi-indicator');
  if (!indicator) return; // BMI 페이지 아닐 경우 종료

  const position = calculateBmiPosition(bmiPercent);
  indicator.style.left = position + '%';
}

function calculateBmiPosition(bmi) {
  // bmi = 비만도(%)
  let position = 0;

  if (bmi <= 90) {
    // 저체중 (0 ~ 90) → 0% ~ 35%
    position = (bmi / 90) * 35;

  } else if (bmi <= 120) {
    // 정상 (90 ~ 120) → 35% ~ 60%
    position = 35 + ((bmi - 90) / 30) * 25;

  } else if (bmi <= 130) {
    // 경도비만 (120 ~ 130) → 60% ~ 70%
    position = 60 + ((bmi - 120) / 10) * 10;

  } else if (bmi <= 150) {
    // 중등도비만 (130 ~ 150) → 70% ~ 90%
    position = 70 + ((bmi - 130) / 20) * 20;

  } else {
    // 고도비만 (150 이상) → 90% ~ 100%
    position = 90 + Math.min((bmi - 150) / 20 * 10, 10);
  }

  return Math.min(Math.max(position, 0), 100);
}

