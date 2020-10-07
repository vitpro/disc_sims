import React, { Component } from 'react';

const getTalentStyle = (selected, hover) => ({
    border: selected? '2px #00D97B solid' : hover? '2px white solid' : '',
    borderRadius: '4px',
    backgroundColor: selected? '#343f5e' : '#22293d',
});

export default class Talent extends Component {

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
            <a data-wowhead={'spell='+ this.props.spellId} rel="noopener" className="wowheadTooltip"
                    onClick={(e) => {e.preventDefault()}}>
                <div style={getTalentStyle(this.props.selected, this.state.hover)} className="talentCell"
                     onClick={() => this.props.talentClickHandler(this.props.index)}
                     onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}
                >
                    <img src={this.props.url} className="talentCellImg"/>
                    <span className="talentCellName">{this.props.name}</span>
                </div>
            </a>
        );
    }
}