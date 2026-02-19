"""
Flask 서버 실행 파일
"""
import os
from app import create_app

if __name__ == '__main__':
    # 환경변수 설정
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_APP', 'app.main')
    
    # Flask 앱 생성 및 실행
    app = create_app()
    
    print("=" * 50)
    print("🚀 Bone Age Report Backend Server")
    print("=" * 50)
    print("Server running on http://localhost:5000")
    print("API Documentation: http://localhost:5000")
    print("=" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
