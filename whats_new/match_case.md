# PEP 634: Structural Pattern Matching

https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching

3.10 버전에서 추가된 기능

```python
match subject:
    case <pattern_1>:
        <action_1>
    case <pattern_2>:
        <action_2>
    case <pattern_3>:
        <action_3>
    case _:
        <action_wildcard>
```

C나 Java의 switch-case와 비슷하지만 다음의 차이점이 있다.

- pattern_1을 만족할 경우 action_1만 실행함. 따로 break를 작성하지 않아도 action_2, action_3은 실행되지 않는다.
- `default:` 대신 `case _:`로 다른 조건에 안 걸리는 케이스를 다룬다.

다음과 같은 방식으로 동작한다.

1. `subject`는 type과 shape가 있는 데이터
2. `match` statement에서 `subject`를 평가한다
3. 위에서부터 `case` statement의 패턴과 비교한다. 매치가 성사될 때까지
4. 매치가 성사되면 해당 `case`의 body를 실행한다.
5. 매치가 성사되지 않으면 와일드카드인 `_` 패턴과 매치된다. `_` 패턴이 없다면 아무 동작도 하지 않는다.

## Match to a literal

```python
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```

익숙한 switch-case 같은 예시이다. 다음과 같이 `|`("or") 로 여러개의 literal을 연결할 수도 있다.

```python
case 401 | 403 | 404:
    return "Not allowed"
```

## Patterns with a literal and variable

subject를 unpack하고 값 일부를 변수로 쓸 수도 있다.

```python
# point is an (x, y) tuple
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
```

첫번째 패턴인 `case (0, 0):`은 literal 매치 패턴과 같다.

하지만 두번째 패턴은 `case (0, y)`로 선언된 적 없는 `y` 변수를 쓰고 있다.
첫번째 패턴에 매치되지는 않지만 첫번째 값이 0인 경우, 두번째 값을 `y` 변수에 넣고 body를 실행한다.

세번째 패턴, 네번째 패턴도 마찬가지로 unpack해서 match를 확인하고 변수에 unpack된 값을 넣는다.

### 보너스: case statement의 지역변수

그렇다면 만약 x, y가 이미 정의된 변수라면 어떻게 될까?

```python
def match_point(point):
    x = 1
    y = 2

    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")

match_point((0, 1))
```

미리 `y=2`로 변수를 정의했지만, **case statement에서의 y에 1을 대입했으므로 실행결과는 `Y=1`이다. (0, 2)를 매치하는 방식으로 동작하지 않는다.**

좀더 간단한 예제도 살펴보자.

```python
a = 2
b = 5

match a:
    case b:
        print(a, b)

print(a, b)
```

```
2 2
2 2
```

a에 있는 값이 b에 있는 값 5와 일치하는지를 검사하는 게 아니라, 패턴에 일치하는지 확인하고 변수에 a 값을 대입힌다.
그렇기 때문에 변수 b에 2가 들어간다.

## Patterns and classes

클래스 객체의 패턴 매칭을 하고 싶을 경우, 생성자를 호출하는 것 같은 형태로 패턴을 작성할 수 있다.
이 경우 class attribute를 변수에 대입할 수도 있다.

```python
class Point:
    x: int
    y: int

def location(point):
    match point:
        case Point(x=0, y=0):
            print("Origin is the point's location.")
        case Point(x=0, y=y):
            print(f"Y={y} and the point is on the y-axis.")
        case Point(x=x, y=0):
            print(f"X={x} and the point is on the x-axis.")
        case Point():
            print("The point is located somewhere else on the plane.")
        case _:
            print("Not a point")
```

위의 튜플 예시와 비슷하지만 클래스를 쓴 예제이다.

## Nested patterns

nested 형태로 패턴을 작성할 수도 있다.

```python
match points:
    case []:
        print("No points in the list.")
    case [Point(0, 0)]:
        print("The origin is the only point in the list.")
    case [Point(x, y)]:
        print(f"A single point {x}, {y} is in the list.")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two points on the Y axis at {y1}, {y2} are in the list.")
    case _:
        print("Something else is found in the list.")
```

이 때 nested pattern에도 와일드카드를 포함할 수 있다.

패턴에 if 문을 같이 쓸 수도 있다. 이 경우 패턴도 매치되고 if 문도 통과해야 매치된 것으로 판정된다.

```python
match point:
    case Point(x, y) if x == y:
        print(f"The point is located on the diagonal Y=X at {x}.")
    case Point(x, y):
        print(f"Point is not on the diagonal.")
```

tuple, list 같은 sequence 들은 서로 매칭 가능하다. iterator는 매치할 수 없으며 sequence 패턴과 string은 서로 매치되지 않는다.

`[x, y, *rest]` 형태로 unpack할 때 쓰던 sequence pattern을 쓸 수 있다. `*_`도 가능

nested 패턴 안의 일부 패턴을 `as`로 변수에 대입할 수 있다. 아래 예시의 경우 x1 y1 x2 y2가 각자 대입된 뒤 두번째 Point 객체 통째로 p2에 대입됨

```python
case (Point(x1, y1), Point(x2, y2) as p2): ...
```

named constants를 쓸 수도 있지만 반드시 dotted name으로 써야 한다! 그렇지 않으면 위의 변수 예제처럼 변수에 대입되는 형태로 작동한다.

```python
from enum import Enum
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
```

# PEP 636 - Structural Pattern Matching: Tutorial

https://peps.python.org/pep-0636/

텍스트 어드벤처를 예시로 structural pattern matching의 예제를 보여주는 PEP

텍스트 어드벤처를 구현하려면 먼저 사용자의 입력 텍스트를 파싱해야 한다. split()을 쓰면 다음과 같을 것이다.

```python
command = input("What are you doing next?")
[action, obj] = command.split()
```

그런데 command가 3단어라면? 1단어라면? 백준 풀 때도 골치아팠던 것처럼 문제가 발생한다.

match statement로는 다음과 같이 작성할 수 있다.
```python
match command.split():
    case [action]:
        ...
    case [action, obj]:
        ...
    case _:
        ...
```

그리고 `if action = "quit"` 이런 걸 줄줄이 이어붙일 필요없이 match statement에 literal 매치 조건을 바로 작성할 수 있다.

```python
match command.split():
    case ["quit"]:
        print("Goodbye!")
        quit_game()
    case ["look"]:
        current_room.describe()
    case ["get", obj]:
        character.get(obj, current_room)
    case ["go", direction]:
        current_room = current_room.neighbor(direction)
    case ["drop", *objects]:
        for obj in objects:
            character.drop(obj, current_room)
```

dict는 다음과 같은 형태로 매치할 수 있다. 이 때 패턴에 정의되지 않은 추가 아이템들이 있어도 패턴 매치로 판정된다.

```python
for action in actions:
    match action:
        case {"text": message, "color": c}:
            ui.set_text_color(c)
            ui.display(message)
        case {"sleep": duration}:
            ui.wait(duration)
        case {"sound": url, "format": "ogg"}:
            ui.play(url)
        case {"sound": _, "format": _}:
            warning("Unsupported audio format")
```

이 외에도 소개된 문법들을 실제 구현에서 어떤 상황에 쓸 수 있을지 예제가 다양하게 제시되어있다!