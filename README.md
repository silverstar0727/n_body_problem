# many_body_problem

<p float="left">
<a> <img src="https://img.shields.io/badge/Language-Python3-blue" alt="alt text"> </a>
<a> <img src="https://img.shields.io/badge/Language-Jupyter notebook-blue" alt="alt text"> </a>  
<a> <img src="https://img.shields.io/badge/Language-Anaconda3-blue" alt="alt text"> </a>
</p>

우주에 떠 있는 행성은 무슨 원리에 의해 움직이는가? 일찍이 뉴턴은 그 힘을 만유인력으로 밝혔으나, 3가지 물체에 대한 일반해를 유도할 수 없음을 푸앵카레가 증명하였다. 이를 3체문제라고 명명하고 수많은 특수해들을 찾기 위한 과학자들의 노력이 시작되었다.

일반해가 없음은 자명하나, 스윙바이 현상 등 우리가 천체의 위치를 정확히 예측하는 것은 꽤나 중요한 주제일 것이다. 그렇다면, 우리는 일반해가 없는 문제에 대해 어떠한 솔루션을 제시할 것인가. 과연 우리가 포기해야 맞는 것인가.

현재 과학계는 이를 컴퓨팅을 이용한 알고리즘을 통해 초기조건을 주어졌을 경우, 특수해를 구하기 위해 노력하고 있으며 본 프로젝트 또한 이를 시도하고자 한다. 


##### 일반해가 존재하지 않음에도 불구하고 우리는 답을 찾을 것이다. 언제나 그랬듯이.


## Requirements
본 코드에서 궤도 모션의 애니메이션을 실행 시키기 위해서는 사전에 ffmpeg package가 설치되어 있어야 한다. 이는 anaconda terminal에서 다음의 코드로 설치할 수 있다.
```python
conda install -c menpo ffmpeg
```
이 비디오는 주피터 노트북에서 html5를 사용하며 이는 mp4로 저장이 가능하다.


## viewer error
종종 .ipynb파일이 열리지 않는 경우가 있는데, 이는 깃허브 뷰어의 문제인 것으로 보여진다.

다음의 링크에서 보고자 하는 .ipynb 파일의 주소를 복사하여 붙여 넣으면 볼 수 있다.

github의 불친절... ㅠㅠ
