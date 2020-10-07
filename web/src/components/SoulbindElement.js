import React, { Component } from 'react';

const getElemStyle = (selected, noneSelected, hover) => ({
    border: selected? '2px #00D97B solid' : hover? '2px white solid' : '2px #6d778b solid',
    borderRadius: '4px',
});

const getImgStyle = (selected, noneSelected, hover) => ({
    filter: selected? '' : noneSelected? '' : hover? '' : 'grayscale(100%)',
});

export default class SoulbindElement extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hover: false
        }
    }


    toggleHover = () => {
        this.setState({ hover: !this.state.hover });
    };

    render() {
        return (
            <div style={getElemStyle(this.props.selected, this.props.noneSelected, this.state.hover)}
                 className="soulbindElement"
                 onClick={() => this.props.clickHandler(this.props.name, this.props.index)}
                 onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}
            >
                <img style={getImgStyle(this.props.selected, this.props.noneSelected, this.state.hover)}
                     src={this.props.url} className="soulbindElementImg"/>
            </div>
        );
    }
}