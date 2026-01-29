# Introduction

This project is an attempt to establish a knowledge database, where the emphasis is on the relation of the different elements rather that the abundant and unstructured pile of definitions.

The knowledge base consists of concepts. A concept has a name, has properties and the properties have values. The following rules apply:

- The `name` and `property` are strings with the following rules:
    - they must not contain white spaces
    - they must not start with '_' or '$'

- `name` is unique. If the same name appears twice, the latest definition will survive.

- The values can be
    - a string, if there is only a single value
    - a list of strings if there are multiple values
    - a dictionary, if we want to use a name that occurs only in the actual place, nowhere else.

- Meaning of the value
    - a substring in the value corresponding a valid name refers to that concept
    - a substring in the value corresponding to a local property refers to the values
    - a substring of the form `A of B` where `A` is a valid name and `B` is its valid property refers to their value(s)
    - pural always means list of the singleton
    - if the value is a valid name in the '_type' module, then it means a placeholder whose value must be specified later.
    - a very specific value is a function. A function is a string embraced by '$$' that can be interpreted as a Python lambda function. Its variables should be locally defined properties (see above). When the function name is used, its value is evaluated.
    - another specific value is an action. The action makes a change in the database. It can not be user defined, it should be a name in the database starting with '__' (double underline). 

- If `property` or any of the `values` matches a name in the database, then it implies further relations. For example if 'my laptop' has a 'position' property with value 'my table', and both 'position' and 'my table' occurs in the database, then new relation are generated: 'my table' will have a 'my laptop' property with a value 'position', and (potentially) 'position' may have a property 'my table' with the value 'my laptop'.

- A special property is `_parents`, which means that the actual concept is a subset of another one. Example: in 'our_dog' a property '_parents' : 'dog' means that all properties of the general 'dog' concept is property for our dog as well.

- It can happen that certain properties have possible values in the generic class, and it is specified in the actual class. It can be done by the inheritance through "_parents" keyword, and the we re-define the actual property. We may validate that the actual property already occured in the list of possible properties.



