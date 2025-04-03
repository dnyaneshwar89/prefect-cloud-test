from prefect import flow

@flow
def my_flow(name):
    print(f"hello {name}")

if __name__ == "__main__":
    my_flow.deploy(
        "example-deployment",
        work_pool_name="test",
        image="prefecthq/prefect:2-latest",
        build=True,
        push=True
    )
