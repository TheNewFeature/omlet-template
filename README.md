# OMLET Template
![CI Lint](https://github.com/TheNewFeature/omlet-template/workflows/Lint/badge.svg)

## 사용 방법
- 세션 컨테이너에서는 `main.py`를 실행합니다. 따라서 전체 프로세스의 진입점은 `main.py`에 작성되어야 합니다.
- 세션 컨테이너의 이미지는 `main.py`에 작성된 `shebang`을 통해 결정됩니다. 따라서 `main.py`의 첫 줄에는 아래와 같은 형식으로 실행할 `Docker` 이미지의 이름을 적어주어야 합니다.
  - `#!omlet: nvcr.io/nvidia/tensorflow:21.09-tf2-py3`
- 세션 컨테이너는 `main.py`를 실행하기 전, `python -m pip install -r requirements.txt`를 통해 필요한 패키지를 설치합니다. 사용하는 외부 패키지는 `requirements.txt`에 작성이 필요합니다.
  - ※주의: `-e git+git://github.com/TheNewFeature/omlet-common#egg=omlet_common`를 삭제할 경우 정상적으로 동작하지 않습니다.
