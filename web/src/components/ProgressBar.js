import React, { Component } from 'react';

const ProgressBar = (props) => {
    const { bgcolour, completed } = props;


    const containerStyles = {
        height: 10,
        width: '100%',
        backgroundColor: "#e0e0de",
        borderRadius: 30,
    };
    // margin: 50

    const fillerStyles = {
        transition: 'width 1s ease-in-out',
        height: '100%',
        width: `${completed}%`,
        backgroundColor: '#f84e57',
        borderRadius: 'inherit',
        textAlign: 'center',
        // overflow: 'hidden',
        color: 'white',
        fontSize: '12px',
    };
    const labelStyles = {
        // padding: 0,
        // display: 'inline-block',
        // textAlign: 'center',
        position: 'relative',
        top: '-3px',
    };

    return (
        <div style={containerStyles}>
            <div style={fillerStyles}>
                {/*<span style={labelStyles}>{`${completed}%`}</span>*/}
                <span style={labelStyles}>{`${completed}%`}</span>
            </div>
        </div>
      );
};

export default ProgressBar;