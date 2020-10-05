import React, { Component } from 'react';
import Select from 'react-select';

const covenantsListOptions = [
    {
        name: "0",
        label: "Kyrian"
    },
    {
        name: "1",
        label: "Venthyr"
    },
    {
        name: "2",
        label: "Necrolord"
    },
    {
        name: "3",
        label: "Night Fae"
    }
];

const selectStyles = {
    menu: (provided, state) => ({
        ...provided,
        backgroundColor: '#111622',
        border: '2px solid',
        borderRadius: 4,
        borderColor: '#343f5e',

        width: '200px',
        zIndex: '5',
        marginTop: -4,
    }),
    container: (provided, state) => ({
        width: '200px',
        padding: 20,
    }),
    control: (provided, state) => ({
        // ...provided,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        outline: '0 !important',
        position: 'relative',

        backgroundColor: '#111622',
        border: '2px solid',
        borderRadius: 4,
        borderColor: state.isFocused ? '#343f5e' : '#111622',
        boxShadow: 'none',

        ':hover' : {
            ...provided['"hover'],
            borderColor: '#343f5e',
            borderRadius: '4px',
        }
    }),
    option: (styles, { data, isDisabled, isFocused, isSelected }) => ({
        ...styles,
        backgroundColor: isFocused? '#343f5e' : '#111622',
        color: 'white',
    }),
    singleValue: (styles) => ({
        ...styles,
        color: 'white',
        fontSize: 22,
    }),
    input: (styles) => ({
        ...styles,
        color: 'white',
        fontSize: 22,
    }),
};

export default class CovenantPicker extends Component {

    handleSelectChange = (selected) => {
        this.props.clickHandler(selected.label, parseInt(selected.name));
    };

    render() {
        return (
            <div className="covenantPickerContainer">
                <div className="flexLeft">
                    <div className="covenantIcon">
                        <img src="" />
                    </div>
                    <Select
                        styles={selectStyles}
                        defaultValue={covenantsListOptions[this.props.selectedCovenant]}
                        className="basic-single"
                        classNamePrefix="select"
                        options={covenantsListOptions}
                        onChange={this.handleSelectChange}
                    />
                </div>
            </div>
        )
    }
}