"""
비즈니스 로직 레이어 - SQL 쿼리 실행 및 데이터 처리
"""
from app.db.database import Database
from app.db.models import QUERIES
from app.schemas.report_schema import full_report_schema, patient_list_schema

class ReportService:
    """보고서 데이터 조회 및 처리"""
    
    @staticmethod
    def get_patient_report(patient_code):
        """
        환자 코드로 최신 보고서 조회
        
        Args:
            patient_code: 환자 코드
            
        Returns:
            dict: 전체 보고서 데이터
        """
        try:
            result = Database.fetch_one(QUERIES['get_patient_report'], (patient_code,))
            
            if not result:
                return None
            
            return full_report_schema(result)
        
        except Exception as e:
            print(f"Error in get_patient_report: {e}")
            raise
    
    @staticmethod
    def get_patient_history(patient_id):
        """
        환자 ID로 검사 이력 조회
        
        Args:
            patient_id: 환자 ID
            
        Returns:
            list: 검사 이력 리스트
        """
        try:
            results = Database.fetch_all(QUERIES['get_patient_history'], (patient_id,))
            
            if not results:
                return []
            
            return results
        
        except Exception as e:
            print(f"Error in get_patient_history: {e}")
            raise
    
    @staticmethod
    def get_all_patients():
        """
        모든 환자 목록 조회
        
        Returns:
            list: 환자 목록
        """
        try:
            results = Database.fetch_all(QUERIES['get_all_patients'])
            
            if not results:
                return []
            
            return [patient_list_schema(patient) for patient in results]
        
        except Exception as e:
            print(f"Error in get_all_patients: {e}")
            raise
    
    @staticmethod
    def search_patients(keyword):
        """
        환자명 또는 코드로 검색
        
        Args:
            keyword: 검색 키워드
            
        Returns:
            list: 검색 결과
        """
        try:
            query = """
                SELECT 
                    p.id, p.patient_code, p.name, p.gender, p.birth_date,
                    MAX(r.exam_date) as latest_exam_date,
                    COUNT(r.id) as total_reports
                FROM patients p
                LEFT JOIN reports r ON p.id = r.patient_id
                WHERE p.patient_code LIKE %s OR p.name LIKE %s
                GROUP BY p.id
                ORDER BY p.name ASC
            """
            search_keyword = f"%{keyword}%"
            results = Database.fetch_all(query, (search_keyword, search_keyword))
            
            if not results:
                return []
            
            return [patient_list_schema(patient) for patient in results]
        
        except Exception as e:
            print(f"Error in search_patients: {e}")
            raise
