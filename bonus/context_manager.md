# Context Manager

## Java의 AutoCloseable

Python에 `with`가 있다면 Java에는 `try-with-resource`가 있다.
다음과 같이 try 블록의 괄호 안에 `AutoCloseable` 인터페이스를 구현한 객체가 있으면 try 블록이 끝난 뒤 자동으로 `close()` 메서드가 호출된다.

```java
import java.io.*;

public class AutoCloseableTest {

	public static void main(String[] args) {
	    // AutoCloseable 인터페이스를 구현한 FileReader, BufferedReader, FileWriter
	    // 객체들을 try-with-resource 블록에서 쓸 수 있다.
		try (FileReader fr = new FileReader("input.txt");
			BufferedReader br = new BufferedReader(fr);
			FileWriter fw = new FileWriter("output.txt")) {
			String buf;
			while ((buf = br.readLine()) != null) {
				fw.write(buf);				
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

}
```

## Context manager란?

Python에서 context manager란 `__enter__()`와 `__exit__()` 메서드가 정의된 객체이다.
다음 예제를 보자.

[예시 코드](/whats_new/parenthesized_context_managers.py)
```python
with (open("input.txt", "r", encoding="utf-8") as fread,
      open("output.txt", "w", encoding="utf-8") as fwrite):
    fwrite.write(fread.read())
```

텍스트 읽기 쓰기 모드이므로 `open()` 메서드는 `io.TextIOBase` 객체를 리턴한다.
`io.TextIOBase`는 `io.IOBase`를 상속하는데, `io.IOBase` 클래스가 context manager임을 확인할 수 있다.
`open()` 메서드의 리턴 객체를 with-statement에 쓸 수 있는 이유이다.

https://docs.python.org/3.10/library/io.html#io.TextIOBase
https://docs.python.org/3.10/library/io.html#io.IOBase

(추가 필요: 파이썬 소스에서 `__enter__()` 메서드와 `__exit__()` 메서드를 못 찾았음)

## with-statement의 역사: PEP 310, PEP 340에서 PEP 343으로

그렇다면 Python의 with-statement는 어떻게 작동할까? 이를 이해하기 위해서는 with-statement의 역사를 알 필요가 있다.

[PEP 343 - The "with" Statement](https://peps.python.org/pep-0343/) -> [Motivation and Summary](https://peps.python.org/pep-0343/#motivation-and-summary)

PEP 310이 원래 with-statement의 형태였는데, 다음과 같은 문법이었다.

```python
with VAR = EXPR:
    BLOCK
```

이것은 다음과 같이 해석할 수 있다.

```python
VAR = EXPR
VAR.__enter__()
try:
    BLOCK
finally:
    VAR.__exit__()
```

PEP 340은 파일을 열고 닫을 때 generator를 템플릿처럼 쓰자는 제안이었다.

```python
@contextmanager
def opening(filename):
    f = open(filename)
    try:
        yield f
    finally:
        f.close()
```

```python
with f = opening(filename):
    ...read data from f...
```

먼저 `@contextmanager`라는 decorator를 달아서 이 메서드가 context manager임을 명시했다.
`opening()` 메서드 안에서는 파일을 연 뒤에 변수 `f`를 **return이 아닌 yield로 전달한다.**
finally 블록에서는 `f.close()`를 수행한다. 이 부분이 with-statement가 끝날 때 쓰이는 듯

그런데 문제가 발생한다. PEP 310에서 `EXPR`의 결과는 `VAR`에 바로 대입되고,
with-statement가 끝날 때 `VAR`의 `__exit__()` 메서드가 호출된다.
그런데 여기서는 `VAR`이 열린 파일을 받아야 하고 `__exit__()` 메서드는 해당 파일의 메서드가 되어야 한다.

(잘 이해가 안 되는데, with-statement가 끝날 때 `opening()` 메서드의 finally 블록을 어떻게 호출할 건지가 문제인가봄)

**프록시 클래스를 이용해서 이를 해결할 수 있다.** `VAR`에는 `__enter__()` 메서드를 호출한 결과를 넣고,
`EXPR`의 결과는 따로 저장해놨다가 나중에 `__exit__()` 메서드를 호출하는 것이다.
**이것이 PEP 343이 제안하는 with-statement의 핵심 동작 방식**(인 것 같다)

```python
mgr = (EXPR)  # EXPR을 실행한 결과를 mgr에 넣음
exit = type(mgr).__exit__  # Not calling it yet
value = type(mgr).__enter__(mgr)  # __enter__() 메서드 실행한 결과를 value에 넣는다
exc = True
try:
    try:
        VAR = value  # Only if "as VAR" is present
        BLOCK
    except:
        # The exceptional case is handled here
        exc = False
        if not exit(mgr, *sys.exc_info()):
            raise
        # The exception is swallowed if exit() returns true
finally:
    # The normal and non-local-goto cases are handled here
    if exc:
        exit(mgr, None, None, None) # 처음에 저장해놓은 exit 메서드 실행
```

with-statement가 이렇게 동작한다면 PEP 310에서 `with VAR = EXPR`이라고 하는 건 이제 의미적으로 맞지 않다.
따라서 as를 쓰도록 바꾼 것이다.

```python
with EXPR as VAR:
    BLOCK
```

## Context manager를 만들어보자

### 클래스로 만들기

`__exit__()` 메서드와 `__enter__()` 메서드를 정의한 클래스를 만들어 with-statement에 써보자.

```python
class ContextManagerClass():
    def __enter__(self):
        print("__enter__() 호출")
        return "__enter__() 메서드의 실행 결과"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__() 호출", exc_type, exc_val, exc_tb)


with ContextManagerClass() as cmc:
    print("BLOCK 시작")
    print(f'{cmc=}')
    print("BLOCK 끝")
```

실행 결과는 다음과 같다.

```
__enter__() 호출  # with-statement 들어가면서 __enter__() 실행
BLOCK 시작
cmc='__enter__() 메서드의 실행 결과'  # __enter__() 메서드에서 리턴한 문자열이 cmc에 들어갔다
BLOCK 끝
__exit__() 호출 None None None  # with-statement 끝나면서 __exit__() 실행
```

`__exit__()`의 인자가 여러 개 있는 것을 볼 수 있다. `exc_`라는 prefix가 붙은 걸 보면 예외처리와 관련한 인자인 것 같다.
코드를 수정해서 with-statement 안에서 예외를 발생시켜보겠다.

```python
class ContextManagerClass():
    def __enter__(self):
        print("__enter__() 호출")
        return "__enter__() 메서드의 실행 결과"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__() 호출", exc_type, exc_val, exc_tb)


with ContextManagerClass() as cmc:
    print("BLOCK 시작")
    print(f'{cmc=}')
    print("BLOCK 끝")
    a = 0 / 0  # ZeroDivisionError 유도
```

결과는 다음과 같다.

```commandline
Traceback (most recent call last):
  File "C:\Users\*****\PycharmProjects\pythonstudy\bonus\context_manager_class.py", line 14, in <module>
    a = 0 / 0
ZeroDivisionError: division by zero
__enter__() 호출
BLOCK 시작
cmc='__enter__() 메서드의 실행 결과'
BLOCK 끝
__exit__() 호출 <class 'ZeroDivisionError'> division by zero <traceback object at 0x0000021A3B73D700>
```

`exc_type`은 예외 타입을, `exc_val`은 예외의 값(메시지?)를, `exc_tb`는 예외의 Traceback을 받는 인자이다.

### Decorator로 만들기

클래스가 아닌 Decorator로도 context manager를 만들 수 있다. `@contextmanager` 데코레이터다.

https://docs.python.org/3/library/contextlib.html?highlight=contextmanager#contextlib.contextmanager

### Asynchronous Context Manager

비동기적인 context manager도 있다.

https://docs.python.org/3/reference/datamodel.html#async-context-managers

클래스로 만들 경우에는 `__aenter__()` 메서드와 `__aexit__()` 메서드를 구현하면 되고,
데코레이터를 단 generator로 만들 경우에는 `@asynccontextmanager`를 쓰면 된다.
