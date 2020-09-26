import React, { Component } from 'react';

const getElemStyle = selected => ({
    border: selected? '2px #fb1563 solid' : '2px #6d778b solid',
    borderRadius: '4px',
});

const getImgStyle = selected => ({
    filter: selected? '' : 'grayscale(100%)',
});

export default class SpecElement extends Component {

    render() {
        return (
            <div style={getElemStyle(this.props.selected)}
                 className={this.props.selected? "specElement specElementLocked" : "specElement"}
                 onClick={() => this.props.clickHandler(this.props.name, this.props.index)}
            >
                <img style={getImgStyle(this.props.selected)} src={this.props.url} className="specElementImg"/>
            </div>
        );
    }
}