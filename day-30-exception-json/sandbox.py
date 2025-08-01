#FileNotFoundError
try:
    file = open("a_file.txt")
    a_dictionary = {"key": "value"}
    print(a_dictionary["key"])
except FileNotFoundError:
    file = open("a_file.txt", "w")
    file.write("Something")
except KeyError as error_message:
    print(f"The key {error_message} does not exist.")
else: # if no error, execute this block
    content = file.read()
    print(content)
finally: # always execute this block
    file.close()
    print("File was closed")