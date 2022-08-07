# PEP

Python을 깊이있게 공부하다보면 PEP라는 용어를 많이 보게 된다.
공식 문서에서 이번 버전에서는 PEP 몇 번을 반영했다고 공지한다던가, PEP 몇 번의 문법이 IDE에 반영되지 않으니 수정해달라고 포럼에 올라온다든가.

그렇다면 PEP란 무엇인가? 이는 PEP 1에 정의되어있다.

https://peps.python.org/pep-0001/#what-is-a-pep

PEP는 Python Enhancement Proposal의 약자이다.
Python 커뮤니티에 정보를 전달하거나 새로운 기능을 알려주는 설계 문서.

https://github.com/python/peps

GitHub에도 공개되어있으니 오픈소스 기여를 할 수도 있겠다!

PEP의 타입들:

1. Standards Track PEP: 새로운 기능을 알려주는 PEP
2. Informational PEP: 파이썬 설계 이슈나 일반적인 가이드라인을 제공하는 PEP. 새로운 기능을 제안하지는 않는다.
3. Process PEP: 파이썬 관련 프로세스를 알려주는 PEP

예를 들어, PEP 1은 파이썬에서 PEP가 무엇이고 새 기능이 PEP에 어떻게 명시되고 이런 프로세스를 알려주는 PEP이므로 Process PEP이다.
반면 with-statement를 제안하는 PEP 343은 Standards Track PEP이다.

새로운 PEP를 제안하고 싶다면 PEP repository를 포크해서 draft PEP를 작성한 뒤 pull request를 요청하면 된다.
PEP editor들이 리뷰한 뒤 승인되면 PEP의 번호를 받는다. 이후 이 PEP에 대해 토론하고 리뷰하는 과정이 있다.

실제로 PEP repository에서 closed pull requests 중 `new-pep` label 단 것들을 보면 제안된 PEP들을 볼 수 있다.
