import mlflow

def calculator(a, b, operation=None):
    if operation == 'add':
        return a+b
    elif operation == 'subtract':
        return a-b
    elif operation == 'multiply':
        return a*b

if __name__=='__main__':
    a, b, operation = 2, 3, "subtract"
    # Start the server of MLflow
    with mlflow.start_run():
        res = calculator(a, b, operation)
        # Track it
        mlflow.log_param('a', a)
        mlflow.log_param('b', b)
        mlflow.log_param('operation', operation)
        print(res)
        mlflow.log_param('result', res)
