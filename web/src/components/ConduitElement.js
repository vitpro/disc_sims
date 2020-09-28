import React, { Component } from 'react';

const getElemStyle = (selected, hover, coords_x, coords_y) => {
    const offset = { x: 700, y: 700 };
    const x_coord = (coords_x + offset.x).toString() + 'px';
    const y_coord = (coords_y + offset.y).toString() + 'px';
    return ({
        position: 'absolute',
        top: y_coord,
        left: x_coord,
        border: selected? '2px #fb1563 solid' : hover? '2px white solid' : '2px #6d778b solid',
        borderRadius: '4px',
})};

const getImgStyle = (available, hover) => ({
    filter: available? '' : hover? '' : 'grayscale(100%)',
});

export default class ConduitElement extends Component {

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
            <div style={getElemStyle(this.props.selected, this.state.hover, this.props.coords_x, this.props.coords_y)}
                 className="conduitElement"
                 onClick={() => this.props.clickHandler(this.props.name, this.props.index, this.props.available)}
                 onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}
            >
                <img style={getImgStyle(this.props.available, this.state.hover)}
                     src={this.props.url} className="conduitElementImg"/>
            </div>
        );
    }
}