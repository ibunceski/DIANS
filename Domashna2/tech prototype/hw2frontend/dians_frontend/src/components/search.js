import React, {useState, useEffect} from "react";
import {AsyncPaginate} from "react-select-async-paginate";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const AutocompleteIssuerSearch = () => {
    const [issuers, setIssuers] = useState([]);
    const [search, setSearch] = useState(null);
    const navigate = useNavigate();


    useEffect(() => {
        const fetchIssuers = async () => {
            try {
                const response = await axios.get(
                    "http://localhost:8080/api/issuers"
                );
                setIssuers(response.data);
            } catch (error) {
                console.error("Error fetching issuers:", error);
            }
        };

        fetchIssuers();
    }, []);

    const loadOptions = async (inputValue) => {
        if (!inputValue.trim()) {
            return {options: []};
        }
        const filteredIssuers = issuers.filter((issuer) =>
            issuer.toLowerCase().startsWith(inputValue.toLowerCase())
        ).slice(0, 5);
        return {
            options: filteredIssuers.map((issuer) => ({
                label: issuer,
                value: issuer,
            })),
        };
    };
    const handleOnChange = (selectedOption) => {
        setSearch(selectedOption);
        if (selectedOption) {
            navigate('/details', {
                state: {
                    issuer: selectedOption.value
                }
            });
        }
    };

    const customStyles = {
        control: (provided) => ({
            ...provided,
            marginTop: "10px",
            marginBottom: "300px",
            width: "400px",
            height: "50px",
            backgroundColor: "#f9f9f9",
            border: "1px solid #ccc",
            borderRadius: "8px",
            fontSize: "14px",
        }),
        menuList: (provided) => ({
            ...provided,
            backgroundColor: "#f5f5f5",
            borderRadius: "8px",
            padding: "0",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
            border: "1px solid #e0e0e0",
            maxHeight: "100px",
            marginTop: "-300px"
        }),
        option: (provided, state) => ({
            ...provided,
            backgroundColor: state.isFocused ? "#f0f0f0" : "#ffffff",
            color: "#333",
        }),
        singleValue: (provided) => ({
            ...provided,
            color: "#333",
        }),
    };

    return (
        <AsyncPaginate
            styles={customStyles}
            placeholder="Search issuers"
            debounceTimeout={500}
            value={search}
            onChange={handleOnChange}
            loadOptions={loadOptions}
        />
    );
};

export default AutocompleteIssuerSearch;

