# DockerHub를 사용하는 이유

- **이미지 저장 및 공유**: DockerHub는 컨테이너 이미지를 저장하고, 전 세계 개발자와 쉽게 공유할 수 있는 공식 퍼블릭 레지스트리입니다.
- **배포 자동화**: CI/CD 파이프라인에서 이미지를 자동으로 빌드·푸시·배포할 수 있습니다.
- **버전 관리**: 이미지에 태그를 붙여 여러 버전을 관리할 수 있습니다.
- **공식 이미지 제공**: 다양한 오픈소스 및 상용 소프트웨어의 공식 이미지를 손쉽게 사용할 수 있습니다.
- **접근성**: 퍼블릭/프라이빗 저장소를 지원하며, 어디서든 이미지를 pull하여 사용할 수 있습니다.

---

# Container Registry 종류 3가지

1. **DockerHub**
   - 가장 널리 사용되는 퍼블릭 컨테이너 레지스트리
   - 공식 이미지 및 커뮤니티 이미지 제공

2. **GitHub Container Registry (GHCR)**
   - GitHub에서 제공하는 컨테이너 이미지 저장소
   - GitHub Actions 등과 연동이 쉬움

3. **Google Container Registry (GCR)**
   - Google Cloud Platform에서 제공하는 컨테이너 이미지 저장소
   - GCP 서비스와 연동 및 권한 관리가 용이함

> 이 외에도 Amazon ECR, Azure Container Registry