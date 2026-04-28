# Python Coding Standards (ENG1013)

**Version:** 2.0  
**Last Updated:** Jan 1, 2024  

## Purpose
This document defines Python coding standards for ENG1013: Engineering Smart Systems (Monash University).  
Follow these guidelines for assignments, tests, and exams.

## Variables

### Name of the Variable
Variables should clearly describe what they represent.

**Best practice:**
```python
buildingHeight = 100
````

**Bad example:**

```python
x = 100
```

### Style of the Variable

Use **lower camel case** (first word lowercase, subsequent words capitalised).

**Best practice:**

```python
numberOfInputs
```

**Bad examples:**

```python
NumberOfInputs
Number_of_inputs
number_of_inputs
```

## Functions

### Name of the Function

Use descriptive names indicating what the function does.

**Best practice:**

```python
def find_max_number(numb1, numb2):
```

**Bad example:**

```python
def fx(numb1, numb2):
```

### Style of the Function

Use **snake_case** (lowercase words separated by underscores).

**Best practice:**

```python
def find_max_number(numb1, numb2):
```

**Bad examples:**

```python
def findmaxnumber(numb1, numb2):
def Find_Max_Number(numb1, numb2):
def find_Max_Number(numb1, numb2):
```

## Magic Numbers

Magic numbers are numeric literals with no explanation. Avoid them by assigning values to well-named variables.

**Best practice:**

```python
pi = 3.14

radius = float(input("Enter the radius of a circle:"))
area = pi * radius * radius

print("Area of a circle = %.2f" % area)
```

**Bad example:**

```python
radius = float(input("Enter the radius of a circle:"))

area = 3.14 * radius * radius

print("Area of a circle = %.2f" % area)
```

## Indentation

Indentation defines code blocks. Python uses **4 spaces per indentation level**.

### Criteria

* One tab = four spaces
* Code blocks should be clear and readable
* All content within a block must be indented

### Example

```python
def some_function(x, y):

    if x > 100:

        if y > 100:
            doThing(x, y)

        elif y < 100:
            doThing(x, 100 - y)

    elif x < 100:

        if y > 100:
            doThing(x + 50, y)

        elif y < 100:
            doThing(x + 50, 100 + y)
```

## Documentation

Code should be understandable to both users and developers.

### Inline Comments

Use `#` for short comments.

**Example:**

```python
def hello_world():
    # A simple comment preceding a print statement
    print("Hello World")
```

### Multiple Line Comments

Use `#` on each line or triple quotes `"""`.

**Example:**

```python
# comment line 1
# comment line 2
# comment line 3
```

```python
"""
This is a block
comment.
"""
```



### File Headers

Include metadata at the top of each file.

**Example:**

```python
# Details about the module and its purpose
# Created By  : name_of_the_creator
# Created Date: date/month/time
# version = '1.0'
```

### Function Headers

Each function should include a description, parameters, and return value.

**Example:**

```python
"""
Used to print a hello message with name included.

Parameters:
name (string): The string name to be printed

Returns:
function has no return
"""
def hello_name(name):
    print(f"Hello, {name}")
```