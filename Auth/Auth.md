# Authentication
## Requirements
python-dotenv
ldap3
pycryptodome (python does not support MD4 hash algorithm needed by ldap3)
PyJWT

## Functions
### **JWT.authenticate_token(token: str)**
#### Description
Verfies the credibility of a token

Args: 
* token(string): Token, whose credibility is to be reviewed

Returns:
* 0: Token not credible
* 1: Token credible

Exceptions:\
(!ToDo)
* Token not credible
* Token expired

#### Example Implementation
```python
from JWT import authenticate_token

securedFunction(arg1, token:str): #You need to be logged in as AD-user to execute this function
    if authenticate_token(token)==1:
        ... #execute function
    else:
        return exception
```

### **JWT.authenticate(username: str, passwd: str)**
#### Description

#### Example Implementation

### **JWT.new_token(username: str, passwd: str)**
#### Description

#### Example Implementation

### **pypath.verify_login(username: str, passwd: str)**
#### Description

#### Example Implementation