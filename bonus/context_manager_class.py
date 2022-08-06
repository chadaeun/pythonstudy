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
    a = 0 / 0