# N_body_problem

<p float="left">
<a> <img src="https://img.shields.io/badge/Language-Python3-blue" alt="alt text"> </a>
<a> <img src="https://img.shields.io/badge/Language-Jupyter notebook-blue" alt="alt text"> </a>  
<a> <img src="https://img.shields.io/badge/Language-Anaconda3-blue" alt="alt text"> </a>
</p>

#### 본 프로젝트는 연세대학교 ACE 사업단으로부터 지원금을 받아 진행되었습니다.

우주에 떠 있는 행성은 무슨 원리에 의해 움직이는가? 티코브라헤는 일생을 바쳐 천체를 관측했으며, 이를 바탕으로 요하네스 케플러가 케플러 법칙을 정립하기에 이른다. 뉴턴은 그 힘을 만유인력으로 밝혔으나, 3가지 물체에 대한 일반해를 유도할 수 없음을 위대한 수학자 푸앵카레가 증명하였다. 이를 3체문제라고 명명하고 수많은 특수해들을 찾기 위한 과학자들의 노력이 시작되었다.

일반해가 없음은 자명하나, 스윙바이 현상 등 우리가 천체의 위치를 정확히 예측하는 것은 꽤나 중요한 주제일 것이다. 그렇다면, 우리는 일반해가 없는 문제에 대해 어떠한 솔루션을 제시할 것인가. 과연 우리가 포기해야 맞는 것인가.

현재 과학계는 이를 컴퓨팅을 이용한 알고리즘을 통해 초기조건이 주어졌을 경우, 특수해를 구하기 위해 노력하고 있으며 본 프로젝트 또한 이를 시도하고자 한다. 



## 3body simulation 결과
3body_main.ipynb

https://www.youtube.com/watch?v=dthhIN79EJE&t=2s

![sample_output_1](https://user-images.githubusercontent.com/49096513/88818032-32f1f100-d1f9-11ea-993e-03b72b5c9976.gif)
## n-body simulation 결과
n-body modeling.py

https://www.youtube.com/watch?v=JqrZXK-2J84
![KakaoTalk_20200726_220712734](https://user-images.githubusercontent.com/49096513/88479761-7562c600-cf8c-11ea-9546-14b2a3d3fcf1.png)



## Requirements
본 코드에서 궤도 모션의 애니메이션을 실행 시키기 위해서는 사전에 ffmpeg package가 설치되어 있어야 한다. 이는 anaconda terminal에서 다음의 코드로 설치할 수 있다.
```python
conda install -c menpo ffmpeg
```
이 비디오는 주피터 노트북에서 html5를 사용가능케 하며 이는 mp4로 저장이 가능하다.


## Viewer Error
종종 .ipynb파일이 열리지 않는 경우가 있는데, 이는 깃허브 뷰어의 문제인 것으로 보여진다.

다음의 링크에서 보고자 하는 .ipynb 파일의 주소를 복사하여 붙여 넣으면 볼 수 있다.
>https://nbviewer.jupyter.org/

github의 불친절... ㅠㅠ


## Mathematical Theory
본 프로젝트는 solution을 근사적으로 도출하는 프로젝트인데, 그 수학적 이론은 numerical anaylsis에 기초한다.

Euler method등 다양한 방법이 존재하나 삼체문제는 RK4를, 다체문제는 euler method 주로 사용한다.

## Singularity
문제가 발생했던 지점은 r = 0일 때이다. zero division error가 발생하는 것은 아니지만, r이 0에 한없이 가까워 질 때 계산량은 무한히 증가하게된다.

중력의 공식을 참고해보면 어쩌면 당연한 결과였을 것이다.

해당 문제를 해결하는 방법으로 최규홍 교수님 저의 천체역학 3장을 참고하면, 수학적으로 이를 없앨 수 있으나, 이 또한 단점이 존재한다.

따라서, 본프로젝트에서는 단순히 r이 0에 가까워지기 이전에 업데이트를 특정한 값으로 고정하는 것으로 대체하였다.

추후에 이를 보완하여 업데이트를 할 수 있었으면 좋겠다... ㅠㅠ

## Further Study
![2010030235534653](https://user-images.githubusercontent.com/49096513/89095146-d9124680-d405-11ea-89c4-78a2ca27a1d8.jpg)

다체문제의 영상을 보면, 2분만에 나선 팔이 사라지는 것을 확인할 수 있다. 이는 이론과 상당히 부합하는데, 이론상으로 은하의 중심에서 멀어질수록 회전 속도는 감소하기 때문이다.
위 그림에서도 곡선 A가 그것에 해당한다. 그러나, 이는 실질 관측결과와는 차이가 존재한다. 실질 관측결과는 곡선 B에 해당하며, 이러한 현상은 암흑물질(Dark Matter)의 존재를 예견한다.

추후에 암흑물질의 분포를 예측할 수 있는 프로젝트를 진행하면 좋을 듯 싶다.
