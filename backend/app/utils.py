"""
유틸리티 함수 모음
"""
from datetime import datetime

def calculate_age_months(birth_date):
    """
    생년월일로부터 현재 나이를 월 단위로 계산
    
    Args:
        birth_date: datetime 객체 또는 YYYY-MM-DD 형식의 문자열
    
    Returns:
        int: 나이 (개월 단위)
    """
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = datetime.now().date()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    return months

def format_age_text(months):
    """
    월 단위 나이를 '세' 및 '개월' 형식으로 변환
    
    Args:
        months: 나이 (개월 단위)
    
    Returns:
        str: 예) "11세 9개월"
    """
    years = months // 12
    remaining_months = months % 12
    return f"{years}세 {remaining_months}개월"

def calculate_bmi(weight, height_m):
    """
    BMI 계산
    
    Args:
        weight: 체중 (kg)
        height_m: 키 (m)
    
    Returns:
        float: BMI
    """
    if height_m == 0:
        return 0
    return round(weight / (height_m ** 2), 2)

def classify_bmi(bmi):
    """
    BMI 분류
    
    Args:
        bmi: BMI 값
    
    Returns:
        str: 저체중/정상/과체중/비만
    """
    if bmi < 18.5:
        return '저체중'
    elif bmi < 25:
        return '정상'
    elif bmi < 30:
        return '과체중'
    else:
        return '비만'

def classify_height(percentile):
    """
    키 분류 (백분위 기준)
    
    Args:
        percentile: 백분위 순위 (1-100)
    
    Returns:
        str: 저신장/정상/고신장
    """
    if percentile <= 5:
        return '저신장'
    elif percentile <= 95:
        return '정상'
    else:
        return '고신장'

def format_percentile_text(percentile):
    """
    백분위를 텍스트로 변환
    
    Args:
        percentile: 백분위 순위 (1-100)
    
    Returns:
        str: 예) "상위 99%" 또는 "하위 5%"
    """
    upper_percent = 100 - percentile + 1
    if upper_percent > 50:
        lower_percent = 100 - upper_percent + 1
        return f"하위 {lower_percent}%"
    else:
        return f"상위 {upper_percent}%"

def convert_decimal_age_to_korean(decimal_age):
    """
    소수점 나이를 "n세 n개월" 형식으로 변환
    
    예: 11.75 → "11세 9개월"
    예: 2.5 → "2세 6개월"
    
    Args:
        decimal_age: 소수점 형식의 나이 (float, int, 또는 str)
        
    Returns:
        str: "n세 n개월" 형식의 문자열, 또는 None
    """
    if decimal_age is None:
        return None
    
    # 문자열인 경우 처리
    if isinstance(decimal_age, str):
        # 이미 "n세 n개월" 형식이면 그대로 반환
        if '세' in decimal_age or '년' in decimal_age:
            return decimal_age
        try:
            decimal_age = float(decimal_age)
        except ValueError:
            return decimal_age
    
    decimal_age = float(decimal_age)
    years = int(decimal_age)
    months = round((decimal_age - years) * 12)
    
    # 12개월이 되면 년도에 포함
    if months == 12:
        years += 1
        months = 0
    
    return f"{years}세 {months}개월"

def convert_gender_to_korean(gender):
    """
    성별 코드를 한글로 변환
    
    예: 'M' → '남자'
    예: 'F' → '여자'
    
    Args:
        gender: 성별 코드 ('M' 또는 'F')
        
    Returns:
        str: '남자' 또는 '여자', 또는 원본값
    """
    if gender is None:
        return None
    
    gender_map = {
        'M': '남자',
        'F': '여자',
        'm': '남자',
        'f': '여자'
    }
    
    return gender_map.get(gender, gender)
