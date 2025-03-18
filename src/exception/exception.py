import sys

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = str(error_message)
        _, _, exc_tb = error_details.exc_info()

        if exc_tb is not None:
            self.error_line = exc_tb.tb_lineno  # Getting line number
            self.error_file = exc_tb.tb_frame.f_code.co_filename  # Getting file name
        else:
            self.error_line = "Unknown"
            self.error_file = "Unknown"

    def __str__(self):
        return f"Error in file {self.error_file} at line {self.error_line}: {self.error_message}"

if __name__ == "__main__":
    try:
        print(1 / 0)
    except Exception as e:
        raise CustomException(error_message=e, error_details=sys)

    print("Exiting main!!!")
