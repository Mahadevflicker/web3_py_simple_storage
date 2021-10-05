// SPDX-License-Identifier: MIT

// Created by Mahadevan

pragma solidity ^0.6.0;

contract SimpleStorage {

    // Initializing the variable

    uint256 favouriteNumber;
    bool favouriteBool;

    // Creating record of people and favourite number

    struct People{
        uint256 favouriteNumber;
        string name;
    }

    // Declaring dynamic array

    People[] public people;

    // Mapping to combine above arry and struct for people dictionary

    mapping(string => uint256) public nameToFavouriteNumber;


    // Stores the record of the favouriteNumber
    function store(uint256 _favouriteNumber) public {

        favouriteNumber = _favouriteNumber;
    }

    // Retrieve the record of the favouriteNumber
    function retrieve() public view returns(uint256) {

        return favouriteNumber;

    }

    //Function to store all the values

    function addPerson(string memory _name,uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber,_name));
        nameToFavouriteNumber[_name] = favouriteNumber;
    }
}
