from prefect import flow, task

@task
def my_task(message):
    print(f"Task message: {message}")
    return message

@flow
def my_flow(message="Hello, Prefect Cloud!"):
    result = my_task(message)
    print(f"Flow result: {result}")

if __name__ == "__main__":
    my_flow()
