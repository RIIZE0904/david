# Python의 대표 웹 프레임워크 3가지와 특성

## 1. Django

- **설명**: Python 기반의 고수준 웹 프레임워크로, 신속한 개발과 깔끔한 디자인을 목표로 함
- **특징**:
  - `MTV(Model-Template-View)` 아키텍처
  - 관리자 페이지, ORM, 인증 시스템 등 다양한 기능을 내장
  - 보안 기능 탑재 (SQL Injection, CSRF, XSS 방지 등)
  - 대규모 프로젝트에 적합

## 2. Flask

- **설명**: 마이크로 웹 프레임워크로, 필요한 기능만 최소한으로 제공
- **특징**:
  - 가볍고 유연하며 확장성이 뛰어남
  - Jinja2 템플릿 엔진 사용
  - 기본적으로 ORM, 인증 같은 기능은 포함하지 않으며, 확장으로 구현 가능
  - 소규모 프로젝트나 API 서버에 적합

## 3. FastAPI

- **설명**: 최신 Python 표준인 `Pydantic`과 `Type Hints`를 활용하는 고성능 웹 프레임워크
- **특징**:
  - 비동기(Async) 지원으로 높은 처리 성능
  - 자동 Swagger 문서 생성
  - 입력 데이터 검증이 편리함
  - RESTful API 개발에 최적화

---

## 참고

- Django: https://www.djangoproject.com/
- Flask: https://flask.palletsprojects.com/
- FastAPI: https://fastapi.tiangolo.com/