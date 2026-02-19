-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS bone_report;
USE bone_report;

-- 1. 환자 테이블
CREATE TABLE IF NOT EXISTS patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_code VARCHAR(50) UNIQUE NOT NULL COMMENT '환자 코드',
    name VARCHAR(100) NOT NULL COMMENT '환자 이름',
    gender ENUM('M', 'F') NOT NULL COMMENT '성별',
    birth_date DATE NOT NULL COMMENT '생년월일',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_patient_code (patient_code),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. 검사 보고서 테이블
CREATE TABLE IF NOT EXISTS reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    exam_date DATE NOT NULL COMMENT '검사 일자',
    requested_doctor VARCHAR(100) COMMENT '의뢰 의사',
    status ENUM('pending', 'in_progress', 'completed', 'failed') DEFAULT 'pending' COMMENT '검사 상태',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_exam_date (exam_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. 골연령 정보 테이블
CREATE TABLE IF NOT EXISTS bone_ages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    chronological_age VARCHAR(50) COMMENT '실제 나이 (예: 11세 9개월)',
    bone_age VARCHAR(50) COMMENT '골연령 (예: 13세 5개월)',
    age_difference VARCHAR(50) COMMENT '나이 차이 (예: 1세 8개월)',
    current_height DECIMAL(5, 2) COMMENT '현재 키 (cm)',
    predicted_height_ai DECIMAL(5, 2) COMMENT 'AI 기반 예측 키 (cm)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. 유전 정보 테이블
CREATE TABLE IF NOT EXISTS genetic_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    father_height DECIMAL(5, 2) COMMENT '아버지 키 (cm)',
    mother_height DECIMAL(5, 2) COMMENT '어머니 키 (cm)',
    predicted_height_genetic DECIMAL(5, 2) COMMENT '유전적 예측 키 (cm)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. 키 백분위 테이블
CREATE TABLE IF NOT EXISTS height_percentiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    gender ENUM('M', 'F') NOT NULL COMMENT '성별',
    percentile INT COMMENT '백분위 순위 (1-100)',
    percentile_rank VARCHAR(50) COMMENT '상위/하위 퍼센트',
    assessment VARCHAR(50) COMMENT '저신장/정상/고신장',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. 체중 정보 테이블
CREATE TABLE IF NOT EXISTS weight_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    weight DECIMAL(5, 2) COMMENT '체중 (kg)',
    percentile INT COMMENT '백분위 순위',
    bmi DECIMAL(5, 2) COMMENT '체질량 지수',
    bmi_category VARCHAR(50) COMMENT '저체중/정상/과체중/비만',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. 엑스레이 분석 정보 테이블
CREATE TABLE IF NOT EXISTS xray_analysis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    image_path VARCHAR(255) COMMENT 'X-Ray 이미지 경로',
    analysis_result TEXT COMMENT '분석 결과',
    confidence_score DECIMAL(3, 2) COMMENT '신뢰도 점수 (0-1)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 샘플 데이터 삽입
INSERT INTO patients (patient_code, name, gender, birth_date) VALUES
('2024-001234', '홍길동', 'M', '2012-05-15'),
('2096361', '허지효', 'M', '2011-06-07'),
('2024-005678', '김철수', 'M', '2010-03-21'),
('2024-009012', '이영희', 'F', '2013-08-10');

INSERT INTO reports (patient_id, exam_date, requested_doctor, status) VALUES
(1, '2024-11-20', '김영희', 'completed'),
(2, '2023-03-24', '박민수', 'completed'),
(3, '2024-10-15', '이순신', 'completed'),
(4, '2024-11-18', '김영희', 'completed');

INSERT INTO bone_ages (report_id, chronological_age, bone_age, age_difference, current_height, predicted_height_ai) VALUES
(1, '11세 9개월', '13세 5개월', '1세 8개월', 107.8, 123.2),
(2, '11세 9개월', '13세 5개월', '1세 8개월', 107.8, 123.2),
(3, '12세 2개월', '13세 10개월', '1세 8개월', 110.5, 128.5),
(4, '10세 6개월', '12세 4개월', '1세 10개월', 105.2, 120.8);

INSERT INTO genetic_info (report_id, father_height, mother_height, predicted_height_genetic) VALUES
(1, 170.0, 160.0, 171.5),
(2, 170.0, 160.0, 171.5),
(3, 175.5, 162.0, 176.2),
(4, 168.0, 158.5, 169.8);

INSERT INTO height_percentiles (report_id, gender, percentile, percentile_rank, assessment) VALUES
(1, 'M', 1, '상위 99%', '저신장'),
(2, 'M', 1, '상위 99%', '저신장'),
(3, 'M', 5, '상위 95%', '정상'),
(4, 'F', 10, '상위 90%', '정상');

INSERT INTO weight_info (report_id, weight, percentile, bmi, bmi_category) VALUES
(1, 22.5, 1, 17.21, '저체중'),
(2, 22.5, 1, 17.21, '저체중'),
(3, 26.8, 5, 18.52, '정상'),
(4, 21.3, 3, 17.85, '저체중');

INSERT INTO xray_analysis (report_id, image_path, analysis_result, confidence_score) VALUES
(1, '/static/image/xray_001.jpg', '좌측 손 엑스레이 분석 완료', 0.95),
(2, '/static/image/xray_002.jpg', '좌측 손 엑스레이 분석 완료', 0.94),
(3, '/static/image/xray_003.jpg', '좌측 손 엑스레이 분석 완료', 0.96),
(4, '/static/image/xray_004.jpg', '좌측 손 엑스레이 분석 완료', 0.93);
