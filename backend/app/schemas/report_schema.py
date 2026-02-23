"""
응답 데이터 구조 정의 (Serialization용)
"""
from app.utils import convert_decimal_age_to_korean, convert_gender_to_korean

def patient_schema(patient):
    """환자 정보 스키마"""
    return {
        'id': patient.get('id'),
        'patient_code': patient.get('patient_code'),
        'name': patient.get('name'),
        'gender': convert_gender_to_korean(patient.get('gender')),
        'birth_date': str(patient.get('birth_date')) if patient.get('birth_date') else None,
    }

def report_schema(report):
    """보고서 기본 정보 스키마"""
    return {
        'report_id': report.get('report_id'),
        'exam_date': str(report.get('exam_date')) if report.get('exam_date') else None,
        'requested_doctor': report.get('requested_doctor'),
        'status': report.get('status'),
    }

def bone_age_schema(report):
    """골연령 정보 스키마"""
    return {
        'chronological_age': convert_decimal_age_to_korean(report.get('chronological_age')),
        'bone_age': convert_decimal_age_to_korean(report.get('bone_age')),
        'age_difference': convert_decimal_age_to_korean(report.get('age_difference')),
        'current_height': report.get('current_height'),
        'predicted_height_ai': report.get('predicted_height_ai'),
    }

def genetic_info_schema(report):
    """유전 정보 스키마"""
    return {
        'father_height': report.get('father_height'),
        'mother_height': report.get('mother_height'),
        'predicted_height_genetic': report.get('predicted_height_genetic'),
    }

def height_percentile_schema(report):
    """키 백분위 스키마"""
    return {
        'percentile': report.get('percentile'),
        'percentile_rank': report.get('percentile_rank'),
        'assessment': report.get('assessment'),
        'gender': convert_gender_to_korean(report.get('gender')),
    }

def weight_info_schema(report):
    """체중 정보 스키마"""
    return {
        'weight': report.get('weight'),
        'percentile': report.get('weight_percentile'),
        'bmi': report.get('bmi'),
        'bmi_category': report.get('bmi_category'),
        'obesity_rate': report.get('obesity_rate'),
        'obesity_grade': report.get('obesity_grade'),
    }

def xray_schema(report):
    """엑스레이 분석 스키마"""
    return {
        'image_path': report.get('image_path'),
        'analysis_result': report.get('analysis_result'),
        'confidence_score': report.get('confidence_score'),
    }

def full_report_schema(report):
    """전체 보고서 스키마 (모든 정보 포함)"""
    return {
        'patient': patient_schema(report),
        'report': report_schema(report),
        'bone_age': bone_age_schema(report),
        'genetic_info': genetic_info_schema(report),
        'height_percentile': height_percentile_schema(report),
        'weight_info': weight_info_schema(report),
        'xray': xray_schema(report),
    }

def patient_list_schema(patient):
    """환자 목록 스키마"""
    return {
        'id': patient.get('id'),
        'patient_code': patient.get('patient_code'),
        'name': patient.get('name'),
        'gender': convert_gender_to_korean(patient.get('gender')),
        'birth_date': str(patient.get('birth_date')) if patient.get('birth_date') else None,
        'latest_exam_date': str(patient.get('latest_exam_date')) if patient.get('latest_exam_date') else None,
        'total_reports': patient.get('total_reports', 0),
    }
