"""
데이터베이스 테이블 모델 정의
"""

class Patient:
    """환자 테이블"""
    TABLE_NAME = 'patients'
    COLUMNS = [
        'id',
        'patient_code',
        'name',
        'gender',
        'birth_date',
        'created_at',
        'updated_at'
    ]

class Report:
    """검사 보고서 테이블"""
    TABLE_NAME = 'reports'
    COLUMNS = [
        'id',
        'patient_id',
        'exam_date',
        'requested_doctor',
        'status',
        'created_at',
        'updated_at'
    ]

class BoneAge:
    """골연령 정보 테이블"""
    TABLE_NAME = 'bone_ages'
    COLUMNS = [
        'id',
        'report_id',
        'chronological_age',  # 실제 나이
        'bone_age',            # 골연령
        'age_difference',      # 나이 차이
        'current_height',      # 현재 키
        'predicted_height_ai', # AI 기반 예측 키
        'created_at',
        'updated_at'
    ]

class GeneticInfo:
    """유전 정보 테이블"""
    TABLE_NAME = 'genetic_info'
    COLUMNS = [
        'id',
        'report_id',
        'father_height',         # 아버지 키
        'mother_height',         # 어머니 키
        'predicted_height_genetic', # 유전적 예측 키
        'created_at',
        'updated_at'
    ]

class HeightPercentile:
    """키 백분위 테이블"""
    TABLE_NAME = 'height_percentiles'
    COLUMNS = [
        'id',
        'report_id',
        'gender',
        'percentile',      # 백분위 순위
        'percentile_rank', # 상위/하위 퍼센트
        'assessment',      # 저신장/정상/고신장
        'created_at',
        'updated_at'
    ]

class WeightInfo:
    """체중 정보 테이블"""
    TABLE_NAME = 'weight_info'
    COLUMNS = [
        'id',
        'report_id',
        'weight',
        'percentile',      # 백분위 순위
        'bmi',
        'bmi_category',    # 저체중/정상/과체중/비만
        'obesity_rate',    # 비만도(%) 또는 비만율
        'obesity_grade',   # 비만 등급(예: 경도, 중등도)
        'created_at',
        'updated_at'
    ]

class XRayAnalysis:
    """엑스레이 분석 정보 테이블"""
    TABLE_NAME = 'xray_analysis'
    COLUMNS = [
        'id',
        'report_id',
        'image_path',
        'analysis_result',
        'confidence_score',
        'created_at',
        'updated_at'
    ]

# SQL 쿼리 템플릿
QUERIES = {
    'get_patient_report': """
        SELECT 
            p.id, p.patient_code, p.name, p.gender, p.birth_date,
            r.id as report_id, r.exam_date, r.requested_doctor, r.status,
            ba.chronological_age, ba.bone_age, ba.age_difference, ba.current_height, ba.predicted_height_ai,
            gi.father_height, gi.mother_height, gi.predicted_height_genetic,
            hp.percentile, hp.percentile_rank, hp.assessment,
            wi.weight, wi.percentile as weight_percentile, wi.bmi, wi.bmi_category, wi.obesity_rate, wi.obesity_grade,
            xa.image_path, xa.analysis_result, xa.confidence_score
        FROM patients p
        LEFT JOIN reports r ON p.id = r.patient_id
        LEFT JOIN bone_ages ba ON r.id = ba.report_id
        LEFT JOIN genetic_info gi ON r.id = gi.report_id
        LEFT JOIN height_percentiles hp ON r.id = hp.report_id
        LEFT JOIN weight_info wi ON r.id = wi.report_id
        LEFT JOIN xray_analysis xa ON r.id = xa.report_id
        WHERE p.patient_code = %s
        ORDER BY r.exam_date DESC
        LIMIT 1
    """,
    
    'get_patient_history': """
        SELECT 
            r.id as report_id, r.exam_date, r.status,
            ba.chronological_age, ba.bone_age, ba.current_height, ba.predicted_height_ai
        FROM reports r
        LEFT JOIN bone_ages ba ON r.id = ba.report_id
        WHERE r.patient_id = %s
        ORDER BY r.exam_date DESC
    """,
    
    'get_all_patients': """
        SELECT 
            p.id, p.patient_code, p.name, p.gender, p.birth_date,
            MAX(r.exam_date) as latest_exam_date,
            COUNT(r.id) as total_reports
        FROM patients p
        LEFT JOIN reports r ON p.id = r.patient_id
        GROUP BY p.id
        ORDER BY MAX(r.exam_date) DESC
    """
}
