import React, { Component } from 'react';

const getElemStyle = selected => ({
    border: selected? '1px red solid' : '1px #b0b0b0 solid',
    // borderRadius: selected? '3px' : '',

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