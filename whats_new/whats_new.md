# What's New In Python 3.10

https://docs.python.org/3.10/whatsnew/3.10.html

## Parenthesized context managers

`with` 키워드를 이용한 구문에서 다음과 같이 여러 개의 context manager를 쓸 수 있다.

```python
with (
    CtxManager1() as example1,
    CtxManager2() as example2,
    CtxManager3() as example3,
):
    ...
```

[예시 코드](parenthesized_context_managers.py)
```python
with (open("input.txt", "r", encoding="utf-8") as fread,
      open("output.txt", "w", encoding="utf-8") as fwrite):
    fwrite.write(fread.read())
```

파일 입출력할 때 쓰는 built-in function `open()`을 이용한 예시이다.
이렇게 `with` 키워드를 이용한 구문에 괄호를 쓸 수 있다.

[보너스: Context Manager](/bonus/context_manager.md)