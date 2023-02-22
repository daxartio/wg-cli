# Wiregurad CLI

## Get started

### Help

```
usage: wg_cli [-h] name address

positional arguments:
  name
  address

options:
  -h, --help  show this help message and exit
```

### Required files

```
endpoint
privatekey
publickey
wg0.conf
```

### Run

```
wg_cli test 10.0.0.5/32
```

#### Created files

Will create files

```
test_publickey
test_privatekey
test.conf
```

Will change the file `wg0.conf`
