"""
API 엔드포인트 - 보고서 관련 라우팅
"""
from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/api/reports')

@report_bp.route('/patient/<patient_code>', methods=['GET'])
def get_patient_report(patient_code):
    """
    환자 코드로 최신 보고서 조회
    
    GET /api/reports/patient/{patient_code}
    
    Response:
        {
            "success": true,
            "data": {
                "patient": {...},
                "report": {...},
                "bone_age": {...},
                "genetic_info": {...},
                "height_percentile": {...},
                "weight_info": {...},
                "xray": {...}
            }
        }
    """
    try:
        report = ReportService.get_patient_report(patient_code)
        
        if not report:
            return jsonify({
                'success': False,
                'message': f'Patient with code {patient_code} not found',
                'data': None
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Report retrieved successfully',
            'data': report
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving report: {str(e)}',
            'data': None
        }), 500

@report_bp.route('/patient/<int:patient_id>/history', methods=['GET'])
def get_patient_history(patient_id):
    """
    환자 ID로 검사 이력 조회
    
    GET /api/reports/patient/{patient_id}/history
    
    Response:
        {
            "success": true,
            "data": [
                {
                    "report_id": 1,
                    "exam_date": "2024-01-15",
                    "status": "completed",
                    ...
                }
            ]
        }
    """
    try:
        history = ReportService.get_patient_history(patient_id)
        
        return jsonify({
            'success': True,
            'message': 'History retrieved successfully',
            'data': history
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving history: {str(e)}',
            'data': None
        }), 500

@report_bp.route('/patients', methods=['GET'])
def get_all_patients():
    """
    모든 환자 목록 조회 (페이징 지원)
    
    GET /api/reports/patients?page=1&per_page=20
    
    Query Parameters:
        - page: 페이지 번호 (기본값: 1)
        - per_page: 페이지당 항목 수 (기본값: 20)
    
    Response:
        {
            "success": true,
            "data": [...],
            "total": 100,
            "page": 1,
            "per_page": 20
        }
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        patients = ReportService.get_all_patients()
        
        # 페이징 처리
        start = (page - 1) * per_page
        end = start + per_page
        paginated_patients = patients[start:end]
        
        return jsonify({
            'success': True,
            'message': 'Patients retrieved successfully',
            'data': paginated_patients,
            'total': len(patients),
            'page': page,
            'per_page': per_page
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving patients: {str(e)}',
            'data': None
        }), 500

@report_bp.route('/patients/search', methods=['GET'])
def search_patients():
    """
    환자명 또는 코드로 검색
    
    GET /api/reports/patients/search?keyword=홍길동
    
    Query Parameters:
        - keyword: 검색 키워드 (필수)
    
    Response:
        {
            "success": true,
            "data": [...]
        }
    """
    try:
        keyword = request.args.get('keyword', '', type=str).strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': 'Keyword is required',
                'data': None
            }), 400
        
        results = ReportService.search_patients(keyword)
        
        return jsonify({
            'success': True,
            'message': 'Search completed successfully',
            'data': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching patients: {str(e)}',
            'data': None
        }), 500

@report_bp.route('/health', methods=['GET'])
def health_check():
    """
    헬스 체크
    
    GET /api/reports/health
    """
    return jsonify({
        'success': True,
        'message': 'Report service is running',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }), 200
