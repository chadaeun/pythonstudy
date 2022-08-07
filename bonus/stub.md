# Stub

https://peps.python.org/pep-0484/#stub-files

PEP 484 - Type Hints에서는 타입 힌트를 작성하는 문법을 제안한다.
이는 Python 3.5부터 반영되었다. 다음과 같은 문법으로 인자와 리턴값에 대한 타입 힌트를 선언할 수 있다.

```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```

Stub 파일은 PEP 484에서 제안된 개념 중 하나이다.
type checker만 참고하는 type hints를 포함하는 파일이다.

일반적인 파이썬 모듈처럼 쓰되 `@overload` decorator가 있다는 점만 다르다.
type checker는 함수의 signature만 참고할 것이므로 function body는 ...로 작성할 것이 권장된다.

모듈과 같은 디렉터리에 같은 이름으로 `.pyi` 확장자를 써서 stub 파일을 작성할 수 있다.

## 예제

[예제 코드 - module](stub.py)

```python
def hello(name: str) -> str:
    print('Hello ' + name)
```

[예제 코드 - stub](stub.pyi)

```python
def hello(name: str) -> str:
    ...
```

PyCharm 같은 IDE에서 stub 파일과 모듈을 연결해주는 것을 확인할 수 있다.

Python의 built-in module에 대응하는 stub 파일들도 확인할 수 있다.
다음은 `round()` 함수의 예시이다.

`builtins.py`

```python
def round(*args, **kwargs): # real signature unknown
    """
    Round a number to a given precision in decimal digits.
    
    The return value is an integer if ndigits is omitted or None.  Otherwise
    the return value has the same type as the number.  ndigits may be negative.
    """
    pass
```

`builtins.pyi`

```python
@overload
def round(number: SupportsRound[Any]) -> int: ...
@overload
def round(number: SupportsRound[Any], ndigits: None) -> int: ...
@overload
def round(number: SupportsRound[_T], ndigits: SupportsIndex) -> _T: ...
```

모듈에서는 typing hints가 없지만, stub 파일에서 typing hints와 오버로드 함수 signature들을 정의한 것을 확인할 수 있다.
PyCharm 같은 IDE에서도 stub 파일을 기준으로 함수 signature를 알려준다.

