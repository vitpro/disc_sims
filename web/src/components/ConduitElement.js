import React, { Component } from 'react';

const getElemStyle = (selected, hover, coords_x, coords_y) => {
    const offset = { x: 650, y: 700 };
    const x_coord = (coords_x + offset.x).toString() + 'px';
    const y_coord = (coords_y + offset.y).toString() + 'px';
    return ({
        position: 'absolute',
        top: y_coord,
        left: x_coord,
        border: selected? '2px #00D97B solid' : hover? '2px white solid' : '2px #6d778b solid',
        borderRadius: '4px',
})};

const getImgStyle = (available, hover) => ({
    filter: available? '' : 'grayscale(100%)',
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
        let imgContainer;
        let conduitType;
        switch(this.props.conduitType) {
            case "generic":
                conduitType = ''; break;
            case "finesse":
                conduitType = (
                        <div className="conduitTypeElementIcon">
                            {/*<img src="/static/images/Conduits/Test.svg" />*/}
                        </div>
                ); break;
            case "potency":
                conduitType = (
                    <div className="conduitTypeElementIcon" >
                        <img src="/static/images/Conduits/Test.svg" />
                    </div>
                ); break;
            case "endurance":
                conduitType = (
                    <div className="conduitTypeElementIcon" >

                    </div>
                ); break;
            default:
                conduitType = '';
        }
        if (this.props.selected) {
            imgContainer = (
                <div className="conduitImgContainer">
                    <a data-wowhead={'spell='+ this.props.spellId} rel="noopener" className="wowheadTooltip"
                    onClick={(e) => {e.preventDefault()}}>
                        <img style={getImgStyle(this.props.available, this.state.hover)}
                             src={this.props.url} className="conduitElementImg"/>
                        <div className="conduitCloseElementIcon"
                            onClick={() => {
                                this.props.clickHandler(this.props.name, this.props.index, this.props.available, false)}}>
                            {/*/!*<img src="/static/images/cross.png" />*!/ <span className="closeConduitButton">X</span>*/}
                        </div>
                    </a>
                    {conduitType}
                </div>
            )
        } else {
            imgContainer = (
                <div className="conduitImgContainer">
                    <a data-wowhead={'spell='+ this.props.spellId} rel="noopener" className="wowheadTooltip"
                    onClick={(e) => {e.preventDefault()}}>
                        <img style={getImgStyle(this.props.available, this.state.hover)}
                                 src={this.props.url} className="conduitElementImg"/>
                    </a>
                    {conduitType}
                </div>
            )
        }

        return (
            <div style={getElemStyle(this.props.selected, this.state.hover, this.props.coords_x, this.props.coords_y)}
                 className="conduitElement"
                 onClick={() => this.props.clickHandler(this.props.name, this.props.index, this.props.available, true)}
                 onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}
            >
                {imgContainer}
            </div>
        );
    }
}