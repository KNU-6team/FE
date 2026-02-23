"""
Flask 애플리케이션 팩토리
"""
from flask import Flask, render_template, send_from_directory, abort
import os
from flask_cors import CORS
from app.config.settings import DevelopmentConfig, ProductionConfig, get_config

def create_app(config=None):
    """
    Flask 앱 생성 및 초기화
    
    Args:
        config: 설정 클래스 (없으면 환경에 따라 자동 선택)
    
    Returns:
        Flask: Flask 애플리케이션 인스턴스
    """
    # 기존 Flask 인스턴스 생성(주석 처리)
    # app = Flask(__name__)
    # 템플릿과 정적 파일 경로를 프로젝트의 상위 폴더로 지정하여
    # template/report.html 및 static/* 파일을 제공하도록 설정합니다.
    # 상대 경로 방식은 작업 디렉터리에 따라 TemplateNotFound를 일으킬 수 있으므로
    # 프로젝트 루트를 기준으로 한 절대 경로로 지정합니다.
    # app = Flask(__name__, static_folder='../static', template_folder='../template')

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(base_dir, 'template')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    # 설정 적용
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # CORS 설정
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 라우트 등록
    from app.routes.report import report_bp
    app.register_blueprint(report_bp)
    
    # 에러 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'message': 'Resource not found',
            'data': None
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'success': False,
            'message': 'Internal server error',
            'data': None
        }, 500
    
    # 기존 루트 엔드포인트는 주석 처리하고, 필요 시 아래 JSON 응답을 복원하세요.
    # @app.route('/', methods=['GET'])
    # def index():
    #     return {
    #         'success': True,
    #         'message': 'Bone Age Report Backend API',
    #         'version': '1.0.0',
    #         'endpoints': {
    #             'health': '/api/reports/health',
    #             'get_report': '/api/reports/patient/<patient_code>',
    #             'get_history': '/api/reports/patient/<patient_id>/history',
    #             'get_all_patients': '/api/reports/patients',
    #             'search_patients': '/api/reports/patients/search?keyword=<keyword>'
    #         }
    #     }, 200

    # 기존 간단 렌더 핸들러(원본) - 필요 시 복원용으로 남겨둡니다.
    @app.route('/', methods=['GET'])
    def index():
        # 기본 동작: 쿼리 파라미터로 `patient_code`가 없으면 시작 페이지(start.html)를 보여줍니다.
        # (기존 report 렌더 로직은 보존되어 있으며, patient_code가 주어졌을 때 report.html을 렌더합니다.)
        from flask import request

        patient_code = request.args.get('patient_code')
        birth_date = request.args.get('birth_date')

        # 1. 아무 값도 없으면 시작 페이지
        if not patient_code and not birth_date:
            return render_template('start.html')

        # 2. 하나라도 없으면 에러
        if not patient_code or not birth_date:
            return render_template('error.html')
        # patient_code가 있으면 기존 로직대로 리포트 조회 후 report.html로 렌더
        try:
            from app.services.report_service import ReportService

            report = ReportService.get_patient_report(patient_code)

            # patient_code 없음
            if not report:
                return render_template('error.html')

            patient_birth = report.get('patient', {}).get('birth_date')

            if not patient_birth:
                return render_template('error.html')

            expected = f"{birth_date[0:4]}-{birth_date[4:6]}-{birth_date[6:8]}"

            # birth_date 틀림
            if str(patient_birth) != expected:
                return render_template('error.html')

            # 성공
            return render_template('report.html', report=report)

        except Exception as e:

            print("ERROR:", e)

            return render_template('error.html')

    # report.js에서 fetch로 요청하는 개별 페이지 조각들(page_cover.html 등)을
    # 루트 경로에서 직접 요청할 수 있도록 처리합니다. 이 라우트는
    # 요청된 경로가 template_dir 내부에 존재하는 .html 파일이면 해당 파일을 반환합니다.
    @app.route('/<path:filename>', methods=['GET'])
    def serve_template_fragment(filename):
        # API 경로는 /api/ 로 시작하므로 무시합니다.
        if filename.startswith('api/'):
            return abort(404)

        # .html 파일만 처리
        if not filename.endswith('.html'):
            return abort(404)

        file_path = os.path.join(template_dir, filename)
        if os.path.exists(file_path):
            return send_from_directory(template_dir, filename)

        return abort(404)
    
    return app
