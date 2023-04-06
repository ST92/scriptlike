# Scriptlike

## Python = quick prototyping
## `scriptlike` = quicker prototyping

## Instructions
### obtain

Inside your project

    git clone this_repo your_dir_name

somewhere inside your package tree. Assuming you have chosen "`dev`" as `your_dir_name`
you should create this way a package with no modules.

### short description

It's called `scriptlike` because it behaves a lot like calling shell (`bash`, etc.) scripts
from other scripts. You can even do something like:

    $ rm -f ./my_script                 # then...             
    $ sleep 300 && ./my_script args &   # you have 5 minutes to make `my_script` be an executable!

### longer example

Create a python file inside "`dev`", for example `functions.py`:

    import random

    def foo(x,y):
        print(x)
        print(y)
        return 13

    def bar(x):
        z = foo(x,6)
        print("Boo!")
        print(z*2)
        return z*2

From sibling modules do either one of

    from .dev import *
    from . import dev

    # unfortunately this doesn't work as `functions` only imitates a module
    from .dev import functions

to obtain access to `dev.functions` object, that allows access to
every `callable` and `not callable` member of the real module, except:

- every `callable` reloads whole `functions` module right before every call
- `not callable` items pass through to the latest version of the namespace
- every `callable` that was available before reload and now is not, is removed
- new names are made available right after any call to `callable`
- `callable` that resolves to nothing after reload will act like calling `None`

like this:
    
    from .dev import *
    handler = functions.foo

    handler(1,2)            # prints 1 2 13
    functions.bar(3)        # prints 3 6 13 26
    
    # .. change functions.py: 13 to 20, z*2 to z%10, name `bar` to `baz` and save file
    
    functions.bar(3)        ##  Exception: NoneType is not callable  (but it reloaded so...)
    functions.bar(3)        ##  Exception: AttributeError `functions` has no attribute `bar`
    handler(1,2)            # prints 1 2 20
    functions.baz(3)        # prints 3 6 20 0

Now if you have a service that's costly to bring up and tear down, but you want
to develop on a _function tweaking_ level, you can make the project call this
directory's definitions, and as long as it doesn't crash, you can repeat
the process without restarting everything. 

At the end of the day, the definitions can be copied verbatim to their proper place.

# License: MIT