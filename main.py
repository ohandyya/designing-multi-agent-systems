import os


def myfunc(a: int, b: int):
    return a + b


def main():
    print("Hello from designing-multi-agent-systems!")

    print(myfunc(1, 2))
    
    print(os.getenv('OPENAI_API_KEY'))


if __name__ == "__main__":
    main()
    
