# Agent

- Gives LLMs tool access on the system and lets them run in a loop to
solve relatively complex tasks autonomously
- Uses Google's Gemini LLM

## How to use

Run the below command

```sh
uv run main.py <prompt> [--verbose]
```

- `--verbose` explicitly prints out the LLM's "thoughts", and also
prints the number of tokens used in the exchange.
- The agent loop runs a maximum of 20 times

## Demos

### Getting information about a file

```
$ uv run main.py "explain how the file \`hello.py\` works"
Calling function: get_file_content({'file_path': 'hello.py'})
 - Calling function: get_file_content
file_path: hello.py
The file `hello.py` is a Python script that takes an integer input from the user. It then iterates from 0 up to (but not including) the given number. In each iteration:
- If the current number is divisible by 15, it prints "FizzBuzz".
- If the current number is divisible by 3 (but not by 15), it prints "Fizz".
- If the current number is divisible by 5 (but not by 15), it prints "Buzz".
- Otherwise, it prints the number itself.
```

### Annotating source code

```
$ uv run main.py "annotate \`hello.py\` and add a README.md to the project explaining what it is and how to use it"
Calling function: get_files_info({})
 - Calling function: get_files_info
Calling function: get_file_content({'file_path': 'hello.py'})
 - Calling function: get_file_content
file_path: hello.py
Calling function: write_file({'content': '#!/usr/bin/env python3\n\n# This script plays the classic FizzBuzz game.\n# It prompts the user to enter a number and then iterates from 0 up to (but not including) that number.\n# - If the number is a multiple of both 3 and 5 (i.e., a multiple of 15), it prints "FizzBuzz".\n# - If the number is a multiple of 3, it prints "Fizz".\n# - If the number is a multiple of 5, it prints "Buzz".\n# - Otherwise, it prints the number itself.\n\n# Get input from the user for the upper limit of the FizzBuzz game.\na = int(input("enter a number: "))\n\n# Iterate from 0 up to \'a\' (exclusive).\nfor i in  range(a):\n    # Check if \'i\' is a multiple of both 3 and 5.\n    if i % 15 == 0:\n        print("FizzBuzz")\n    # Check if \'i\' is a multiple of 3.\n    elif i % 3 == 0:\n        print("Fizz")\n    # Check if \'i\' is a multiple of 5.\n    elif i % 5 == 0:\n        print("Buzz")\n    # If none of the above, print the number itself.\n    else:\n        print(i)\n', 'file_path': 'hello.py'})
 - Calling function: write_file
Calling function: write_file({'content': '# FizzBuzz Game\n\nThis project contains a simple Python script that plays the classic FizzBuzz game.\n\n## `hello.py`\n\nThis script prompts the user to enter a number. It then iterates from 0 up to (but not including) that number, applying the following rules:\n\n- If the number is a multiple of both 3 and 5, it prints "FizzBuzz".\n- If the number is a multiple of 3, it prints "Fizz".\n- If the number is a multiple of 5, it prints "Buzz".\n- Otherwise, it prints the number itself.\n\n### How to Run\n\n1. Make sure you have Python 3 installed.\n2. Execute the script from your terminal:\n   ```bash\n   python3 hello.py\n   ```\n3. When prompted, enter a number and press Enter.\n', 'file_path': 'README.md'})
 - Calling function: write_file
I've successfully annotated `hello.py` and added a `README.md` file to your project.
```

## Planned features

- [ ] Don't hard-code the working directory
- [ ] User-specified number of iterations
- [ ] Access to additional tools:
  - [ ] Recursive regex search (via `ripgrep`)
  - [ ] System manual pages (via `man`)
  - [ ] Python documentation (via `pydoc`)