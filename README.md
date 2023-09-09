# Pet Net Application

A small application to demonstrate how to use `pydomkeys`.  PetNet Application ...

## Implementations

* pickleDB
* redis
* sqlite3

## Domain Models


* user
    * key
    * version
    * value first_name, last_name, email, phone, birth_year, pets []
    * status
* pet
    * key
    * version
    * value name, type, bread, birth_year, owner, vet
    * status
* vet
    * key
    * version
    * value name, type, phone, email
    * status
* appointments
    * key
    * version
    * value date, time, vet
    * status
* version
    * create_date
    * last_update
    * version
    * hash
* status
    * new, active, inactive

## The Application

### Build the dataset

### Unit Tests

### Integration Tests



### Run the Application

`just run` then navigate to `http://localhost:9001/docs`

test the endpoints

## Misc

* consider making this a submodule of pydomkeys? $ git submodule add https://github.com/darrylwest/petnet-app
* consider a submodule of pydomkeys? $ git submodule add https://github.com/darrylwest/pydomkeys


###### darryl.west | 2023.09.09
