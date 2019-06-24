# uninitpyc
Tool that scans C source code to find variables that aren't initialized in their declaration. It's a best practice.

## Usage
Scans a single source file for variables that aren't initialized in their declaration.
eg. if tests/simple.c is the following:

```
int main(){
    int a;
    a = 1;
    for (int i = 0, j, k; i < 10; i++){
        int s = i + j + k;
    }
    return 0;
}
```

Then, after installing Pip dependencies, running `python3 uninitpyc.py tests/simple.c` should identify the following uninitialized variables:

```
line 2: int a
line 4: int j
line 4: int k
```

## // TODO
* Comments are unsupported; current workaround is to remove the comments from your source code (https://stackoverflow.com/questions/2394017).
* Investigate other C syntax constructs that need support.
* Add real testing via pytest (improvmeent from current ad-hoc testing).
