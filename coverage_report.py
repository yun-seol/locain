import coverage
import sys
from datetime import datetime
import os

def generate_coverage_report():
    print(f"\n커버리지 리포트 생성 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 커버리지 측정 시작
    cov = coverage.Coverage(
        branch=True,
        source=['app'],
        omit=['tests/*', '*/__init__.py']
    )
    cov.start()
    
    # pytest 실행
    import pytest
    pytest.main(['tests/'])
    
    # 커버리지 측정 종료
    cov.stop()
    
    # HTML 리포트 생성
    print("\nHTML 리포트 생성 중...")
    cov.html_report(directory='coverage_html')
    
    # XML 리포트 생성
    print("XML 리포트 생성 중...")
    cov.xml_report(outfile='coverage.xml')
    
    # 터미널에 요약 출력
    print("\n커버리지 요약:")
    print("=" * 50)
    cov.report()
    
    print(f"\n커버리지 리포트 생성 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("HTML 리포트: coverage_html/index.html")
    print("XML 리포트: coverage.xml")

if __name__ == "__main__":
    generate_coverage_report() 