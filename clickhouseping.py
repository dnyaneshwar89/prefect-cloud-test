import clickhouse_connect

if __name__ == '__main__':
    client = clickhouse_connect.get_client(
        host='q3zu55b6u5.ap-south-1.aws.clickhouse.cloud',
        user='default',
        password='m.ZYik17aFDmy',
        secure=True
    )
    # print("Result:", client.query("SELECT * from test_source").result_set[0][0])
    # print("Result:", client.query("SELECT * from test_source").result_set)
    client.insert("test_destination", [['new simple text']],column_names=['data'])


# from clickhouse_driver import Client

# try:
    # client = Client(host='q3zu55b6u5.ap-south-1.aws.clickhouse.cloud', port=9440,user='default', password='m.ZYik17aFDmy',secure=True,verify=False)
    # client.execute('SELECT 1')
    # print("Connection successful")
    # client.command("INSERT INTO test_destination (data) VALUES", [('simple text',)])
# except Exception as e:
    # print(f"Error: {e}")
