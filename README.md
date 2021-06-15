# Number theoretic methods in cryptography
Laboratory work on the number-theoretic method in cryptography.

## Dependencies

For this module to work, you need to install certain libraries, namely: sympy and gmpy2. If you want 
to use this module as a library, you can skip this step, otherwise you need to enter the following 
command to install:

```zsh
pip install sympy, gmpy2
```


## Usage
There are several use cases:

1. **Use as a module.**
   We just add the **ntmcrypt** folder to the project and import any module:
   
    ```python
    from ntmcrypt import rsa
    ```

2. **Use as a library.**
    To use a module as a library, you need to build the library. First, you need to clone the repository:

    ```zsh
    git clone https://github.com/vasilyperekhrest/Number-theoretic-methods-in-cryptography.git
    ```

    Next, you need to go to the folder with the project and run the __setup.py__ script:

    ```zsh
    cd Number-theoretic-methods-in-cryptography/
    python setup.py sdist
    ```
    
    After executing the script, the **dist** folder will appear, in which the library will be located. 
    The next step is to install the library and all its dependencies:
    
    ```zsh
    pip install dist/ntmcrypt-0.1.tar.gz
    ```
    
    After installation, you can safely delete the folder with this project, for this 
    you need to enter the following commands:
    
    ```zsh
    cd ..
    rm -rf Number-theoretic-methods-in-cryptography/
    ```
