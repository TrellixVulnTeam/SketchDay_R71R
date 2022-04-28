# :blue_book:SketchDay : 내 일기의 감정을 통하여 노래를 추천 받고 그림일기로 볼 수 있는 서비스
> 2022.04.11 ~ 2022.05.10 AI 빅프로젝트
* 일기를 쓰면서 자신의 고민과 일상을 털어놓고 그 감정에 맞는 노래를 듣고 AI를 통해 사용자가 쓴 일기를 그림으로 표현을 해 주면서 다른 사람들과 그림 일기를 공유하며 사용자에게 재미를 주는 서비스 입니다.
# 목차
[1. 조원 소개](#1-조원-소개)

[2. 배경 및 목적](#2-배경-및-목적)

[3. 배경 및 목적](#2-배경-및-목적)

[4. Architecture - 3 - Tier](#4-architecture---3---tier)

[5. ERD](#5-erd)

[6. 실행 방법](#6-실행-방법)
# 1. 조원 소개
#### [5조]수도권 2반 2조
>  김동현(조장), 강민서, 김세진, 전성호, 황인원
# 2. 배경 및 목적
* 시대가 급격하게 변해가면서 바쁘고 지친 하루를 보내고 있는 사람들이 늘어나고 있습니다. 그런 사용자들의 마음의 짐을 덜고 바빴던 일상이 추억이 될 수 있도록 서비스를 제공하고 싶었습니다.추억을 남길 수 있는 좋은 방법으로 일기가 떠올랐고 단순한 일기보다는 작성 한 일기의 감정에 따라 음악을 듣고 그것을 그림일기 형태로 저장할 수 있다면 더 오래 추억에 남고 재미를 줄 수 있을 것 이라고 생각했습니다.

#### :bulb: 즉, 일기 분석을 통한 노래 추천 및 그림일기 생성 서비스를 통해 사용자들의 소통 공간을 만들고자 했습니다.
&nbsp;
* 타켓층
  * 지친 일상생활에서 위로 받고 싶은 사람 
  * 하루를 기록하기를 원하는 사람
  * 자신의 하루를 공유하기 원하는 사람
  * 다른 사람의 일기를 공유 받고 싶은 사람
  * 자신의 일기를 그림일기로 남기고 싶은 사람
# 3. Service Flow
![에이블스쿨 AI 빅프로젝트_Flow Chart_05조](https://user-images.githubusercontent.com/90138160/165701902-97f4d696-584c-4155-8116-7c38d8e43640.png)
# 4. Architecture - 3 - Tier
![image](https://user-images.githubusercontent.com/90138160/165702512-c5253680-c504-4c28-902c-43a4f83885bd.png)
# 5. ERD
![에이블스쿨 AI 빅프로젝트_ERD_05조 (1) (1)](https://user-images.githubusercontent.com/90138160/165702651-7e543f8c-f92d-4066-b6b4-0e7b40a27261.png)
# 6. 실행 방법
1. 가상 환경 구축하기
2. 아래의 명령어를 입력한다.
```
pip install -r requirements.txt
```
